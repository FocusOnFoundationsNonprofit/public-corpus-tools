# ===== START OF FILE primary/dbgen.py =====
# Library of functions and execution code to generate databases

import os
import json
import sqlite3
import csv
import re


### EXCHANGES SQLITE DB
def create_exchanges_db(db_path):
    """
    Create a SQLite database with the required schema for indexing exchanges.
    If the database doesn't exist, it will be created.
    If the database exists but the 'exchanges' table doesn't, the table will be created.
    If both the database and 'exchanges' table exist, no changes will be made to the structure.

    :param db_path: Path to the SQLite database file.
    :return: None
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchanges (
                filename TEXT PRIMARY KEY,  -- Use filename as the unique identifier
                date_PT TEXT,               -- Extracted date in Pacific time from file name
                time_PT TEXT,               -- Extracted time in Pacific time from file name
                user_question TEXT,         -- Include user question from JSON
                hmac_user_id TEXT,          -- HMAC user ID from JSON
                local_file_path TEXT        -- Relative local path to the file
            )
        ''')
        conn.commit()
        print(f"Database '{db_path}' checked/created with table 'exchanges'.")
    except sqlite3.Error as e:
        print(f"SQLite error during database operation: {e}")
    finally:
        conn.close()
def mtest_create_exchanges_db():
    db_path = 'exchanges.db'
    create_exchanges_db(db_path)

def index_exchanges_in_db(root_folder, exclude_subfolders=None):
    """
    Traverse the local folder structure starting from root_folder,
    extract metadata from each JSON file, and store it in the SQLite database.

    :param root_folder: Root local folder to start indexing from.
    :param exclude_subfolders: List of subfolder names to exclude from indexing. Defaults to None.
    :return: The relative path to the SQLite database file.
    """
    from primary.fileops import get_files_in_folder

    if exclude_subfolders is None:
        exclude_subfolders = []

    # Get all JSON files in the folder and subfolders, excluding specified subfolders
    json_files = get_files_in_folder(root_folder, include_subfolders=True, suffixpat_include='.json')
    json_files = [f for f in json_files if not any(subfolder in f for subfolder in exclude_subfolders)]

    db_path = os.path.join(root_folder, 'exchanges.db')
    
    # Ensure the database and table are created
    create_exchanges_db(db_path)  # Call the function to create the table if it doesn't exist

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    new_records = 0
    updated_records = 0
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract metadata
            filename = os.path.basename(file_path)
            # Extract date and time from filename
            if filename.startswith('qrag-exch_') and filename.endswith('.json'):
                date_time_part = filename[10:-5]  # Remove 'qrag-exch_' prefix and '.json' suffix
                date_PT, time_PT = date_time_part.split('_')
                time_PT = f"{time_PT[:2]}:{time_PT[2:4]}:{time_PT[4:]}"  # Format time as HH:MM:SS
            else:
                date_PT, time_PT = None, None
            user_id = data['metadata'].get('user_id')
            local_file_path = file_path  # Full local path to the file
            user_question = data['content'].get('user_question')

            # Use the user_id directly as HMAC user ID
            hmac_user_id = user_id

            # Insert or update the record
            cursor.execute('''
                INSERT OR REPLACE INTO exchanges (filename, date_PT, time_PT, user_question, hmac_user_id, local_file_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (filename, date_PT, time_PT, user_question, hmac_user_id, local_file_path))
            if cursor.rowcount > 0:
                new_records += 1
            else:
                updated_records += 1

        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")

    conn.commit()
    conn.close()
    print(f"Indexing complete. New records: {new_records}, Updated records: {updated_records}")
    return db_path
def mtest_index_exchanges_in_db():
    root_folder = 'exchanges/deutsch_qrag'  # Replace with your root folder
    exclude_subfolders = None  # ['not-reviewed']
    db_path = index_exchanges_in_db(root_folder, exclude_subfolders)
    print(f"SQLite database created at: {db_path}")

def view_all_exchanges(db_path):
    """
    Retrieve and print all records from the exchanges table.

    :param db_path: Path to the SQLite database file.
    :return: None
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM exchanges")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()
def mtest_view_all_exchanges():
    db_path = 'exchanges/deutsch_qrag/exchanges.db'
    view_all_exchanges(db_path)

def copy_exchanges_db_with_pii_add_column(exchanges_db_path):
    """
    Copy the exchanges database and add a column with a static value 'blank' for user_name.

    :param exchanges_db_path: Path to the exchanges SQLite database file.
    :return: Path to the new database with PII.
    """
    # Connect to the original database
    conn = sqlite3.connect(exchanges_db_path)
    cursor = conn.cursor()

    # Create a new database with 'pii-' prefix
    new_db_path = os.path.join(os.path.dirname(exchanges_db_path), f"pii-{os.path.basename(exchanges_db_path)}")
    if os.path.exists(new_db_path):
        os.remove(new_db_path)  # Remove existing file to avoid conflicts
    new_conn = sqlite3.connect(new_db_path)
    new_cursor = new_conn.cursor()

    try:
        # Get the schema of the original table
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='exchanges'")
        create_table_sql = cursor.fetchone()[0]

        # Create the table in the new database
        new_cursor.execute(create_table_sql)

        # Add the new column to the new database
        new_cursor.execute("ALTER TABLE exchanges ADD COLUMN user_name TEXT DEFAULT 'blank'")

        # Copy data from the original database to the new one
        cursor.execute("SELECT * FROM exchanges")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        placeholders = ', '.join(['?' for _ in columns])
        new_cursor.executemany(f"INSERT INTO exchanges ({', '.join(columns)}, user_name) VALUES ({placeholders}, 'blank')", rows)

        # Commit changes
        new_conn.commit()
        print(f"Created new database with PII at: {new_db_path}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Close connections
        conn.close()
        new_conn.close()

    return new_db_path

def copy_exchanges_db_with_user_pii(exchanges_db_path, users_csv_path):
    """
    Copy the exchanges database, add a table with user PII from the users CSV file,
    and add a username column to the exchanges table.

    :param exchanges_db_path: Path to the exchanges SQLite database file.
    :param users_csv_path: Path to the users CSV file.
    :return: Path to the new database with PII.
    """
    # Connect to the original database
    conn = sqlite3.connect(exchanges_db_path)
    cursor = conn.cursor()

    # Create a new database with 'pii-' prefix
    new_db_path = os.path.join(os.path.dirname(exchanges_db_path), f"pii-{os.path.basename(exchanges_db_path)}")
    if os.path.exists(new_db_path):
        os.remove(new_db_path)  # Remove existing file to avoid conflicts
    new_conn = sqlite3.connect(new_db_path)
    new_cursor = new_conn.cursor()

    try:
        # Get the schema of the original table
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='exchanges'")
        create_table_sql = cursor.fetchone()
        if not create_table_sql:
            raise ValueError("exchanges table not found in the original database")
        
        create_table_sql = create_table_sql[0]

        # Create the table in the new database
        new_cursor.execute(create_table_sql)
        print("Created exchanges table in the new database")

        # Copy data from the original database to the new one
        cursor.execute("SELECT * FROM exchanges")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        # print(f"Number of rows to copy: {len(rows)}")
        # print(f"Columns: {columns}")

        if not rows:
            print("Warning: No rows found in the original exchanges table")
        else:
            placeholders = ', '.join(['?' for _ in columns])
            insert_sql = f"INSERT INTO exchanges ({', '.join(columns)}) VALUES ({placeholders})"
            new_cursor.executemany(insert_sql, rows)
            print(f"Copied {new_cursor.rowcount} rows to the new database")

        # Add users table to the new database
        add_users_table_to_db(new_cursor, users_csv_path)

        # Add username column to the exchanges table
        add_username_column_to_exchanges(new_cursor)

        # Commit changes
        new_conn.commit()
        print(f"Created new database with PII at: {new_db_path}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        print(f"Error occurred on line: {e.__traceback__.tb_lineno}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Error occurred on line: {e.__traceback__.tb_lineno}")
    finally:
        # Close connections
        conn.close()
        new_conn.close()

    return new_db_path

# get users csv file by downloading from Webflow
def add_users_table_to_db(cursor, users_csv_path):
    """
    Add a users table to the database from a CSV file.

    :param cursor: SQLite cursor object.
    :param users_csv_path: Path to the users CSV file.
    """
    # Read the CSV file to get the column names
    with open(users_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        csv_columns = next(reader)

    # Create the 'users' table in the database with all CSV columns
    create_users_table_sql = f'''
        CREATE TABLE IF NOT EXISTS users (
            {', '.join([f'"{col}" TEXT' for col in csv_columns])}
        )
    '''
    cursor.execute(create_users_table_sql)

    # Read the users CSV file and insert data into the 'users' table
    with open(users_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        users_data = [tuple(row.values()) for row in reader]

    placeholders = ', '.join(['?' for _ in csv_columns])
    insert_sql = f'''
        INSERT OR REPLACE INTO users ({', '.join([f'"{col}"' for col in csv_columns])})
        VALUES ({placeholders})
    '''
    cursor.executemany(insert_sql, users_data)

def add_username_column_to_exchanges(cursor):
    """
    Add a username column to the exchanges table and populate it with usernames
    from the users table based on the HMAC User ID, excluding 'default' user IDs.

    :param cursor: SQLite cursor object.
    """
    try:
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(exchanges)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'user_name' not in columns:
            # Add the new column to the exchanges table
            cursor.execute("ALTER TABLE exchanges ADD COLUMN user_name TEXT DEFAULT 'NA'")
            print("Added user_name column to exchanges table.")
        else:
            print("user_name column already exists in exchanges table.")

        # Update the user_name column based on HMAC User ID, excluding 'default'
        cursor.execute("""
            UPDATE exchanges
            SET user_name = (
                SELECT "Name"
                FROM users
                WHERE users."HMAC User ID" = exchanges.hmac_user_id
            )
            WHERE EXISTS (
                SELECT 1
                FROM users
                WHERE users."HMAC User ID" = exchanges.hmac_user_id
            )
            AND exchanges.hmac_user_id != 'default'
        """)
        print(f"Updated {cursor.rowcount} rows in the exchanges table.")

        # Debug: Check contents of exchanges table after update
        cursor.execute("SELECT hmac_user_id, user_name FROM exchanges LIMIT 5")
        print("Sample data from exchanges table after update:")
        for row in cursor.fetchall():
            print(row)

    except sqlite3.Error as e:
        print(f"SQLite error while adding or updating user_name column: {e}")

def add_hmac_user_id_to_users_csv(users_csv_path):
    """
    Add a column for the HMAC User ID to the CSV file, appearing after the Email column.
    The HMAC is generated from the email address.

    :param users_csv_path: Path to the users CSV file.
    :return: Boolean indicating success or failure
    """
    from primary.aws import generate_hmac_hash, USERS_HMAC_SECRET_KEY

    try:
        # Read the CSV file
        with open(users_csv_path, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            
            # Insert new column header for HMAC User ID
            headers.insert(3, 'HMAC User ID')
            
            # Prepare data with HMAC User ID
            updated_rows = [headers]
            for row in reader:
                email = row[2]  # Assuming email is in the third column (index 2)
                # Generate HMAC for email using the existing function
                hmac_user_id = generate_hmac_hash(email, USERS_HMAC_SECRET_KEY)
                # Insert HMAC User ID into the row
                row.insert(3, hmac_user_id)
                updated_rows.append(row)
        
        # Write the updated data back to the CSV
        with open(users_csv_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(updated_rows)
        
        row_count = len(updated_rows) - 1  # Subtract 1 to exclude the header row
        print(f"Successfully added HMAC User ID to CSV. The file contains {row_count} rows.")
        return True
    except Exception as e:
        print(f"Failed to add HMAC User ID to CSV: {str(e)}")
        return False

def run_mtests_exchanges():
    pass
#if __name__ == "__main__":
    # mtest_create_exchanges_db()
    # mtest_index_exchanges_in_db()
    #mtest_view_all_exchanges()
    #mtest_generate_hmac_hash()
    add_hmac_user_id_to_users_csv("exchanges/deutsch_qrag/pii-users.csv")


# ===== END OF FILE primary/dbgen.py =====
