import os
import re
import csv
import subprocess
import pyperclip
import pyautogui
import time

from primary.fileops import *

import warnings  # Set the warnings to use a custom format
warnings.formatwarning = custom_formatwarning
# USAGE: warnings.warn(f"Insert warning message here")


### BLOCK PROCESSING
def get_blocks_from_file(qa_file_path, verbose=False):
    """
    Extracts and validates blocks of text from a file.

    :param qa_file_path: string of the path to the file to be read.
    :param verbose: boolean, if True, prints verbose messages. Default is False.
    :return: list of valid blocks from the file.
        """
    from primary.fileops import get_heading, verbose_print
    
    block_delimiter = "\n\n"  
    qa_text = get_heading(qa_file_path, "### qa")
    qa_text = re.sub(r'^#.*\n?', '', qa_text, flags=re.MULTILINE)
    qa_text = re.sub(r'\n{3,}', '\n\n', qa_text)
    blocks_list = []

    blocks = qa_text.split(block_delimiter)
    for block in blocks:
        if block.strip():
            blocks_list.append(block.strip())
            
    # valid_blocks = validate_qa_blocks(blocks_list)
    # if valid_blocks > 0:
    #     verbose_print(verbose, f"QA blocks ALL VALID for {valid_blocks} blocks for file {qa_file_path}")
    # else:
    #     invalid_blocks = 0 - valid_blocks  
    #     verbose_print(verbose, f"QA blocks validation FAILED on {invalid_blocks} blocks for file {qa_file_path}")
    return blocks_list

def get_field_value(block, field):
    """
    Extracts the content of a specified field from a block of text.

    :param block: string of the block of text to be processed.
    :param field: string of the field to be extracted from the block.
    :return: the content of the field in its appropriate data type, or None if the field is not found.
    """
    # Split the block into lines
    lines = block.split('\n')
    # Iterate through each line to find the field
    for line in lines:
        if line.startswith(field + ":"):
            # Extract the field content after the colon and space
            field_content = line[len(field) + 2:]
            # Special handling for STARS and TOPICS fields
            if field == "STARS" or field == "TRANSCRIPT START POSITION" or field == "TRANSCRIPT END POSITION":
                # Convert these fields to an integer
                return int(field_content)
            elif field == "TOPICS":
                # Convert the TOPICS field to a list of strings
                return [topic.strip() for topic in field_content.split(',')]
            else:
                # Return the field content as is for other fields
                return field_content
    # If the field is not found, return None
    return None

def get_all_fields_dict(block):
    """
    Extracts all fields and their contents from a block of text.

    :param block: string of the block of text to be processed.
    :return: dictionary of fields and their contents in their appropriate data types.
    """
    lines = block.split('\n')
    # Initialize an empty dictionary to store the fields and their contents
    fields_dict = {}
    # Iterate through each line to find the fields
    for line in lines:
        # Split the line at the first colon to separate the field and its content
        parts = line.split(":", 1)
        if len(parts) == 2:
            field, field_content = parts
            field = field.strip()
            field_content = field_content.strip()
            # Special handling for STARS and TOPICS fields
            if field == "STARS":
                # Convert the STARS field to an integer
                fields_dict[field] = field_content
            elif field == "TOPICS":
                # Convert the TOPICS field to a list of strings
                fields_dict[field] = [topic.strip() for topic in field_content.split(',')]
            else:
                # Add the field and its content to the dictionary
                fields_dict[field] = field_content
    # Return the dictionary of fields and their contents
    return fields_dict

def count_blocks(file_path, heading="## content"):  # quick way is to use find on a field
    """
    Counts the number of blocks in a specific section of a file, skipping comment lines.

    :param file_path: string of the path to the file to be processed.
    :param heading: string of the markdown heading to search for. Default is "## content".
    :return: integer representing the total number of blocks found.
    """
    content = get_heading(file_path, heading)
    
    if content is None:
        return 0
    
    # Remove comment lines (lines starting with # or whitespace followed by #)
    content_lines = [line for line in content.split('\n') if not line.lstrip().startswith('#')]
    content_without_comments = '\n'.join(content_lines)
    
    # Split the content into blocks (separated by blank lines)
    blocks = content_without_comments.split('\n\n')
    
    # Count non-empty blocks
    total_blocks = sum(1 for block in blocks if block.strip())
    
    return total_blocks


### TOPICS
# TODO try on townhall qa files - may need to update for alternate METADATA and CONTENT format
def extract_topic_counts_triples(qa_file_path, verbose=False):
    """
    Extracts topics from QA blocks in a file and counts their occurrences. 

    :param qa_file_path: string of the path to the QA file.
    :param verbose: boolean, if True, prints additional information during execution. Default is False.
    :return: string of CSV lines with each line in the format "topic, file_stem, count".
    """
    # Get the blocks from the file
    blocks = get_blocks_from_file(qa_file_path, verbose)
    
    # Initialize a dictionary to keep track of topics and their occurrences
    topic_dict = {}
    
    # Iterate through each block to extract topics and count their occurrences
    for block in blocks:
        # Use the helper function to get a list of topics from the block
        topics = get_field_value(block, "TOPICS")
        if topics:
            # Iterate through the topics and update their count in the dictionary
            for topic in topics:
                if topic:  # Ensure that the topic is not an empty string
                    topic_dict[topic] = topic_dict.get(topic, 0) + 1
                else:
                    warnings.warn(f"Warning: TOPIC is blank and should have been previously validated before calling this function for file {qa_file_path}\n{block}\n\n")
    
    # Get the file stem (filename without extension)
    file_stem = os.path.splitext(os.path.basename(qa_file_path))[0]
    
    # Build the result text with the required format
    topic_counts_csv_lines = "\n".join([f"{topic}, {file_stem}, {count}" for topic, count in topic_dict.items()])
    
    return topic_counts_csv_lines

def create_topics_matrix(folder_paths, target_file_path="matrix_topics.csv", suffixpat_include="_qafixed"):
    """
    Collects topics from files in specified folders and creates a CSV matrix file at the target file path.

    :param folder_paths: list of strings of folder paths to search for files.
    :param target_file_path: string of the path where the resulting CSV file will be created. If no folder is provided in the path, the parent folder of the first folder in the folder_paths list will be used.
    :param suffix_include: string of the suffix to include in file search. Default is "_qafixed".
    :return: string of the path to the created csv file.
    """
    from primary.fileops import apply_to_folder, create_csv_matrix_from_triples
    
    all_topics_results = []  # Initialize an empty list to collect all topics from all folders

    # Iterate over each folder path and process files within
    for folder_path in folder_paths:
        # Use apply_to_folder to process files and get topics
        topics_results = apply_to_folder(extract_topic_counts_triples, folder_path, suffixpat_include=suffixpat_include)
        # Append the topics from the current folder to the all_topics_results list
        all_topics_results.extend(topics_results.values())

    triples_text = "\n".join(all_topics_results)  # no need to srt because that's done by create_csv_matrix_from_triples

    # Check if the target file path has a folder component
    if not os.path.dirname(target_file_path):
        # If not, use the parent folder of the first folder in folder_paths
        parent_folder = os.path.dirname(folder_paths[0])
        target_file_path = os.path.join(parent_folder, os.path.basename(target_file_path))

    # Call the create_csv_from_triples function to create the CSV file
    return create_csv_matrix_from_triples(triples_text, target_file_path)  # function is in fileops

def change_topic_in_file(file_path, find_topic, replace_topic):
    """
    Replaces a specified topic with another in a single file.

    :param file_path: string of the file path to process.
    :param find_topic: string of the topic to find.
    :param replace_topic: string of the topic to use as a replacement.
    :return: tuple of (int, int) representing (replacements_in_file, total_replacements)
    """
    if find_topic == replace_topic:
        print(f"Aborting: find_topic '{find_topic}' and replace_topic '{replace_topic}' are the same.")
        return 0

    from primary.fileops import read_metadata_and_content, write_metadata_and_content

    metadata, content = read_metadata_and_content(file_path)
    
    blocks = get_blocks_from_file(file_path)
    content_lines = content.split('\n')
    replacements_in_file = 0
    for i, line in enumerate(content_lines):
        if line.startswith("TOPICS:"):
            topics = line[len("TOPICS:"):].strip().split(', ')
            if find_topic in topics:
                topics = [replace_topic if topic == find_topic else topic for topic in topics]
                new_line = 'TOPICS: ' + ', '.join(topics)
                content_lines[i] = new_line
                replacements_in_file += topics.count(replace_topic)
    
    if replacements_in_file > 0:
        new_content = '\n'.join(content_lines)
        write_metadata_and_content(file_path, metadata, new_content, overwrite='yes')
    
    return replacements_in_file

def change_topic_in_folders(folder_paths, find_topic, replace_topic, suffixpat_include="_qafixed"):
    """
    Replaces a specified topic with another across files in given folders.

    :param folder_paths: list of strings of folder paths to search for files.
    :param find_topic: string of the topic to find.
    :param replace_topic: string of the topic to use as a replacement.
    :param suffix_include: string of the suffix to include in file search.
    :return: None.
    """
    from primary.fileops import apply_to_folder
    
    total_replacements = 0
    files_with_replacements = []

    def process_file(file_path):
        nonlocal total_replacements, files_with_replacements
        replacements_in_file = change_topic_in_file(file_path, find_topic, replace_topic)
        if replacements_in_file > 0:
            total_replacements += replacements_in_file
            files_with_replacements.append((file_path, replacements_in_file))

    for folder_path in folder_paths:
        apply_to_folder(process_file, folder_path, suffixpat_include=suffixpat_include)

    print(f"Total replacements done: {total_replacements}")

    for file_path, count in files_with_replacements:
        file_name = os.path.basename(file_path)
        print(f"{count} {file_name}")

def review_singlet_topic_SONNET(folder_paths, matrix_csv_file_path, starting_letter="a"):
    # Read the CSV file
    with open(matrix_csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        topics = {row['row title']: sum(int(count) for count in row.values() if count.isdigit()) for row in reader}

    # Filter singlet topics
    singlet_topics = {topic: None for topic, count in topics.items() if count == 1 and topic.lower().startswith(starting_letter)}

    # Read the CSV file again to find files containing singlet topics
    with open(matrix_csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for topic in singlet_topics.keys():
            # Find the file that contains the topic
            csvfile.seek(0)  # Reset file pointer before each search
            file_with_topic = next((col for col in reader.fieldnames[1:] if any(int(row[col]) > 0 for row in reader if row['row title'] == topic)), None)
            csvfile.seek(0)  # Reset file pointer after each search
            
            if file_with_topic:
                # Search for the file within the given folder paths
                file_path = None
                for folder in folder_paths:
                    potential_path = os.path.join(folder, file_with_topic)
                    if os.path.exists(potential_path):
                        file_path = potential_path
                        break
                
                if file_path is None:
                    print(f"Could not find file '{file_with_topic}' in any of the provided folders.")
                    continue
                # Open the file in VS Code and search for the topic
                subprocess.run(['code', '--goto', f'{file_path}:1', '--search', topic])
                
                # Prompt user for action
                action = input(f"Topic '{topic}' found in {file_with_topic}. Enter 'DEL' to delete, press Enter to skip, or enter a new topic name to change: ")
                
                if action.upper() == 'DEL':
                    # Delete the topic
                    change_topic_in_file(file_path, topic, '')
                    print(f"Topic '{topic}' deleted from {file_with_topic}")
                elif action and action.upper() != 'd':  # use single lowercase 'd' for delete
                    # Change the topic
                    change_topic_in_file(file_path, topic, action)
                    print(f"Topic '{topic}' changed to '{action}' in {file_with_topic}")
                else:
                    print(f"Skipped topic '{topic}' in {file_with_topic}")
            else:
                print(f"Could not find file for topic '{topic}'")

    print("Review of singlet topics completed.")

def review_singlet_topic(folder_paths, matrix_csv_file_path, starting_letter="a"):
    import os
    import csv
    import subprocess

    # Step 1: Read the CSV file and build the data structures
    topic_counts = {}  # Mapping from topic to total count
    topic_file_stems = {}  # Mapping from topic to list of file stems

    print(f"Reading topics from CSV file: {matrix_csv_file_path}")
    with open(matrix_csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)  # Get the headers (first row)
        if not headers:
            print("CSV file is empty or missing headers.")
            return

        # The first column is assumed to be 'row title' or similar
        file_stems = headers[1:]  # Exclude the first column header
        print(f"File stems extracted: {file_stems}")

        for row in csvreader:
            if len(row) < 2:
                continue  # Skip invalid rows
            topic = row[0].strip()
            counts = [int(count.strip()) for count in row[1:]]

            total_count = sum(counts)
            topic_counts[topic] = total_count

            # Find the indices where the topic occurs
            file_indices = [i for i, count in enumerate(counts) if count > 0]
            if topic not in topic_file_stems:
                topic_file_stems[topic] = []
            for idx in file_indices:
                file_stem = file_stems[idx]
                topic_file_stems[topic].append(file_stem)

    print(f"Total topics read: {len(topic_counts)}")

    # Step 2: Build mapping from file stems to full file paths
    file_stem_to_path = {}  # Mapping from file stem to full file path

    print("Building file stem to path mapping...")
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                stem, ext = os.path.splitext(filename)
                full_path = os.path.join(root, filename)
                if stem not in file_stem_to_path:
                    file_stem_to_path[stem] = full_path

    # Step 3: Process topics with total count == 1 and starting with starting_letter
    matching_topics = [topic for topic in topic_counts if topic_counts[topic] == 1 and topic.startswith(starting_letter)]
    print(f"Total topics with count == 1 and starting with '{starting_letter}': {len(matching_topics)}")

    if not matching_topics:
        print("No topics to process.")
        return

    for topic in sorted(matching_topics):
        total_count = topic_counts[topic]
        file_stems = topic_file_stems[topic]
        if len(file_stems) != 1:
            print(f"Warning: Topic '{topic}' occurs in multiple files but total count is 1.")
            continue
        file_stem = file_stems[0]
        file_path = file_stem_to_path.get(file_stem)
        if not file_path:
            print(f"File for file stem '{file_stem}' not found.")
            continue

        print(f"\nProcessing topic '{topic}' in file '{file_path}'")

        # Open the file in VS Code and perform search
        try:
            subprocess.run(['code', file_path])

            # Copy the topic to the clipboard
            pyperclip.copy(topic)

            # Wait a moment to ensure VS Code has focus
            time.sleep(1)  # Adjust the sleep time if necessary

            # Simulate Ctrl+F to open the find dialog
            pyautogui.hotkey('command', 'f')

            # Paste the topic into the find dialog
            pyautogui.hotkey('command', 'v')

        except Exception as e:
            print(f"Error opening file in VS Code: {e}")
            continue

        print(f"Opened file '{file_path}' in VS Code. Please search for topic '{topic}' using the search tool.")

        # Prompt the user for action
        user_input = input("Type 'DEL' to delete the topic, type new topic to replace, or press Enter to keep: ").strip()

        if user_input.upper() == 'DEL':
            # Delete the topic
            print(f"Deleting topic '{topic}' in file '{file_path}'")
            change_topic_in_file(file_path, topic, '')
        elif user_input == '':
            # Do nothing
            print(f"Keeping topic '{topic}'")
        else:
            # Replace topic
            new_topic = user_input
            print(f"Replacing topic '{topic}' with '{new_topic}' in file '{file_path}'")
            change_topic_in_file(file_path, topic, new_topic)



