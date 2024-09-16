import os
import re
from collections import defaultdict

from primary.fileops import *

import warnings  # Set the warnings to use a custom format
warnings.formatwarning = custom_formatwarning
# USAGE: warnings.warn(f"Insert warning message here")


### QA VALIDATION
def validate_stars(stars_str):
    if not stars_str.strip():  # Check if the string is blank or just whitespace
        return True
    try:
        stars = int(stars_str)
        return True  # Accept any integer, including negative numbers
    except ValueError:
        return False  # Return False if the string can't be converted to an integer

def validate_topics(topics_str):
    if ",  " in topics_str or re.search(r',(?![ ])', topics_str):
        return False
    topics = re.split(r',\s*', topics_str.strip())
    return all(topic.strip() == topic for topic in topics)

def validate_qa_blocks(blocks_list, required_fields, custom_validators=None):
    """
    Validates the structure and content of QA blocks against required fields.

    :param blocks_list: List of QA blocks, each block is a string of text representing a QA entry.
    :param required_fields: List of required field names.
    :param custom_validators: Dictionary of field names and their corresponding validation functions (default: None).
    :return: Integer representing the number of valid blocks if all are valid, or the negative count of invalid blocks.
    """
    custom_validators = custom_validators or {}
    
    invalid_blocks_count = 0
    total_blocks = len(blocks_list)

    for block in blocks_list:
        block_fields = {}
        block_errors = []

        # Parse the block into fields
        for line in block.strip().split("\n"):
            if line:
                try:
                    key, value = line.split(":", 1)
                    block_fields[key.strip()] = value.strip()
                except ValueError:
                    block_errors.append(f"Invalid line format: {line}")

        # Check for required fields
        for field in required_fields:
            if field not in block_fields:
                block_errors.append(f"Missing required field: {field}")

        # Validate field contents using custom validators if provided
        for field, validator in custom_validators.items():
            if field in block_fields:
                try:
                    if not validator(block_fields[field]):
                        block_errors.append(f"Custom validation failed for field: {field}")
                except Exception as e:
                    block_errors.append(f"Error in custom validator for field {field}: {str(e)}")

        # Update validation statistics
        if block_errors:
            invalid_blocks_count += 1
            question = block_fields.get("QUESTION", "Question not found")
            for error in block_errors:
                warnings.warn(f"{error} in block\nQUESTION: {question}")

    if invalid_blocks_count == 0:
        return total_blocks
    else:
        return -invalid_blocks_count

def is_valid_file_qa(file_path, required_fields, custom_validators, verbose=False):
    """
    Function to validate QA blocks in a file and return True if all blocks are valid

    :param file_path: string of the path to the file to be validated
    :param required_fields: List of required field names.
    :param custom_validators: Dictionary of field names and their corresponding validation functions.
    :param verbose: boolean to control verbose output
    :return: boolean indicating whether all blocks in the file are valid
    """
    from primary.structured import get_blocks_from_file
    blocks = get_blocks_from_file(file_path)
    valid_blocks = validate_qa_blocks(blocks, required_fields, custom_validators)
    if valid_blocks < 0:
        print(f"FAIL - INVALID blocks for file: {file_path}\n\n\n")
        return False
    if verbose:
        print(f"VALID blocks for file: {file_path}")
    return True

def validate_folders_qa(folder_paths, required_fields, custom_validators, suffixpat_include="_qafixed"):
    """
    Validates QA blocks in all files within specified folders, printing the number of valid files in each folder
    and statistics about required and optional fields.

    :param folder_paths: list of strings of folder paths to search for files.
    :param required_fields: List of required field names.
    :param custom_validators: Dictionary of field names and their corresponding validation functions.
    :param suffixpat_include: string of the suffix to include in file search. Default is "_qafixed".
    :return: string of the path of the first file with invalid QA blocks if any; None if all files are valid.
    """
    from primary.fileops import get_files_in_folder
    from primary.structured import get_blocks_from_file

    total_valid_files = 0
    total_files = 0
    optional_fields_stats = defaultdict(lambda: {'files': set(), 'blocks': 0})

    for folder_path in folder_paths:
        file_paths = get_files_in_folder(folder_path, suffixpat_include=suffixpat_include)
        valid_files_count = 0
        
        for file_path in file_paths:
            total_files += 1
            blocks = get_blocks_from_file(file_path)
            if is_valid_file_qa(file_path, required_fields, custom_validators):
                valid_files_count += 1
                total_valid_files += 1
                
                # Count optional fields
                for block in blocks:
                    for line in block.strip().split("\n"):
                        if line:
                            key, _ = line.split(":", 1)
                            field = key.strip()
                            if field not in required_fields:
                                optional_fields_stats[field]['files'].add(file_path)
                                optional_fields_stats[field]['blocks'] += 1
            else:
                print(f"Number of validated files: {valid_files_count} in {folder_path}: ")
                print(f"INVALID file: {file_path}")
                return file_path

        print(f"Number of valid files in {folder_path}: {valid_files_count}")

    print(f"\nTotal valid files across all folders: {total_valid_files}/{total_files}")
    print(f"\nRequired fields: {', '.join(required_fields)}")
    print("\nOptional fields statistics:")
    for field, stats in optional_fields_stats.items():
        print(f"  {field}: appears in {len(stats['files'])} files and {stats['blocks']} blocks")

    return None

### DEUTSCH
DEUTSCH_FOLDER_PATHS = ["data/deutsch/f8_done_qafixed_and_vrb", "data/deutsch/f8_qafixed_talks"]
def validate_corpus_deutsch():
    required_fields = ["QUESTION", "TIMESTAMP", "ANSWER", "EDITS", "TOPICS", "STARS"]
    custom_validators = {
        "STARS": validate_stars,
        "TOPICS": validate_topics
    }
    validate_folders_qa(DEUTSCH_FOLDER_PATHS, required_fields, custom_validators)


if __name__ == "__main__":
    #validate_corpus_deutsch()
    from primary.structured import create_topics_matrix, change_topic_in_folders, review_singlet_topic
    cur_matrix_topics_csv = "data/deutsch/matrix_topics.csv"
    #cur_matrix_topics_csv = create_topics_matrix(DEUTSCH_FOLDER_PATHS)
    #change_topic_in_folders(DEUTSCH_FOLDER_PATHS, "AI safety", "AI risk")
    review_singlet_topic(DEUTSCH_FOLDER_PATHS, cur_matrix_topics_csv, "b")

def validate_qa_blocks_deutsch_OLD(blocks_list):
    """
    Validates the structure and content of QA blocks against required and optional fields.

    :param blocks_list: list of qa blocks where each block is a string of text representing a qa entry.
    :return: the number of valid blocks if all are valid, or the negative count of invalid blocks.
    """
    required_fields = ["QUESTION", "TIMESTAMP", "ANSWER", "EDITS", "TOPICS", "STARS"]
    optional_fields = ["NOTES", "ORIGINAL QUESTION", "ALTERNATE QUESTION", "ADDITIONAL QUESTION"]

    all_fields = set(required_fields + optional_fields)
    invalid_blocks_count = 0

    for block in blocks_list:
        block_lines = block.strip().split("\n")
        block_fields = {}
        block_is_valid = True  # Track validity of individual block
        for line in block_lines:
            if line:
                try:
                    key, value = line.split(":", 1)
                    block_fields[key.strip()] = value.strip()  # Ensure that the key is stripped of whitespace
                except ValueError as e:
                    warnings.warn(f"Error splitting line '{line}' in block:\n{block}\nError: {e}")
                    block_is_valid = False
                    break
            else:
                warnings.warn(f"Block contains a blank line:\n{block}")
                block_is_valid = False
                break

        # Check for invalid fields
        for field in block_fields:
            if field not in all_fields:
                warnings.warn(f"Invalid field '{field}' in block:\n{block}\n\n")
                block_is_valid = False

        # Check required fields
        for field in required_fields:
            if field not in block_fields:
                warnings.warn(f"Missing required field '{field}' in block:\n{block}")
                block_is_valid = False
            else:
                if field == "STARS":
                    stars_str = block_fields[field]
                    stars = int(stars_str) if stars_str.isdigit() else 0
                    if stars < 0:
                        warnings.warn(f"Invalid format for STARS field.")
                        block_is_valid = False
                elif field == "TOPICS":
                    topics_line = block_fields[field]
                    # Check for incorrect delimiters and print a warning if necessary
                    if ",  " in topics_line:
                        warnings.warn(f"Double space after comma in topics line '{topics_line}'")
                        block_is_valid = False
                    elif re.search(r',(?![ ])', topics_line):
                        warnings.warn(f"Missing space after comma in topics line '{topics_line}'")
                        block_is_valid = False
                    # Split the topics by comma, accounting for optional spaces and removing trailing whitespace
                    topics = re.split(r',\s*', topics_line.strip())
                    # Remove any leading or trailing whitespace from each topic and filter out empty strings
                    cleaned_topics = [topic.strip() for topic in topics if topic.strip()]
                    # Check for and warn about trailing whitespace in the original topic strings
                    for topic, cleaned_topic in zip(topics, cleaned_topics):
                        if topic != cleaned_topic:
                            warnings.warn(f"Incorrect whitespace in topic '{topic}'")
                            block_is_valid = False

        # Check optional fields
        for field in optional_fields:
            if field in block_fields and not block_fields[field]:
                warnings.warn(f"Optional field '{field}' is present but blank in block:\n{block}")
                block_is_valid = False

        if not block_is_valid:
            invalid_blocks_count += 1
            
    if invalid_blocks_count == 0:
        return len(blocks_list)
    else:
        return (0 - invalid_blocks_count)

### FDA TOWNHALLS
def remove_lines_fda_townhall(text):
    """ 
    Remove lines from a string of FDA townhall transcript text that match certain patterns.

    :param text: string of the transcript text to be cleaned.
    :return: string of the cleaned transcript text.
    """
    # Matches "Page X" where X is a number, or a line that starts with a number followed by whitespace, indicating a page header or footer.
    page_pattern = re.compile(r"^(Page \d+|\d+)\s*$", re.IGNORECASE)
    
    # Matches dates in various formats, e.g., "July 14, 2021", "3-25-20", followed by any text.
    date_pattern = re.compile(r"^(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}.*$|\d{1,2}-\d{1,2}-\d{2,4}.*$", re.IGNORECASE)
    
    # Matches time formats, e.g., "12:15 pm ET", "3:00 pm ET".
    time_pattern = re.compile(r"^\d{1,2}:\d{2} (?:am|pm) ET\s*$", re.IGNORECASE)
    
    # Matches introductory lines that typically start with the document title or section,
    # e.g., "Virtual Townhall", "FDA Virtual Town Hall Series – ", "FDA Virtual Town", "Virtual Town", "FDA Virtual Townhall"
    title_pattern = re.compile(r"^(?:Virtual Townhall|FDA Virtual Town Hall Series – |FDA Virtual Town|Virtual Town|FDA CDRH|Immediately in Effect Guidance|FDA Virtual Townhall)\s*$", re.MULTILINE)
    
    # Matches ending lines that typically say "END", "[ Event concluded ]", or a line with any number of asterisks with any amount of white space before or after
    end_pattern = re.compile(r"^(END|\[\s*Event concluded\s*\]|\s*\*+\s*)\s*$", re.IGNORECASE)
    
    # Matches moderator lines that include the moderator's name, e.g., "Moderator: Irene Aihie".
    # These lines are often part of the introductory section that precedes the actual content.
    moderator_pattern = re.compile(r"^Moderator: [A-Za-z\s]+\s*$", re.MULTILINE)
    
    # List of all patterns for iteration
    patterns = [page_pattern, date_pattern, time_pattern, title_pattern, end_pattern, moderator_pattern]
    
    # Split the text into lines
    lines = text.splitlines()
    
    # Apply each pattern and remove matching lines on a per-line basis
    cleaned_lines = []
    for line in lines:
        if not any(pattern.match(line) for pattern in patterns):
            cleaned_lines.append(line)
    
    # Join the cleaned lines back into a single string
    cleaned_text = "\n".join(cleaned_lines)
    # Remove extra newlines and spaces that might be left after removal
    #cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text).strip()
    return cleaned_text

# TODO test after July refactor
def clean_fda_townhall(file_path):
    """
    Cleans the FDA townhall file by removing unnecessary lines and fixing speaker text.

    :param file_path: string of the path to the file to be cleaned.
    :param suffix_new: string of the suffix to be added to the cleaned file. Default is '_cleaned'.
    :return: The cleaned text with the heading set.
    """
    from primary.fileops import get_heading, set_heading
    from primary.docwork import reformat_transcript_text

    heading = "### transcript"
    text = get_heading(file_path, heading)
    
    cleaned1_text = remove_lines_fda_townhall(text)
    cleaned2_text = reformat_transcript_text(cleaned1_text)
    
    set_heading(file_path, '\n' + cleaned2_text, heading)

# TODO test after July refactor
def run_clean_on_fda_townhalls(source_folder, destination_folder):
    """
    Cleans the files in the source folder and moves the cleaned files to the destination folder.

    :param source_folder: string of the path to the source folder containing the files to be cleaned.
    :param destination_folder: string of the path to the destination folder where the cleaned files will be moved.
    :return: None
    """
    from primary.fileops import apply_to_folder, move_files_with_suffix

    apply_to_folder(clean_fda_townhall, source_folder)
    move_files_with_suffix(source_folder, destination_folder, "_cleaned")

# TODO WIP - add path to find_replace_csv after testing fileops func
def run_fix_names_on_fda_townhalls():  # COPY to your run file and use there
    from primary.fileops import find_and_replace_from_csv, apply_to_folder, sub_suffix_in_file
    
    # ***NOTE*** must manually copy orig-folder to create fixnames_folder, enter that new path below
    orig_folder = 'data/floodlamp_fda/townhalls/f4_md_cleaned_manualedits'
    suffix_orig = '_cleaned'
    fixnames_folder = 'data/floodlamp_fda/townhalls/f5_md_fixnames'
    suffix_new = '_fixnames'
    csv_file_path = 'data/floodlamp_fda/townhalls/names_findandreplace_fda_townhalls.csv'
    
    # TODO need to fix in docwork
    #print(validate_townhalls(cur_folder_path))
    #print(create_speakers_matrix(cur_folder_path))
    #apply_to_folder(sub_suffix_in_file, fixnames_folder, suffix_new, suffix_include='_fixnamed')
    # ***NOTE*** must copy files before running
    #find_and_replace_from_csv(fixnames_folder, csv_file_path, suffix_include=suffix_orig, verbose=True)
    #apply_to_folder(sub_suffix_in_file, fixnames_folder, suffix_new, suffix_include=suffix_orig)
    # NEXT PASS
    #find_and_replace_from_csv(fixnames_folder, csv_file_path, suffix_include=suffix_new, verbose=True)

def validate_qa_blocks_townhall_OLD(blocks_list):
    """
    Validates the structure and content of QA blocks against required and optional fields.

    :param blocks_list: list of qa blocks where each block is a string of text representing a qa entry.
    :return: the number of valid blocks if all are valid, or the negative count of invalid blocks.
    """
    required_fields = ["QUESTION", "ANSWER", "QUESTION SPEAKER", "ANSWER SPEAKER", "TOPICS", "STARS"]
    optional_fields = ["NOTES", "ORIGINAL QUESTION", "ALTERNATE QUESTION", "ADDITIONAL QUESTION"]

    all_fields = set(required_fields + optional_fields)
    invalid_blocks_count = 0

    for block in blocks_list:
        block_lines = block.strip().split("\n")
        block_fields = {}
        block_is_valid = True  # Track validity of individual block
        for line in block_lines:
            if line:
                try:
                    key, value = line.split(":", 1)
                    block_fields[key.strip()] = value.strip()  # Ensure that the key is stripped of whitespace
                except ValueError as e:
                    warnings.warn(f"Error splitting line '{line}' in block:\n{block}\nError: {e}")
                    block_is_valid = False
                    break
            else:
                warnings.warn(f"Block contains a blank line:\n{block}")
                block_is_valid = False
                break

        # Check for invalid fields
        for field in block_fields:
            if field not in all_fields:
                warnings.warn(f"Invalid field '{field}' in block:\n{block}\n\n")
                block_is_valid = False

        # Check required fields
        for field in required_fields:
            if field not in block_fields:
                warnings.warn(f"Missing required field '{field}' in block:\n{block}")
                block_is_valid = False
            else:
                if field == "STARS":
                    stars_str = block_fields[field]
                    stars = int(stars_str) if stars_str.isdigit() else 0
                    if stars < 0:
                        warnings.warn(f"Invalid format for STARS field.")
                        block_is_valid = False
                elif field == "TOPICS":
                    topics_line = block_fields[field]
                    # Check for incorrect delimiters and print a warning if necessary
                    if ",  " in topics_line:
                        warnings.warn(f"Double space after comma in topics line '{topics_line}'")
                        block_is_valid = False
                    elif re.search(r',(?![ ])', topics_line):
                        warnings.warn(f"Missing space after comma in topics line '{topics_line}'")
                        block_is_valid = False
                    # Split the topics by comma, accounting for optional spaces and removing trailing whitespace
                    topics = re.split(r',\s*', topics_line.strip())
                    # Remove any leading or trailing whitespace from each topic and filter out empty strings
                    cleaned_topics = [topic.strip() for topic in topics if topic.strip()]
                    # Check for and warn about trailing whitespace in the original topic strings
                    for topic, cleaned_topic in zip(topics, cleaned_topics):
                        if topic != cleaned_topic:
                            warnings.warn(f"Incorrect whitespace in topic '{topic}'")
                            block_is_valid = False

        # Check optional fields
        for field in optional_fields:
            if field in block_fields and not block_fields[field]:
                warnings.warn(f"Optional field '{field}' is present but blank in block:\n{block}")
                block_is_valid = False

        if not block_is_valid:
            invalid_blocks_count += 1
            
    if invalid_blocks_count == 0:
        return len(blocks_list)
    else:
        return (0 - invalid_blocks_count)

def validate_qa_blocks_townhall(blocks_list):
    required_fields = ["QUESTION", "ANSWER", "QUESTION SPEAKER", "ANSWER SPEAKER", "TOPICS", "STARS"]
    
    custom_validators = {
        "STARS": validate_stars,
        "TOPICS": validate_topics
    }
    
    return validate_qa_blocks(blocks_list, required_fields, custom_validators)