all_source_defs_docstring (39,481 tokens)

## primary/fileops.py (7,075 tokens)
### INITIAL (235 tokens)
def custom_formatwarning(msg, category, filename, lineno, line=None):
    """
    DO NOT CALL - only used to define the custom format
    """
def verbose_print(verbose, *messages):
    """
    Helper function to pass on bool verbose and make verbose printing cleaner
    
    :param verbose: boolean for whether to print the messages.
    :param messages: tuple of variable-length argument list.
    :return: None
    """
def check_file_exists(file_path, operation_name):
    """
    Checks file existence and raises a ValueError if not found, which stops execution.

    :param file_path: string of file path which can be absolute or relative.
    :param operation_name: string of the message that the ValueError will print, typically the function name - optional message.
    :return: bool, True if file exists, False otherwise.
    """
def warn_file_overwrite(file_path):
    """
    Checks if a file already exists and issues a warning if it does.

    :param file_path: string representing the path of the file to be checked.
    :return: bool, True if file exists, False otherwise.
    """
### SUFFIX (676 tokens)
def get_suffix(file_str, delimiter='_'):
    """
    Extracts the suffix from a given file string based on a specified delimiter.

    :param file_str: string of the file name from which to extract the suffix.
    :param delimiter: string representing the delimiter used to separate the suffix from the rest of the file string. Default is "_".
    :return: string of the extracted suffix or None if no valid suffix is found.
    """
def add_suffix_in_str(file_str, suffix_add):
    """
    Adds a suffix to a given file string.

    :param file_str: string of the file name to which the suffix will be added.
    :param suffix_add: string of the suffix to be added to the file string.
    :return: string of the file name with the added suffix.
    """
def sub_suffix_in_str(file_str, suffix_sub, delimiter='_'):
    """
    Replaces the existing suffix in a file string with a new suffix.

    :param file_str: string of the file name from which to replace the suffix.
    :param suffix_sub: string of the new suffix to replace the existing one.
    :param delimiter: string representing the delimiter used to separate the suffix from the rest of the file string. Default is "_".
    :return: string of the file name with the replaced suffix or the original file string if no valid suffix is found.
    """
def remove_all_suffixes_in_str(file_str, delimiter='_'): # DS, cat 1, unitests 7 - no mock
    """
    Removes all suffixes from a given file string based on a specified delimiter while retaining the original file extension.

    :param file_str: string of the file name from which to remove all suffixes.
    :param delimiter: string representing the delimiter used to separate the suffixes from the rest of the file string. Default is "_".
    :return: string of the file name with all suffixes removed but with the original extension preserved.
    """
def copy_file_and_append_suffix(file_path, suffix_new):
    """
    Copies the file with a new suffix added before the file extension.

    :param file_path: string of the path to the original file.
    :param suffix_new: string of the suffix to be appended to the original filename before the file extension.
    :return: string of the path to the newly created file with the new suffix.
    """
def sub_suffix_in_file(file_path, suffix_new):
    """
    Substitutes the suffix in the file name of the given file path with a new suffix.
    If new_suffix is empty '' then it will remove the last suffix of the file.

    :param file_path: string, the path to the original file.
    :param suffix_new: string, the new suffix to replace the existing one in the file name.
    :return: string, the path to the newly created file with the substituted suffix.
    """
def count_suffixes_in_folder(folder_path):
    """
    Analyzes all the files in the specified folder and prints the number of files for each unique suffix, alphabetized.

    :param folder_path: string of the folder path to search for files and analyze suffixes.
    :return: None. The function prints the suffixes and their counts.
    """
### FOLDER (414 tokens)
def get_files_in_folder(folder_path, suffixpat_include=None, suffixpat_exclude=None, include_subfolders=False):
    """
    Retrieves a list of file paths from the specified folder, sorted in alphabetical order.
    Optionally filters by suffix pattern and includes subfolders.

    :param folder_path: string of the path to the folder from which to retrieve files.
    :param suffixpat_include: string of the suffix pattern that included files must have.
    :param suffixpat_exclude: string of the suffix pattern that files must not have to be included.
    :param include_subfolders: boolean indicating whether to include files from subfolders.
    :return: list of strings of the file paths that meet the specified criteria.
    """
def apply_to_folder(worker_function, folder_path, *args, suffixpat_include=None, suffixpat_exclude=None, include_subfolders=False, verbose=False, **kwargs):
    """
    Controller function that applies a specified worker function to each file in a folder.
    The worker function must operate on a single file.
    If it needs the folder name, that can be extracted from the file path.
    If it's creating or writing to another file, that filename or path can be given as another argument.

    :param worker_function: worker function name to apply to each file, not a string so do not use quotes.
    :param folder_path: string of the path to the folder from which to retrieve files.
    :param args: additional arguments to pass to the function.
    :param suffixpat_include: string of the suffix pattern that included files must have.
    :param suffixpat_exclude: string of the suffix pattern that files must not have to be included.
    :param include_subfolders: boolean of whether to include files from subfolders.
    :param verbose: boolean for printing verbose messages. Defaults to True.
    :param kwargs: additional keyword arguments to pass to the function.
    :return: a dictionary with file paths as keys and function return values as values.
    """
### READ WRITE (855 tokens)
def read_complete_text(file_path):
    """
    Reads the entire text from a file.

    :param file_path: string of the file path which can be absolute or relative.
    :return: string of the complete text read from the file.
    """
def read_metadata_and_content(file_path):
    """
    Reads the text from a file and splits it into the metadata and content sections.
    Gives a ValueError if both metadata and content are not present in one of the 2 formats.
    Format 1: ## metadata and ## content
    Format 2: METADATA and CONTENT
    Strips all leading and trailing newlines from the metadata string.
    The content string starts with the content delimiter.

    :param file_path: string of the file path which can be absolute or relative.
    :return: tuple, the metadata and content as two separate strings.
    """
def read_file_flex(file_path):
    """
    Reads the text from a file and splits it into the metadata and content sections if present.
    If no metadata is found, returns (None, complete_text).

    :param file_path: string of the file path which can be absolute or relative.
    :return: tuple, the metadata and content as two separate strings. If no metadata, returns (None, complete_text).
    """
def handle_overwrite_prompt(file_path, file_path_opfunc, verbose=True):
    """
    Handles user prompt for overwriting a file.

    :param file_path: string of the original file path.
    :param file_path_opfunc: string of the new file path.
    :param verbose: boolean for whether to print verbose messages. Default is True.
    :return: string of the path to the file that was kept.
    """
def manage_file_overwrite(original_path, suffix_new, overwrite, verbose=False):
    """
    Handle file overwriting based on the specified mode.
    
    :param original_path: string, the path to the original file.
    :param suffix_new: string, the suffix to be appended to the original filename for the new file.
    :param overwrite: string, the overwrite mode ('no', 'no-sub', 'replace', 'replace-sub', 'yes', 'prompt').
    :param verbose: boolean, whether to print verbose messages.
    :return: string, the final path of the file after applying overwrite logic.
    """
def write_complete_text(file_path, complete_text, suffix_new='_temp', overwrite='no', verbose=False):
    """
    Writes the complete text to a new file with a specified suffix and handles overwrite logic.

    :param file_path: string, the path to the original file.
    :param complete_text: string, the complete text to be written to the new file.
    :param suffix_new: string, the suffix to be appended to the original filename for the new file.
    :param overwrite: string, the overwrite mode. Default is "no".
    :param verbose: boolean, whether to print verbose messages. Default is False.
    :return: string, the path to the final file after applying overwrite logic.
    """
def write_metadata_and_content(file_path, metadata, content, suffix_new='_temp', overwrite='no', verbose=False):
    """
    Writes the metadata and content text to a new file with a specified suffix and handles overwrite logic.
    Insert 2 blank lines between the metadata and content sections if metadata is present or empty string.

    :param file_path: string, the path to the original file.
    :param metadata: string or None, the metadata section to be written to the new file, inclusive of '## metadata' or 'METADATA'.
    :param content: string, the content section to be written to the new file, inclusive of '## content' or 'CONTENT'.
    :param suffix_new: string, the suffix to be appended to the original filename for the new file.
    :param overwrite: string, the overwrite mode. Default is "no".
    :param verbose: boolean, whether to print verbose messages. Default is False.
    :return: string, the path to the final file after applying overwrite logic.
    """
### JSON (301 tokens)
def pretty_print_json_structure(json_file_path, level_limit=None, save_to_file=False):
    """
    Prints the structure of a JSON file and optionally saves it to a file with a '.pretty' extension.

    :param json_file_path: string of the path to the json file.
    :param level_limit: integer of the maximum level of nesting to print. None means no limit.
    :param save_to_file: boolean indicating whether to save the output to a file. defaults to true.
    :return: None.
    """
    def print_json_structure(data, indent=0, parent_key='', level=0):
def write_json_file_from_object(json_object, file_path, overwrite="no"):
    """ 
    Writes a JSON object to a file at the specified path.

    :param json_object: dictionary or list to be written as JSON.
    :param file_path: string of the path where the JSON file will be written.
    :param overwrite: string of either "yes" or "no" to determine if existing files should be overwritten. default is "no".
    :return: None.
    """
def read_json_object_from_file(file_path):  # consider moving to fileops
    """ 
    Reads a JSON object from a file at the specified path.

    :param file_path: string of the path to the JSON file to be read.
    :return: dictionary or list representing the JSON object read from the file.
    """
### MISC FILE (1,277 tokens)
def rename_file(file_path, new_filebase):
    """
    Renames the file base portion for the file given at the argument file path.

    :param file_path: string, the path to the file to be renamed.
    :param new_filebase: string, the new base name for the file without the extension.
    :return: string, the new file path after renaming, or an error if the operation fails.
    """
def rename_file_extension(file_path, new_extension):
    """
    Renames the file extension for the file given at the argument file path.

    :param file_path: string, the path to the file to be renamed.
    :param new_extension: string, the new extension for the file (including the dot).
    :return: string, the new file path after renaming, or an error if the operation fails.
    """
def delete_file(file_path):
    """
    Deletes a file at the specified file path.

    :param file_path: string, the path to the file to be deleted.
    :return: None. The function does not return any value.
    """
def delete_files_with_suffix(folder, suffixpat_include, verbose=False):  # omit unittests
    """
    Deletes all files in a given folder that end with a specified suffix.

    :param folder_path: string, the path to the folder where files are to be deleted.
    :param suffixpat_include: string, the suffix pattern of the files to be deleted.
    :param verbose: boolean, if True, the function will print verbose messages. Default is False.
    :return: None. The function does not return any value.
    """
def move_file(file_path, destination_folder): # cat 3a, unittest 3 - mocks
    """
    Moves a file to the specified destination folder.

    :param file_path: string, the path to the file to be moved.
    :param destination_folder: string, the path to the destination folder.
    :return: string, the new file path after moving, or an error if the operation fails.
    """
def move_files_with_suffix(source_folder, destination_folder, suffixpat_include, verbose=False): # omit unittest
    """
    Moves all files in a given folder that end with a specified suffix to the destination folder.

    :param source_folder: string, the path to the source folder where files are to be moved from.
    :param destination_folder: string, the path to the destination folder where files are to be moved to.
    :param suffixpat_include: string, the suffix pattern of the files to be moved.
    :param verbose: boolean, if True, the function will print verbose messages. Default is False.
    :return: list, the new file paths after moving, or an error if the operation fails.
    """
def tune_title(title):
    """
    Removes any special characters from the given title.

    :param title: string, the title from which special characters are to be removed.
    :return: string, the updated title with special characters removed.
    """
def create_full_path(title_or_path, new_suffix_ext, default_folder=None):
    """
    Creates a full file path from a given title or path, a new suffix extension, and an optional default folder.

    :param title_or_path: string, the title or path of the file.
    :param new_suffix_ext: string, the new suffix extension to be added to the file.
    :param default_folder: string, the default folder to be used if no folder is specified in title_or_path. Default is None.
    :return: string, the newly created full file path.
    """
def find_file_in_folders(file_path, folder_paths):
    """
    Searches for a file within a list of folder paths and returns the first match.

    :param file_path: string of the file name to search for.
    :param folder_paths: list of strings of folder paths where the file will be searched.
    :return: string of the full path to the file if found, otherwise None.
    """
def zip_files_in_folders(folder_paths, suffixpat_include, zip_file_path, include_subfolders=True):
    """
    Zips files in the specified folders that match the given suffix into a single zip file.

    :param folder_paths: list of strings, the paths to the folders where files will be zipped.
    :param suffixpat_include: string, the suffix pattern that included files must have.
    :param zip_file_path: string, the path where the single zip file will be created.
    :param include_subfolders: boolean, indicates whether to include files from subfolders.
    :return: None
    """
def compare_files_text(file1_path, file2_path):
    """
    Compares the content of two files.

    :param file1_path: string, the path to the first file to be compared.
    :param file2_path: string, the path to the second file to be compared.
    :return: boolean, True if the content of the files is exactly the same, False otherwise.
    """
def get_text_between_delimiters(full_text, delimiter_start, delimiter_end=None):
    """
    Extracts a substring from the given text between specified start and end delimiters.

    :param full_text: string of the text from which to extract the substring.
    :param delimiter_start: string of the delimiter indicating the start of the substring.
    :param delimiter_end: string of the delimiter indicating the end of the substring. If None, the end of the text is used. Default is None.
    :return: string of the extracted substring (inclusive of delimiter_start), or None if the start delimiter is not found.
    """
def check_if_duplicate_filename(filename, folder, exclude_suffix=True):
    """
    Checks if a filename already exists in a given folder, optionally excluding suffixes.

    :param filename: str, the filename to check for duplicates.
    :param folder: str, the path to the folder to search in.
    :param exclude_suffix: bool, whether to exclude suffixes when comparing filenames.
    :return: bool, True if a duplicate is found, False otherwise.
    """
### TIME AND TIMESTAMP (929 tokens)
def convert_seconds_to_timestamp(seconds):
    """
    Converts a given number of seconds into a timestamp in the format hh:mm:ss or mm:ss.

    :param seconds: integer or float representing the number of seconds to be converted.
    :return: string representing the timestamp in the format hh:mm:ss or mm:ss.
    """
def convert_timestamp_to_seconds(timestamp):
    """
    Converts a timestamp in the format hh:mm:ss or mm:ss into seconds.

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :return: integer representing the total number of seconds.
    """
def change_timestamp(timestamp, delta_seconds):
    """
    Changes a given timestamp by a specified number of seconds. Uncomment line in tune_timestamp

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :param delta_seconds: integer representing the number of seconds to change the timestamp by.
    :return: string representing the new timestamp after the change.
    """
def tune_timestamp(timestamp):
    """
    Converts a given timestamp to a standard format with respect to digits and leading zeros.

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :return: string representing the tuned timestamp or None if the input timestamp is None.
    """
def get_timestamp(line, print_line=False, max_words=8):
    """
    Extracts a timestamp from a given line of text.

    :param line: string representing the line of text to search for a timestamp.
    :param print_line: boolean indicating whether to print the line where the timestamp was found. Default is False.
    :param max_words: integer representing the maximum number of words allowed before and after the timestamp. Default is 5.
    :return: tuple containing the extracted timestamp as a string and its index in the line, or (None, None) if no valid timestamp is found.
    """
def get_current_datetime_humanfriendly(timezone='America/Los_Angeles', include_timezone=True):
    """
    Returns the current date and time as a string for a given timezone, optionally including the timezone abbreviation and UTC offset.

    :param timezone: string representing the timezone to use for the current time.
    :param include_timezone: boolean indicating whether to include the timezone abbreviation and UTC offset in the returned string.
    :return: string representing the current date and time in the specified timezone, optionally followed by the timezone abbreviation and UTC offset.
        """
def get_current_datetime_filefriendly(location='America/Los_Angeles', include_utc=False):
    """
    Returns the current date and time as a filename-friendly string for a given timezone, optionally including only the UTC offset.

    :param location: string representing the timezone to use for the current time.
    :param include_utc: boolean indicating whether to include the UTC offset in the returned string.
    :return: string representing the current date and time in the specified timezone, formatted for filenames, optionally followed by the UTC offset.
        """
def convert_to_epoch_seconds(datetime_flex, timezone='America/Los_Angeles', verbose=False):
    """
    Converts a human-readable time to the number of seconds since the Unix epoch (1970-01-01 00:00:00 UTC).
    The function assumes the input format is 'YYYY-MM-DD_HH:MM:SS [optional UTC offset] [optional timezone]', 
    where the date and time are separated by an underscore or space,
    and the time may be followed by another underscore or space and a UTC offset string, and optionally a timezone string.

    :param datetime_flex: string representing the time, which can be in 'YYYY-MM-DD_HH:MM:SS' format or 'YYYY-MM-DD HH:MM:SS [UTC offset] [timezone]'.
    :param default_timezone: string representing the default timezone if not specified in datetime_flex. Defaults to 'America/Los_Angeles'.
    :return: float representing the number of seconds since the Unix epoch.
    """
def get_elapsed_seconds(start_time_epoch_seconds):
    """
    Calculates the time elapsed since the start_time and returns it in seconds.

    :param start_time: float, the start time in seconds since the epoch (as returned by time.time())
    :param return_format: string ('minutes' or 'timestamp') for the return value format - 'timestamp' for H:MM:SS or minutes with one decimal place
    :return: integer of the number of seconds
    """
### TIMESTAMP LINKS (340 tokens)
def remove_timestamp_links_from_content(content):
    """
    Removes markdown timestamp links from the content and returns the modified content.

    :param content: string of the content from which to remove markdown timestamp links.
    :return: string of the content with markdown timestamp links removed.
    """
def remove_timestamp_links(file_path):
    """
    Removes markdown timestamp links and overwrites the file.

    :param file_path: string of the path to the original file.
    :return: none.
    """
def generate_timestamp_link(base_link, timestamp):
    """
    Helper function to generate a timestamp link for a given base link and timestamp.
    It uses a dictionary to map domains to their respective timestamp formats.
    For Vimeo, the timestamp is converted to milliseconds.
    
    :param base_link: string of the base URL to which the timestamp will be appended.
    :param timestamp: string of the timestamp to be converted and appended to the base URL.
    :return: string of the complete URL with the timestamp appended in the appropriate format.
    """
def add_timestamp_links_to_content(content, base_link):
    """
    Adds timestamp links to the content using the provided base link.

    :param content: string of the content where timestamp links will be added.
    :param base_link: string of the base URL to which the timestamp will be appended.
    :return: string of the content with timestamp links added.
    """
def add_timestamp_links(file_path):
    """
    Adds markdown timestamp links and overwrites the file.

    :param file_path: string, the path to the file where timestamp links will be added.
    :return: none
    """
### FIND AND REPLACE (453 tokens)
def count_num_instances(file_path, find_str):
    """
    Counts the number of instances of a specific string in the text of the file.
    Is case-sensitive.

    :param file_path: string, the path to the file where the search will be performed.
    :param find_str: string, the string to find in the file content.
    :return: int, the number of instances found, or zero if no instances are found.
        """
def find_and_replace_pairs(file_path, find_replace_pairs, use_regex=False):
    """
    Finds and replaces multiple specified strings or regex patterns in the file and overwrites the original file.

    :param file_path: string, the path to the file where the find and replace operations will be performed.
    :param find_replace_pairs: list of tuples, each containing a string or regex pattern to be found and a string to replace it with.
    :param use_regex: boolean for whether to use regex patterns for finding. Default is False (use exact string matching).
    :return: int, the total number of replacements made.
    """
def parse_csv_for_find_replace(csv_file):
    """
    Parses a CSV file to extract find and replace pairs.
    Returns a list of the find_
    """
def find_and_replace_from_csv(folder_path, find_replace_csv, suffixpat_include=None, verbose=False):
    """
    Applies find and replace operations on all files in a specified folder based on pairs defined in a CSV file.
    Overwrite is fixed at 'yes' so you have to copy the files before running.
    IMPORTANT csv file cannot be in the same folder if suffixpat_include=None
    Good practice is to always include a suffixpat_include even if those are the only type of file in the folder.

    :param folder_path: string, the path to the folder where the files are located.
    :param find_replace_csv: string, the path to the CSV file containing find and replace pairs.
    :param suffixpat_include: string, the suffix pattern that included files must have. If None, all files will be processed.
    :param verbose: boolean, if True prints verbose messages.
    :return: None
    """
### HEADINGS (827 tokens)
def get_heading_level(heading):
    """
    Determines the level of a markdown heading.

    :param heading: string, the markdown heading including '#' characters.
    :return: int, the level of the heading.
    """
def get_heading_pattern(heading):
    """
    Creates a regex pattern to match a heading and its content, including subheadings.

    :param heading: string, the markdown heading including '#' characters.
    :return: compiled regex pattern or None if heading is empty
    """
def find_heading_text(full_text, heading):
    """
    Finds the heading text, including its subheadings, inclusive of the heading itself.

    :param text: string, the text to search in.
    :param heading: string, the markdown heading to find.
    :return: tuple (start_index, end_index) or None if not found.
    """
def get_heading(file_path, heading):
    """
    Extracts the markdown heading and its associated text from a file, including any subheadings of equal or lower order.
    Uses the complete text and does not parse the metadata and content sections.

    :param file_path: string, the path to the file to be read.
    :param heading: string, the markdown heading to be extracted, including the '#' characters and the following space.
    :return: string, the markdown heading and its associated text, including any subheadings of equal or lower order.
    """
def set_heading(file_path, new_text, heading):
    """
    Sets the heading and following text associated with a markdown heading and overwrites the file.
    Replaces if the heading already exists. Adds if it does not exist.
    New line characters must be included in the new_text (e.g., "\nHere's new text\n\n").
    
    :param file_path: string, the path to the file where the heading text will be set.
    :param new_text: string, the new text to be associated with the markdown heading, inclusive of newlines.
    :param heading: string, the markdown heading whose text will be set, including the '#' characters and the following space.
    :return: None
    """
def delete_heading(file_path, heading):
    """
    Deletes the specified markdown heading and its following text, including subheadings, and overwrites the file.
    If the heading does not exist, a warning is issued and no action is taken.

    :param file_path: string of the path to the file from which the heading will be deleted.
    :param heading: string of the markdown heading to be deleted, including the '#' characters and the following space.
    """
def append_heading_to_file(source_file_path, target_file_path, heading, include_filename=True):
    """
    Appends the text under a specified heading from a source file to a target file, optionally including the source filename as a heading.

    :param source_file_path: string of the path to the source file.
    :param target_file_path: string of the path to the target file where the text will be appended.
    :param heading: string of the markdown heading to be appended.
    :param include_filename: boolean indicating whether to include the source filename as a heading. Defaults to True.
    :return: string of the appended text or None if the heading is not found in the source file.
    """
def create_new_file_from_heading(file_path, heading, suffix_new='_headingonly', remove_heading=False):
    """
    Extracts text under a specified heading from a file and writes it to a new file with a specified suffix.

    :param file_path: string of the path to the file.
    :param heading: string of the markdown heading to be processed.
    :param suffix_new: string of the suffix to be appended to the new file. Defaults to "_headingonly".
    :param remove_heading: boolean indicating whether to remove the heading from the extracted text. Defaults to False.
    :return: string of the path to the newly created file.
    """
### METADATA (762 tokens)
def set_metadata_field(metadata, field, value):
    """
    Sets or updates a metadata field with a given value.

    :param metadata: string, the metadata from which a metadata field is to be set or updated.
    :param field: string, the metadata field to be set or updated without the : and space.
    :param value: string, the value to be set for the metadata field.
    :return: string, the updated metadata with the set or updated metadata field.
    """
def remove_metadata_field(metadata, field):
    """
    Removes a specified metadata field from the metadata.

    :param metadata: string, the metadata from which a metadata field is to be removed.
    :param field: string, the metadata field to be removed.
    :return: string, the updated metadata with the removed metadata field.
    """
def create_initial_metadata():
    """
    Creates an initial metadata for a file.

    :return: string, the initial metadata for a file.
    """
def set_last_updated(metadata, new_last_updated_value, use_today=True):
    """
    Updates the 'last updated' metadata field in the metadata with a new value.

    :param metadata: string, the metadata from which the 'last updated' metadata field is to be updated.
    :param new_last_updated_value: string, the new value for the 'last updated' metadata field.
    :param use_today: boolean, if True, today's date is prepended to the new_last_updated_value. Default is True.
    :return: string, the updated metadata with the new 'last updated' value.
    """
def read_metadata_field_from_file(file_path, field):
    """
    Reads a specific metadata field from a file.

    :param file_path: string, the path to the file to be read.
    :param field: string, the metadata field to be read from the file.
    :return: tuple, the line number of the field and the value of the field.
    """
def set_metadata_fields_from_csv(folder_path, csv_file_path, suffix_extension):
    """
    Sets metadata fields for all files in a folder based on a CSV file.

    :param folder_path: string of the path to the folder containing the files.
    :param csv_file_path: string of the path to the CSV file with metadata fields and values.
    :param suffix_extension: string of the file extension to be appended to file bases.
    :return: None, but prints the number of files processed successfully and the total in the CSV excluding empty rows.
    """
def create_csv_from_fields(folder_path, fields):
    """
    Generates a CSV file of input fields from all markdown files in a folder.
    Fields can be 2 formats, 1) generic, usually metadata (ending with a ':') or 2) markdown headings (starting with a '#').
    Generic fields extract single-line values, while heading fields capture all content under the heading.

    :param folder_path: string, the path to the folder containing the markdown files.
    :param fields: list, the fields to be extracted from the markdown files.
    :return: string of the path to the created csv file.
    """
def create_csv_matrix_from_triples(triples_text, target_file_path):
    """
    Converts multiline text of triples into a csv matrix file where each entry is the number for that row and column.

    :param triples_text: string of multiline text containing rows of data separated by newlines, each row containing two strings and a number separated by commas.
    :param target_file_path: string of the path to the target csv file.
    :return: string of the path to the created csv file.
    """
## primary/transcribe.py (4,531 tokens)
### YOUTUBE (866 tokens)
def download_mp3_from_youtube(url, output_title='downloaded_audio'):
    """ 
    Downloads an audio file from a YouTube URL and saves it as an mp3 file. Uses yt_dlp package.

    :param url: string of the YouTube URL from which to download the audio.
    :param output_title: string of the title to save the downloaded mp3 file as. defaults to 'downloaded_audio'.
    :return: string of the path to the saved mp3 file.
    """
def get_youtube_title_length(url):
    """ 
    Retrieves the title and duration of a youtube video in a formatted timestamp. Uses yt_dlp package.

    :param url: string of the youtube url to retrieve information from.
    :return: tuple containing the video title and its duration as a string in a formatted timestamp.
    """
def download_link_list_to_mp3s(links, audio_inbox_path="data/audio_inbox"):  # NO CALLERS (3-3 RT)
    """
    Downloads a list of youtube links as mp3 files to a specified directory and stores the link-title pairs. Uses yt_dlp package.
    Calls download_mp3_from_youtube

    :param links: list of youtube links to be downloaded.
    :param audio_inbox_path: string of the directory path where the audio files will be saved.
    :return: dictionary mapping each youtube link to its corresponding title.
    """
def download_youtube_subtitles_url(subtitle_url): # DS, cat 1, omit unittests since called by next function
    """
    Downloads and extracts subtitle text from a given YouTube subtitle URL.
    Helper function to that is called from get_youtube_subtitles
    
    :param subtitle_url: string of the url from which subtitles are to be downloaded.
    :return: string of the extracted subtitle text, spaces between segments and stripped of new lines.
    """
def get_youtube_subtitles(url):
    """
    Retrieves English subtitles for a given YouTube video URL if available. Uses yt_dlp package.
    
    :param url: string of the youtube video url.
    :return: subtitles as a string if found, otherwise None.
    """
def get_youtube_all(url):
    """
    Retrieves all available information from a YouTube video URL, including title, length, chapters, description, and transcript. Uses yt_dlp package.
    
    :param url: string of the youtube video url.
    :return: dictionary with video details or None if the URL is invalid.
    """
def is_valid_youtube_url(url):
    """ 
    Determine if a string of url is a valid YouTube URL by attempting to fetch video info using the yt_dlp package.

    :param url: string of url to be validated.
    :return: boolean where true if the url is valid, false otherwise.
    """
def create_youtube_md(url, title_or_path=None):  # unittests 3 APICALL + 1 APIMOCK
    """
    Generates a markdown file containing metadata, chapters, description, and transcript from a YouTube video.

    :param url: string of the url to be processed.
    :param title_or_path: string of the title or path for the markdown file, defaults to None.
    :return: string of the path to the created markdown file.
    """
def create_youtube_md_from_file_link(md_file_path):
    """
    Creates a YouTube markdown file from a given file path by extracting the YouTube link from the file's metadata.
    
    :param md_file_path: string of the path to the markdown file containing the YouTube link in its metadata.
    :return: string of the path to the created YouTube markdown file.
    """
def extract_feature_from_youtube_md(yt_md_file_path, feature):
    """
    Extracts a specified feature from a YouTube markdown file and returns it as a string.

    :param yt_md_file_path: string of the path to the markdown file from which the feature is to be extracted.
    :param feature: string of the feature to be extracted (e.g., 'chapters', 'description', 'transcript').
    :return: string of the extracted text under the specified feature
    """
### DEEPGRAM AND JSON (1,190 tokens)
def test_deepgram_client():  # omit unittests
    """
    Tests the Deepgram client initialization with the provided API key and prints a success or failure message.
    Raises ValueError if test fails.
    """
def get_media_length(file_path_or_url):
    """
    Retrieves the length (duration) of a media file or a YouTube video.
    For a local file, it returns the duration in seconds.
    For a YouTube video, it returns the duration in our tuned timestamp format.

    :param file_path_or_url: Path to a local media file or a URL to a YouTube video.
    :return: length (duration) of the media in seconds (for local files) or in our tuned timestamp format (for YouTube videos).
    """
def add_link_to_json(json_file_path, link):
    """ 
    Add a hyperlink to the JSON file under the 'metadata' section.

    :param json_file_path: string, the path to the JSON file to be modified.
    :param link: string, the hyperlink to be added to the JSON file.
    :return: tuple, the path to the modified JSON file and None if successful, or None and an exception if an error occurs.
    """
def get_link_from_json(json_file_path):
    """ 
    Retrieve the hyperlink from the 'metadata' section of a JSON file.

    :param json_file_path: string, the path to the JSON file from which the hyperlink is to be retrieved.
    :return: string or None, the hyperlink if found in the JSON file's 'metadata' section, otherwise None.
    """
def transcribe_deepgram(audio_file_path, model):
    """ 
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription, accpets deepgram api call model or our suffix version (see below).
    :return: a dictionary containing the transcription results.
    """
def transcribe_deepgram_sdk_prerecorded(audio_file_path, model):
    """
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model, utilizing the SDK.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :return: path to the JSON file containing the transcription results.
    """
def transcribe_deepgram_callback(audio_file_path, model, callback_url):
    """
    Transcribes the given audio file using the specified Deepgram model asynchronously with a callback URL.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :param callback_url: URL to which Deepgram will send the transcription results.
    :return: Request ID from Deepgram indicating that the file has been accepted for processing.
    """
def transcribe_deepgram_callback2(audio_file_path, model, callback_url):
    """
    Transcribes the given audio file using the specified Deepgram model asynchronously with a callback URL.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :param callback_url: URL to which Deepgram will send the transcription results.
    :return: Request ID from Deepgram indicating that the file has been accepted for processing.
    """
def transcribe_deepgram_OLD_fixhang(file_path, timeout_duration=1*60*60):
def get_summary_start_seconds(data, index):
    """ 
    Retrieves the start time in seconds of a word from the transcription data at the given index.

    :param data: dictionary of the transcription data.
    :param index: integer of the index of the word to find the start time for.
    :return: integer of the start time in seconds of the specified word, rounded down to the nearest whole number.
    """
def format_feature_segment(feature, segment, data):
    """
    Formats a segment of a feature with a timestamp and additional info.

    :param feature: string, the feature being extracted.
    :param segment: dict, the segment of the feature to be formatted.
    :param data: dict, the JSON data from the Deepgram file.
    :return: string, the formatted segment.
    """
def extract_feature_from_deepgram_json(json_file_path, feature):
    """
    Extract a specific feature section from a Deepgram JSON file and return it as a string.

    :param json_file_path: string of the path to the JSON file from which the feature is to be extracted.
    :param feature: string of the feature of the section to be extracted.
    :return: string of the extracted text under the specified feature, preceded by the feature itself (no pound signs) and a blank line.
    """
def validate_transcript_json(json_file_path):
    """
    Validates the structure of a JSON file to ensure it contains specific keys and types.

    :param json_file_path: string of the path to the JSON file to be validated.
    :return: boolean, True if the JSON structure is as expected, False otherwise.
    """
def set_various_transcript_headings(file_path, feature, source):
    """
    Sets the transcript heading in a file based on the extracted feature from a specified source.

    :param file_path: string of the path to the file where the heading is to be set.
    :param feature: string of the feature to extract and use as the heading.
    :param source: string of the source from which to extract the feature ('deepgram' or 'youtube').
    :return: None.
    """
### NUMERAL CONVERT (1,423 tokens)
def extract_context(line, match, context_radius):
    """ 
    Extracts a context window around a regex match within a string of text.

    :param line: string of text containing the match.
    :param match: regex match object containing the start and end positions of the match within the line.
    :param context_radius: integer specifying the number of words around the match to include in the context window.
    :return: string of text representing the context window around the match.
    """
def print_num_exception(match_str, line_number, num_metadata_lines, printed_exceptions, exception_type, line):
    """ 
    Prints a message for numbers that are excluded from conversion and records the message.

    :param match_str: the string that matches the number to be excluded from conversion.
    :param line_number: the current line number in the file being processed.
    :param num_metadata_lines: the number of metadata lines in the file to adjust the actual line number.
    :param printed_exceptions: a list of exception messages that have already been printed.
    :param exception_type: the type of exception to be printed.
    :param line: the current line of text being processed.
    :return: None, but updates the printed_exceptions list with the new exception message if it hasn't been printed before.
    """
def get_previous_word(substring, start_index):
    """ 
    Finds the word in a string that precedes the given start index.

    :param substring: the string from which to extract the previous word.
    :param start_index: the index in the string to start searching backward from.
    :return: the word found before the start index, or an empty string if no word is found.
    """
def previous_word_exception(word, common_english_vocab, additional_exception_words):
    """ 
    Determines if a word is an exception based on its presence in additional exceptions or English vocabulary.

    :param word: the word to check for exception status.
    :param common_english_vocab: a set of common English words to compare against.
    :param additional_exception_words: a set of words that are always considered exceptions.
    :return: True if the word is an exception, False otherwise.
    """
def convert_num_line_lowercase(line, num, num_str, line_number, num_metadata_lines, printed_exceptions, common_english_vocab):
    """ 
    Converts numbers in a line of text to their lowercase word equivalents, skipping exceptions.

    :param line: The line of text in which to convert numbers.
    :param num: The numerical value to convert to words.
    :param num_str: The string representation of the number to find in the line.
    :param line_number: The current line number in the text being processed.
    :param num_metadata_lines: The number of metadata lines in the text before the content.
    :param printed_exceptions: A set to record exceptions that have been printed.
    :param common_english_vocab: A set of common English vocabulary words.
    :return: A tuple containing the modified line and the total number of substitutions made.
    """
def convert_num_line_capitalization(line, num, num_str):
    """ 
    Capitalize the numeral word at the beginning of a sentence or after punctuation.

    :param line: the line of text in which to perform capitalization.
    :param num: the numerical value to convert to words.
    :param num_str: the string representation of the number to find in the line.
    :return: a tuple containing the modified line and the total number of substitutions made.
    """
def skip_speaker_line_with_timestamp(line):
    """ 
    Determine if a line contains a single timestamp with max_words before the timestamp less that get_timestamp default val (8) and is therefore a speaker line to skip.

    :param line: The line of text to be checked for a timestamp.
    :return: boolean where True if a timestamp is found, otherwise False.
    """
def convert_num_lines(lines, num, num_str, num_metadata_lines, verbose, printed_exceptions):
    """ 
    Converts numbers in lines of text to their word equivalents, handles capitalization, and skips lines with timestamps.
    Takes both num and num_str as separate parameters to provide flexibility in how the function is called.
    This design allows the caller to specify the string representation of the number 1 that should be searched for within the text lines,
    which may not always be a straightforward string conversion of num.
    For example, num could be an integer, but num_str could be a formatted string that represents the number
    in a specific way within the text (e.g., "001" instead of "1", or "1st" for the ordinal form).
    
    :param lines: list of text lines to process.
    :param num: the numerical value to convert to words.
    :param num_str: the string representation of the number to find in the lines.
    :param num_metadata_lines: the number of metadata lines in the document to adjust line numbering for output.
    :param verbose: boolean indicating whether to print the conversion output.
    :param printed_exceptions: list to record any exceptions encountered during processing.
    :return: tuple containing the list of processed lines and the total number of substitutions made.
    """
def convert_numbers_in_content(content, num_limit, additional_numbers, num_metadata_lines, print_output):
    """ 
    Converts numerical values in text content to their word equivalents, excluding lines with timestamps.

    :param content: string containing the text content to be processed.
    :param num_limit: integer representing the upper limit for numbers to convert.
    :param additional_numbers: list of additional numbers to be converted outside the standard range.
    :param num_metadata_lines: integer representing the number of metadata lines in the content.
    :param print_output: boolean indicating whether to print the conversion output.
    :return: tuple containing the converted content as a string and the total number of substitutions made.
    """
def convert_ordinals_in_content(content, punct_capitalization):
    """ 
    Converts ordinal numbers in a string of text to their word equivalents and capitalizes words following specified punctuation.

    :param content: string of text containing ordinal numbers and punctuation.
    :param punct_capitalization: list of punctuation characters after which the following word should be capitalized.
    :return: string of text with ordinal numbers converted and words capitalized as specified.
    """
def convert_nums_to_words(file_path, verbose=False):
    """
    Converts numerals in the content of a file to their corresponding words, appends a specified suffix to the filename, and creates a new file with the converted content.

    :param file_path: string of the path to the original file.
    :param verbose: boolean for printing verbose messages. Defaults to False.
    :return: string of the path to the newly created file with the converted content.
    """
### SPEAKER NAMES (509 tokens)
def read_speaker_names_from_json(json_file_path):
    """ 
    Reads speaker names from a JSON file's metadata, which have been inserted by us and are not in the raw deepgram json files.

    :param json_file_path: string of the path to the JSON file.
    :return: list of speaker names if they exist, otherwise an empty list.
    """ 
def write_speaker_names_to_json(json_file_path, speaker_names, verbose=False):
    """ 
    Writes speaker names to a JSON file's metadata. Overwrites file.

    :param json_file_path: string of the path to the JSON file.
    :param speaker_names: list of strings containing speaker names.
    :return: None.
    """ 
def find_unassigned_speakers(md_file_path, verbose=False):
    """ 
    Identifies speakers in the markdown file who do not have assigned names.
    This is determined by if the line has a valid timestamp and then looking for 'Speaker X' before the timestamp.

    :param md_file_path: string of the path to the markdown file.
    :return: list of strings of unassigned speaker names, or None if all speakers are assigned.
    """
def propagate_speaker_names_throughout_md(md_file_path, input_speaker_names=None):
    """
    Propagates speaker names throughout a markdown file based on provided input names or existing assignments.

    :param md_file_path: string of the path to the markdown file.
    :param input_speaker_names: list of tuples with speaker numbers and names, if available.
    :return: list of tuples with speaker numbers and names after propagation.
    """
def iterate_input_speaker_names(md_file_path, input_speaker_names=None):
    """
    Iterates over input speaker names and updates the markdown file until the user decides to exit.

    :param md_file_path: string of the path to the markdown file.
    :param input_speaker_names: list of tuples with speaker numbers and names, if available.
    :return: list of tuples with speaker numbers and names after all iterations.
    """
def assign_speaker_names(md_file_path):
    """
    Assigns speaker names to markdown file by reading from a corresponding JSON file, updating, and writing back to the json if changed.
    Prompts the user iteratively through assigning the names.
    
    :param md_file_path: string of the path to the markdown file.
    :return: None
    """
### TRANSCRIBE WRAPPER (537 tokens)
def create_transcript_md_from_json(json_file_path, combine_segs=True):
    """
    Creates a markdown transcript from a JSON file containing Deepgram transcription data.
    If combine_segs is True, combines consecutive segments from the same speaker.

    :param json_file_path: string of the path to the json file containing transcription data.
    :param combine_segs: boolean indicating whether to combine consecutive segments from the same speaker.
    :return: string of the path to the created markdown file or None if the json file is not valid.
    """
def process_deepgram_transcription(title, link, model, audio_inbox_path="data/audio_inbox"):  # unittests 1 TEMP SKIPPED
    """
    Processes a Deepgram transcription from a YouTube video link by downloading the audio, transcribing it, and creating a markdown transcript.

    :param title: the title of the video used to name the downloaded audio file.
    :param link: the YouTube link to the video to be transcribed.
    :param model: the Deepgram model used for transcription.
    :param audio_inbox_path: the directory path where the audio file will be downloaded.
    :return: the path to the created markdown file or None if transcription fails.
    """
def process_deepgram_transcription_from_audio_file(audio_file_path, link, model):  # unittests 1 TEMP SKIPPED
    """ 
    Transcribes an audio file using the Deepgram service, adds the YouTube link to the transcription, creates a markdown transcript, and assigns speaker names.

    :param audio_file_path: string of the path to the audio file to be transcribed.
    :param link: string of the youtube link to be added to the transcription json.
    :param model: string of the deepgram model to be used for transcription.
    :return: string of the path to the markdown file with the completed transcription or None if transcription fails.
    """
def process_multiple_videos(videos_to_process, model='nova-2-general', bool_youtube=True):  # unittests 1 MOCK
    """
    Processes multiple videos by transcribing them and creating YouTube markdown files if bool_youtube is True.

    :param videos_to_process: list of tuples containing the title and link of each video to be processed.
    :param model: string of the deepgram model to be used for transcription. Defaults to 'enhmeet' (deepgram enhanced-meeting) model.
    :param bool_youtube: boolean indicating whether to create YouTube markdown files. Defaults to True.
    :return: None
    """
## primary/llm.py (10,101 tokens)
### PRINT AND TOKENS (918 tokens)
def pretty_print_function(messages, tools, print_prompts=False, print_input=True, verbose=False):
    """
    Prints messages with role-specific colors and separates function details for clarity.

    :param messages: list of dictionaries containing message role and content
    :params tools: list of tools, each containing function details, passed to pretty_print_function_descriptions
    :param print_prompts: boolean of whether to print the system prompt and function parameter descriptions, defaults to False
    :param print_input: boolean of whether to print the user input, defaults to True
    :return: a list of the print strings as [print_str_prompts, print_str_input, print_str_responses]
    """
def pretty_print_function_descriptions(tools, print_color):
    """
    Print descriptions of functions and their properties from a list of tools.

    :param tools: a list of tools, each containing function details
    :return: a string of function names and descriptions, including properties
    """
def count_tokens(input_string):  # no unittests
    """
    Counts the number of tokens in a given string using the 'cl100k_base' encoding.

    :param input_string: string of text to be tokenized.
    :return: integer representing the number of tokens in the input string.
    """
def cost_llm_on_file(file_path, prompt, model, token_cost_dict, verbose=False, chunking_function=None, chunking_function_args=(), output_tokens_ratio=1, output_tokens_fixed=0):  # no unittests
    """
    Calculates the cost of processing a file using a language model, based on the number of input and output tokens.

    :param file_path: string of the path to the file to be processed.
    :param prompt: string of the prompt to be used for the language model.
    :param model: string of the name of the language model to be used.
    :param token_cost_dict: dictionary containing the cost per token for the input and output of the model.
    :param chunking_function: function to be used for chunking the file, defaults to None.
    :param chunking_function_args: tuple of arguments to be passed to the chunking function, defaults to an empty tuple.
    :param output_tokens_ratio: ratio of input tokens to output tokens, defaults to 1.
    :param output_tokens_fixed: fixed number of output tokens per chunk, defaults to 0.
    :return: tuple of total input cost, total output cost, and total cost.
    """
    def default_chunking(file_path):
def cost_llm_on_corpus(corpus_path, prompt, model, token_cost_dict, verbose=False, suffix_include=None, suffix_exclude=None, include_subfolders=False, chunking_function=None, chunking_function_args=(), output_tokens_ratio=1, output_tokens_fixed=0):
    """
    Calculates the cost of processing a corpus using a language model, based on the number of input and output tokens.

    :param corpus_path: string of the path to the corpus to be processed.
    :param prompt: string of the prompt to be used for the language model.
    :param model: string of the name of the language model to be used.
    :param token_cost_dict: dictionary containing the cost per token for the input and output of the model.
    :param chunking_function: function to be used for chunking the file, defaults to None.
    :param chunking_function_args: tuple of arguments to be passed to the chunking function, defaults to an empty tuple.
    :param output_tokens_ratio: ratio of input tokens to output tokens, defaults to 1.
    :param output_tokens_fixed: fixed number of output tokens per chunk, defaults to 0.
    :param suffix_include: string of the suffix that included files must have, defaults to None.
    :param suffix_exclude: string of the suffix that files must not have to be included, defaults to None.
    :param include_subfolders: boolean indicating whether to include files from subfolders, defaults to False.
    :return: tuple of total input cost, total output cost, and total cost for the entire corpus.
    """
def add_token_counts_to_headings(text):
    """
    Adds token counts to markdown headings in the given text.

    :param text: string, the text content to process.
    :return: string, the text with token counts added to headings.
    """
### SPLIT FILES (914 tokens)
def get_line_numbers_with_match(file_path, match_str):
    """
    Retrieve line numbers from a file where the line matches a given string exactly after stripping.

    :param file_path: path to the file to be searched
    :param match_str: string of text to match on each line
    :return: list of line numbers where the match_str is found
    """
def get_speaker_segments(file_path, skip_string='SKIPQA'):
    """
    Extract segments from a file that do not contain a specific skip string, or all segments if skip string is None.

    :param file_path: string of the path to the file to be processed
    :param skip_string: string of the substring used to identify segments to skip, or None to include all segments
    :return: list of segments without the skip string, or all segments if skip string is None
    """
def count_segment_tokens(file_path, skip_string='SKIPQA'):
    """
    Count tokens in each segment of a file and provide token statistics.

    :param file_path: string of the path to the file to be processed
    :param skip_string: string of the substring used to identify segments to skip
    :return: tuple containing (list of segments, list of token counts)
    """
def plot_segment_tokens(file_path):
    """
    Create a horizontal bar chart plot of token counts for each segment and save it as a PNG file.

    :param file_path: string of the path to the file to be processed
    :return: string of the path to the saved PNG file
    """
def group_segments_select_speaker(segments, speaker):
    """
    Groups consecutive segments not containing the specified speaker's name and selects segments where the speaker's name is found before the timestamp.
    Calls get_timestamp from fileops.py to determine if the first line in a segment is a speaker line.

    :param segments: list of text segments to be processed
    :param speaker: string of the speaker's name to select segments
    :return: list of text segments where the speaker's name is found before the timestamp
    """
def group_segments_token_cap(segments, token_cap=2000):
    """
    Groups consecutive segments without exceeding the token_cap, without splitting segments.
    Includes segments that exceed the token_cap as individual blocks.

    :param segments: list of text segments to be processed
    :param token_cap: integer of maximum number of tokens, using words = .75 tokens
    :return: list of grouped text segments without exceeding the token_cap, including oversized segments as individual blocks
    """
def split_file_select_speaker(file_path, speaker, skip_string='SKIPQA', suffix_new='_blocks'):
    """
    Add block delimiters to a file, with a block for every segment by the selected speaker and other segments grouped together.

    :param file_path: path to the file to be processed
    :param speaker: the speaker whose sections will be delimited
    :param skip_string: string to identify speaker segments to skip
    :param suffix_new: suffix for the new file with block delimiters
    :return: file_path of new file with separator delimiters ("---") with suffix_new='_blocks' by default
    """
def split_file_every_speaker(file_path, skip_string=None, suffix_new='_blocks'):
    """
    Add block delimiters to a file with one block per speaker segment regardless of speaker.

    :param file_path: path to the file to be processed
    :param skip_string: string to identify speaker segments to skip
    :param suffix_new: suffix for the new file with block delimiters
    :return: file_path of new file with separator delimiters ("---") with suffix_new='_blocks' by default
    """
def split_file_token_cap(file_path, token_cap, skip_string='SKIPQA', suffix_new='_blocks'):
    """
    Add block delimiters to a file with one block per speaker segment regardless of speaker.

    :param file_path: path to the file to be processed
    :param token_cap: integer of maximum number of tokens, using words = .75 tokens
    :param skip_string: string to identify speaker segments to skip
    :param suffix_new: suffix for the new file with block delimiters
    :return: file_path of new file with separator delimiters ("---") with suffix_new='_blocks' by default
    """
### OPENAI LLM (371 tokens)
def test_openai_chat(model=OPENAI_MODEL):# DS, cat 5, unittests 2 APIMOCK
    """
    Sends a predefined message to the OpenAI chat API and prints the response.

    :param model: string of the model name to be used for the chat completion request
    :return: None
    """
def openai_chat_completion_request(messages, tools=None, tool_choice=None, model=OPENAI_MODEL):  # APIMOCK unittests 2
    """
    Send a chat completion request to the OpenAI API with the provided messages and optional tools and tool choice.

    :param messages: a list of message dictionaries to send in the chat completion request
    :param tools: optional list of tools to include in the request
    :param tool_choice: optional tool choice to include in the request
    :param model: the model to use for the chat completion request
    :return: the response object from the OpenAI API request
    """
def simple_openai_chat_completion_request(prompt, model):  # no unittests
def openai_function_call(fcall_prompt, content, tools, model=OPENAI_MODEL, verbose=False):  # APIMOCK unittests 3
    """
    Sends a prompt and content to the OpenAI LLM and returns the assistant's message.

    :param fcall_prompt: string of the system's prompt to initiate the conversation
    :param content: string of the user's content to process
    :param tools: list of dictionaries containing tool configurations
    :param model: string specifying the OpenAI model to use
    :param verbose: boolean indicating whether to print detailed response text
    :return: string of the assistant's message from the LLM response
    """
### ANTHROPIC LLM (250 tokens)
def anthropic_chat_completion_request(messages, model=ANTHROPIC_MODEL, system=None, max_tokens=4096, temperature=0.7):
    """
    Make a chat completion request to Anthropic's API.

    :param messages: List of message objects representing the conversation
    :param model: The model to use for the completion
    :param system: System message to set the behavior of the assistant
    :param max_tokens: Maximum number of tokens to generate (default: 4096)
    :param temperature: Controls randomness in the output (0 to 1, default: 0.7)
    :return: The generated message content or None if an error occurs
    """
def simple_anthropic_chat_completion_request(prompt, model=ANTHROPIC_MODEL):
    """
    Make a simple chat completion request to Anthropic's API.

    :param prompt: String containing the user's prompt or message
    :param model: String specifying the Anthropic model to use (default: "claude-3-opus-20240229")
    :return: String containing the generated message content, or an error message if the request fails
    """
### LLM PROCESSING (1,523 tokens)
def llm_process_block(block, prompt, provider="openai"):
    """
    Processes a single block of text with a given prompt using the OpenAI chat completion API.

    :param block: string of the text block to be processed.
    :param prompt: string of the prompt to use for the chat completion request.
    :param provider: string indicating the LLM provider (default is "openai").
    :return: string of the processed text block or None if no valid response is received.
    """
def llm_process_file_blocks(blocks_file_path, prompt, suffix_new, mode, provider="openai", retain_delimiters=False):
    """
    Processes blocks of text in a file using a specified prompt and operation mode, then writes the processed content back to the file.

    :param blocks_file_path: string of the path to the file containing text blocks
    :param prompt: string of the prompt to use for processing each text block
    :param suffix_new: string of the suffix to append to the file when saving the new content
    :param mode: string of the operation mode ('replace' or 'append') to handle the processed blocks
    :param provider: string indicating the LLM provider (default is "openai")
    :param retain_delimiters: boolean indicating whether to retain the original block delimiters in the new content
    :return: the path to the file with the updated content
    """
def scall_replace(blocks_file_path, prompt, suffix_new='_scall-replace', provider="openai", retain_delimiters=False):
    """
    Processes a file's text blocks and replace the original text with LLM-processed content based on a given prompt.
    
    :param blocks_file_path: string of the path to the file containing text blocks
    :param prompt: string of the prompt to use for processing each text block
    :param suffix_new: string of the suffix to append to the file when saving the new content
    :param provider: string indicating the LLM provider (default is "openai")
    :param retain_delimiters: boolean indicating whether to retain the original block delimiters in the new content
    :return: string of the path to the file with the updated content
    """
def scall_append(blocks_file_path, prompt, suffix_new='_scall-append', provider="openai", retain_delimiters=False):
    """
    Processes a file's text blocks to append LLM-processed content based on a given prompt after the original text.
    
    :param blocks_file_path: string of the path to the file containing text blocks
    :param prompt: string of the prompt to use for processing each text block
    :param suffix_new: string of the suffix to append to the file when saving the new content
    :param provider: string indicating the LLM provider (default is "openai")
    :param retain_delimiters: boolean indicating whether to retain the original block delimiters in the new content
    :return: string of the path to the file with the updated content
    """
def create_simple_llm_file(file_path, prompt, suffix_new, mode, split_file_function, provider="openai", *args, **kwargs):
    """
    Processes a file with a simple llm call to create a LLM-processed version using a specified block separation function and prompt.
    Substitutes the suffix_new for the original suffix of the file_path.

    :param file_path: string of the path to the file to be processed
    :param prompt: string of the prompt to use for processing each text block
    :param suffix_new: string of the new suffix that will be substituted for the original suffix
    :param mode: string indicating the operation mode ('replace' or 'append')
    :param split_file_function: function used to separate the file into blocks
    :param provider: string indicating the LLM provider (default is "openai")
    :param args: additional positional arguments passed to the block separation function
    :param kwargs: additional keyword arguments passed to the block separation function
    :return: string of the path to the file with the updated content
    """
PROMPT_SUMMARIZE = """
summaize the text after the speaker line as 3 keywords that best captures what is said, returned as a single line with commas between the words. retain the speaker line exactly as it is and put the new key word line as the next line directly underneath"""
PROMPT_QUOTATIONS = """
You are an expert at transcript processing, you are to evaluate the provided text according to specific quotation guidelines. Your task is to ensure that all instances of direct speech, internal monologue, specific terms, and imitations are correctly enclosed in single quotation marks. Additionally, you must identify and correct instances where quotations are missing or misused. Follow these guidelines:

1. Use single quotes ' ' for direct speech in anothers voice. Include a comma before the quote if it's preceded by a speech attribution (e.g., he said, she asked). Example correction: John said hello → John said, 'hello'.

2. Use single quotes for internal monologue presented as direct speech.

3. For specific terms, jargon, or phrases, use quotes, but do not add commas before the quotes. Place punctuation inside the single quotes.

4. Contextually decide if quotes are needed for ambiguous sentences.

In addition to those rules for quotations, please note the following things to keep in mind.

*  Do not add quotes for indirect speech. ie: they expressed their appreciation for them

*  For nested dialogue, use single quotes for the primary speech and double quotes for the nested part. 

*  Keep punctuation inside the single quotes for full sentences. For fragments, place punctuation outside.

*  For interrupted dialogue, continue the sentence within the same quotes after the tag or action.

*  Use single quotes for special cases like sarcasm or mimicry.

* Pay special attention to specific and related patterns that my preceed a quotation. These patterns include but are not limited to:
"they might say, "
"say well, "
"oh,"
"might ask"

Your primary tasks are to:
- Identify and fix instances where quotations are incorrectly applied.
- Locate and edit parts of the text where quotations are necessary but missing, according to these guidelines.

Please evaluate the text provided and make necessary corrections or suggest where quotations should be added or amended.
If an existing quotation is found your response should be the quote itself in curly braces, followed by a few word description of the problem with '**' at either end. if there is no problem with the existing quotation, just say 'CORRECT' for that description. If there is text that is not enclosed in quotes that shouldnt be, then DONT RETURN ANYTHING FOR IT. IGNORE IT. THE CURLY BRACES ARE AN IMPORTANT FLAG, USE THEM.
If there is a section that, according to the rules should have a quote, then return the section that should be quoted, with a few extra words from the text on either side. the quotes should be applied and flagged by curly braces and a description that uses the number of the rule that is being referenced to make the call.
If no changes at all are to be needed, please only respond with 'N/A'. Only use 'N/A' when there are no errors or quotes in the entire block."""
### COPYEDITS (1,590 tokens)
PROMPT_COPYEDIT = """
You are an expert in copyediting interview transcripts. Your task is to refine the transcript while preserving its verbatim nature. Follow these guidelines:
1. General Principles:
- Maintain verbatim transcription: Preserve the speaker's original words and speech patterns as much as possible.
- Aim for a polished and readable transcript while keeping the original meaning and style intact.
- Don't rephrase.
- Don't make drastic changes, don't make any changes that does not align with the given guidelines.
- Don't correct grammatical errors.
- Don't remove words if unnecessary or if it does not fall in any of the following guidelines mentioned.

2. Speaker Transitions and Segmentation based on context:
- Correct unsplit speaker segments based on context and conversation flow.

3. Proper Names and Terminology:
- Correct and standardize spelling of proper names, places, and specialized terms.
- Capitalize proper nouns appropriately.
- Capitalize also the positions and organizations (e.g., Town Manager, Town Council, Fire Marshal)
- Use unpunctuated acronyms, please don't add periods in between (e.g., ASCC instead of A.S.C.C.)

4. Transcription Error Correction:
- Identify and fix words that don't make sense given the surrounding context. (e.g., 'The cat jumped over the moon'  might be an error for 'The cat jumped over the broom.')
- Replace the informal word 'gonna' with 'going to' and 'wanna' with 'want to' 

5. Punctuations and Formatting:
- Use appropriate punctuation: commas, periods, question marks.
- Use double quotation marks ("") for quoted speech or phrase, meaning when the speaker is quoting someone else's words.
- Don't use exclamation marks (!) replace them with periods (.).
- If there are any forward slash (/) or backslash (\), replace them with dashes (-).
- Don't use semicolons (;) and colons (:), if needed then use commas (,) instead.
- Don't use hyphens (—) or dashes (-), if needed then use commas (,) instead.
- Don't use this format of ellipsis '…', use three periods (...) instead.

6. Disfluencies and Filler Words:
- Remove repetitions unless they add meaning (e.g., 'I I' change to 'I', 'this this' chang to 'this', 'he said that he said that' change to 'he said that').
- Remove 'uh' and 'um' unless they significantly impact meaning.
- Retain 'you know,' 'I mean,' 'like,' and 'yeah' if they add meaning to the statement.
- Only use commas for restarts, hesitations, and self-corrections (e.g., I want to, I mean, I need to fix, or rather, correct this issue.).
- Don't use hyphen (—) or dashes (-) for restarts, hesitations, and self-corrections.

7. Time and Dates:
- Change time format from 24-hour to 12-hour when appropriate (e.g., 14:00 to 2 o'clock).   
- Format dates consistently, as much as possible use the long format date (e.g., June 1st, June 4th).

8. Special Characters and Formatting:
- Spell out currency types (e.g., change $123 to 123 dollars).
- Use the special character '&' only if needed in the proper name (e.g., AT&T).
- Replace special characters with their standard English equivalents (e.g., Gödel to Godel).

9. Quotations and Specific Terms:
- Use double quotation marks if the speaker is quoting someone's words (e.g., Popper said, “Science must begin with myths, and with criticism of myths.").
- Follow the American style for quotations, place periods and commas inside quotation marks.

Here are examples with explanations of the kinds of edits I'm looking:
<example1>
Before: Dale Pfau (EPC Chair)  [9:14](https://youtu.be/hNFjjFll1EY&t=554)
When the new ones come out? We we will probably review them at least in September. We'll review full committing yet. Do you have any do you have any idea when that might happen?

After: Dale Pfau (EPC Chair)  [9:14](https://youtu.be/hNFjjFll1EY&t=554)
When the new ones come out? We will probably review them at least in subcommittee and may bring them to full committee. Yeah. Do you have any idea when that might happen?

Explanation:
- Removed repetition of "we".
- Corrected "full committing" to "full committee" based on context.
- Removed repetition of "do you have any".
- Added "Yeah." to separate the response to the previous question from the new question.
</example1>

<example2>
Before: Dale Pfau (EPC Chair)  [15:30](https://youtu.be/hNFjjFll1EY&t=930)
To add to that. I've had Starlink a little over a year now. I use it. I primarily got it as a backup to another Internet connection I have that goes out. StarLink never goes out. As long as you've got power, it's gonna be there. So even AT and T Fiber goes out occasionally when they lose power.

After: Dale Pfau (EPC Chair)  [15:30](https://youtu.be/hNFjjFll1EY&t=930)
To add to that, I've had Starlink a little over a year now. I use it. I primarily got it as a backup to another internet connection I have that goes out. Starlink never goes out. As long as you've got power, it's going to be there. So even AT&T Fiber goes out occasionally when they lose power.

Explanation:
- Added a comma after "To add to that".
- Changed "Internet" to lowercase "internet" as it's not a proper noun.
- Corrected the proper noun "StarLink" to "Starlink".
- Changed "gonna" to "going to" for formality.
- Corrected the proper noun "AT and T" to "AT&T".
</example2>

Please apply the necessary corrections to the transcript while maintaining the integrity of the spoken content. Remember that when in doubt and it's not specified in the given guidelines, prioritize preserving the original speech over making grammatical improvements. If you're unsure about a potential edit, flag it for human review, add *** in the beginning and end of the word or phrase that needs to be reviewed.

Before providing your final response, think through your edits step by step to ensure consistency and adherence to the provided guidelines.
"""
def create_copyedit_file(file_path, split_file_function, prompt, *args, **kwargs):
    """
    Processes a file for copyediting by separating it into blocks, applying a prompt to each block, and appending the results to a new file with a '_copyedit' suffix.
    Uses an argument to pass in the separator function, in case you want different types of blocks

    :param file_path: string of the path to the file to be processed
    :param split_file_function: function used to separate the file into blocks
    :param prompt: string of the prompt to use for processing each text block
    :param args: additional positional arguments passed to the block separation function
    :param kwargs: additional keyword arguments passed to the block separation function
    :return: string of the path to the file with the updated content
    """
### TRANSCRIPT TRANSITIONS (1,204 tokens)
PROMPT_TRANSITIONS = """
    Your task is to analyze transcripts for speaker transition errors. 
    You will do this on a single speaker segment where the speaker segments are identified by a speaker name followed by a time stamp with a link. And then on the next line, the segment text, which is the dialogue of what that speaker
    The intended target segment is identified as the segment that follows the following text "TARGET SEGMENT TO ANALYZE FOR TRANSITIONS".
    The input text I'm providing contains the ending speaker text from the speaker segment above, and it also contains below the target segment the beginning text from below. And those adjacent text are provided for context so you can look to see if there are words from the previous segment that should be in the target segment, and likewise if there are words from the next segment that should, that start the next segment that should be at the end of the target segment.    
    For your analysis, ignore any text on the speaker line itself, which is the line that contains the speaker name and the timestamp. There could be additional words after that for other processing. Just ignore those, such as 'SKIPQA'
    
    To do the analysis To look for possible transition errors in the target segment, what you should do is look at the ending words of the text above, which is from the previous segment, and see if they both, see if that text both looks out of place at the end of that text, and then insert that text at the beginning of the speaker segment text for the target segment and see if that fits better as a speaker dialogue. And you can also analyze that target speaker segment text to see if it looks out of place without the added text.

    If your analysis concludes that there are no transition errors in the text for the target segment, then make your response only the text "No suspected transition errors."
    If your analysis concludes that there are transition errors, then state what those are with quoted text, but do not reproduce the entire text for the target segment. I will make the modifications manually.
    """
PROMPT_TRANSITIONS_2 = """
    Your task is to analyze transcripts for speaker transition errors. You will be given entiere speaker segments and you will return suggestions if needed. Follow these guidelines:
1. **Speaker Transitions (ST) - Identifying Missing Speaker Transitions**:
   - ALWAYS Flag and suggest changes when there is a possible interjection from another speaker such as these listed:
        - 'Yes, I agree.'
        - 'Okay.'
        - 'Right.'
    - Be creative and think deeply about any sentence that could be from a different speaker and flag it with curly braces if there is doubt that the entire block is from a single speaker.
    - If there is any text at all that could be interpreted as coming from a seperate speaker, than Flag it for review.
    - Heavily favor tagging possible errors in the middle of a speaker block, rather than at the beggining or end. Do not flag anything at the beginning or the end of a block. assume that whatever is there is correct.
3. **Evaluating Overlapping Talk**:
   a) If overlapping talk is short and doesn't affect meaning, suggest integrating it into the next speaker segment.
   b) If moving the overlap confuses the start of the next segment and the overlapping statement is short and insignificant, suggest deletion.
   c) If the overlapping statement is significant and moving it confuses the start of the next segment, suggest adding a new speaker segment.

Your response if a change is considered to be needed should be of the entire text given to you, but with the problematic section enclosed in curly braces, followed by a few word description of the problem with '**' at either end. THE CURLY BRACES ARE AN IMPORTANT FLAG, USE THEM.
If no changes at all are to be needed, please only respond with 'N/A'. Only use 'N/A' when there are no errors in the entire block. The parts that are without error before or after an error should still be returned.
    """
def mod_blocks_file_with_adjacent_words(blocks_file_path, num_adjacent_words):
    """
    Modifies the content of a file by adding a specified number of words from the previous and next blocks to each block.
    Also adds a Markdown heading and content at the beginning of the new content.
    :param blocks_file_path: string of the path to the file containing text blocks
    :param num_adjacent_words: integer indicating the number of words to add from adjacent blocks
    :return: None
    """
def scall_replace_adjacent_words(blocks_file_path, prompt, adjacent_words, retain_delimiters=False, suffix_new='_scall-replace-adj'):
    """
    Replaces words adjacent to each block in a file with a language model processed version based on a given prompt.

    :param blocks_file_path: string of the path to the file containing text blocks
    :param prompt: string of the prompt to process each block with
    :param adjacent_words: integer indicating the number of words to add from adjacent blocks
    :param retain_delimiters: boolean indicating whether to retain original block delimiters
    :param suffix_new: string of the suffix to append to the new file name
    :return: string of the path to the modified file
    """
def create_transitions_file(file_path, split_file_function, prompt, *args, **kwargs):
    """
    Creates a file with transitions between blocks processed by a language model based on a given prompt.

    :param file_path: string of the path to the original file
    :param split_file_function: function used to separate the original file into blocks
    :param prompt: string of the prompt to process each block with
    :return: string of the path to the transitions file
    """
### QA GENERATION (2,827 tokens)
FCALL_PROMPT_QA_DIALOGUE_STATEDQA = """
You are an expert text analyzer that is trained in identifying stated questions and answers in transcripts of dialogue. You will be given blocks of dialogue and your role is to return extracted question and answer pairs that faithfully capture the meaningful content in the dialogue, while removing filler words and minimally modifying the text for clarity and readability. You will use your tool to only return exact JSON in the format specified.
"""
FCALL_PROMPT_QA_DIALOGUE_FROMANSWER = """
You are an expert text analyzer that is trained in identifying questions or implied questions. You will be given dialogue and your role is to return a create a general, simple question from the provided answer. This created general question may or may not be related to the question actually asked by the speaker in the dialogue preceding the answer. The created general question will be part of a question and answer set used for Retrieval Augmented Generation. The question must not mention the speaker name. You will use your tool to only return exact JSON in the format specified.
"""
FCALL_PROMPT_QA_DEUTSCH = """
You are an expert text analyzer that is trained in identifying questions or implied questions. You will be given dialogue and your role is to return a create a general, simple question from the provided answer. This created general question may or may not be related to the question actually asked by the speaker in the dialogue preceding the answer. The created general question will be part of a question and answer set used for Retrieval Augmented Generation. The question must not mention the speaker name. The question should be written in such a way that it assumes that the answer provided is the best knowledge humanity has about this topic at present moment.  Some specific phrases to use include: 1) 'multiverse quantum theory' - rather than 'many-worlds interpretation of quantum'. You will use your tool to only return exact JSON in the format specified. 
"""
CUSTOM_INSTRUCTIONS_DEUTSCH_GENERALQ = """
Analyze the following passage and create a general, simple question for which the answer will be the response. This will be part of a question and answer set such that new questions are compared against the questions, and answers retrieved. The question should not mention the author, or David Deutsch. The question should be written in such a way that it assumes that the answer provided is the best knowledge humanity has about this topic at present moment. Use the phrase 'multiverse quantum theory' rather than 'many-worlds interpretation of quantum'
"""
def tools_qa_speaker(speaker):  # no unittests
    """
    Generate a list of tools for question and answer extraction based on the speaker's response.

    :param speaker: string of the speaker's name whose responses are being analyzed
    :return: list of dictionaries containing tool configurations for QA extraction
    """
                    "description":f"""
                    The question should capture the essence of the original query posed by the interviewer in a simplified, generic form. It should focus on the core topic or idea, removing extraneous contextual details. The modified question should have semantic alignment with {speaker}'s answer. The question should be rephrased for a third-person audience, ensuring it is generalized and does not include direct references to {speaker}. DO NOT mention the name {speaker} in the question.
                    """ , 
                    "description": f"""
                    The timestamp corresponding to the start of {speaker}'s response in the format H:MM:SS or MM:SS or M:SS (chose whichever is present in the input text). This timestamp is crucial for contextualizing the answer within the transcript and must be accurate to reflect the exact moment the response begins.
                    """, 
def fcall_qa_speaker(block_file_path, speaker, fcall_prompt, suffix_new="_qa"):  # skip unittests because called below
    """ 
    Processes a transcript file already sectioned into blocks to generate new question and answer file.
    Answers are based on the speaker segments of the provided speaker.
    Uses OpenAI function calling.

    :param block_file_path: string of the path to the _blocks file to be processed.
    :param speaker: string of the speaker's name for the answers in QA.
    :param fcall_prompt: string of the prompt to be used for function calling.
    :param suffix_new: string of the suffix to be appended to the original filename for the new file. Defaults to "_qa".
    :return: string of the path to the newly created file with QA
    """
def create_qa_file_select_speaker(file_path, speaker, fcall_prompt):
    """
    Processes a _prepqa file to generate QA question and answer blocks using OpenAI LLM function calling.

    :param file_path: string of the path to the _prepqa transcript file to be processed.
    :param speaker: string of the speaker's name to be used in processing.
    :return: None.
    """    
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCTIPRT_FDA_TOWNHALLS_1ST_DRAFT = """
    You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue. 
    Your role is to extract and clarify the next question-answer pair from the given transcript chunk.
    The previous question-answer pair is provided in both the original text verbatim version and in a modified clarified version.

    Your task is identify the next important information that comes after the previous question-answer pair. This important information may comprise an explicit question asked by a speaker, or it may not and instead be a standalone statement.
    A requirement for qualification as important information of a next question-answer pair is that it is not included in the verbatim_answer property of the provided previous question answer pair.
     
    Identify the speakers for both questions and answers. Speakers are identified on separate lines of text that precede the speaker dialogue. The speaker lines end in either just a colon, or a timestamp which optionally be followed by a timestamp link. Speaker lines will start with the speaker name, or a surrogate string such as 'Moderator'. The speaker name may be followed by a role provided in parentheses. The role may comprise or contain text that specifies that speaker as an 'Authority Speaker'. See below for the text that specifies Authority Speakers.
    
    If important information is provided by a speaker identified as an Authority Speaker (see below), and that important information is not explicitly asked as a question, then you will generate a clarified question that is the best suitable question to be paired with that important information. The important information will be considered the answer. If a statement is made by a Non-Authority Speaker, and that statement is not phrased as a question, then it must be acknowledged by an Authority Speaker with an explicit affirmation response. See property descriptions below for values to use in this case where there is no explicit verbatim question.

    You will extract both the verbatim_answer from the transcript text, and then process the verbatim_answer to create the clarified_answer. The clarified_answer may be similar or perhaps even identical to the verbatim_answer from the transcript text. Typically the clarified answer wil be modified and therefore different at least to some extent from the verbatim_answer, however the clarified_answer must NEVER contradict the corresponding verbatim_answer and must ALWAYS have the same meaning. You will create the clarified versions of the question and answer by removing filler words to improve clarity and readability.

    This specific corpus comprises transcripts of the dialogue from virtual townhall meetings held by the United States Food and Drug Administration (FDA) to help answer technical questions about the development and validation of tests for the virus SARS-CoV2, and the updated policy on COVID-19 diagnostics policy for diagnostics test for coronavirus disease 2019 during the public health emergency caused by the COVID-19 global pandemic.

    Authority Speakers in this FDA Townhall Transcript Corpus are specified by the inclusion of the string ‘FDA’ in the role portion of the speaker line.

    The criteria for qualification for important information to be extracted as question-answer pairs is that the information be technical in nature, procedural, or legal. Information that should not be considered important and excluded from the question-answer extraction process is information related to the orchestration of the call such as which caller or speaker is being selected by the moderator. Information, whether questions by call-in speakers or answers by FDA staff, that is related to whether the FDA authorities can answer the question are considered to be legal and always to be included. These typical include answers from the FDA Authority Speakers similar to ‘we are not able to respond to questions about specific submissions that might be under review’. If you are not sure whether information qualifies as important information, then includeit and set the review_flag property of the response to True.
    """
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCTIPRT_FDA_TOWNHALLS = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics. Your role is to extract and clarify the next question-answer pair from the given transcript chunk, while also precisely identifying its location within the text.

Your task:
1. Identify the next question or important information after the provided previous question-answer pair, even if there is overlap between the corresponding transcript text. The next question and answer may be related to but should be distinct from the previous question and answer.
2. Extract both verbatim and clarified versions of questions and answers, excluding speaker lines and newline characters.
3. Identify speakers and their roles for questions and answers separately.
4. Generate clarified questions for important statements from Authority Speakers if not explicitly asked as questions.
5. Focus on technical, procedural, or legal information.
6. Include information about FDA's ability to answer questions.
7. Exclude call orchestration details involving starting the meeting, openning for questions, connection problems, speaker order, and meeting feedback surveys.
8. Precisely identify the start and end positions of the verbatim text from the transcript that corresponds to the clairified question-answer pair.

Key points:
- Important information must not be included in the previous answer.
- Speakers are identified by lines ending with a colon or timestamp.
- Authority Speakers are indicated by 'FDA' in their role description.
- Clarified versions should improve readability without changing meaning.
- Non-Authority Speaker statements must be acknowledged by Authority Speakers to be included.
- If unsure about information importance, include it and set the review flag to True.
- Accurately report the relative character positions (start and end) of the input transcript text that the extracted question-answer pair correspond to.
- All extracted text (verbatim and clarified) should be on a single line without newline characters or speaker identifications.

The precise identification of question-answer pair positions is crucial for the incremental extraction process. It allows for:
- Accurate progression through the transcript without missing or duplicating content.
- Identification of the next chunk to be processed based on the end position of the current pair.
- Thorough extraction of all important question-answer pairs from the original transcript.

This incremental approach ensures comprehensive coverage of the transcript while maintaining context and continuity throughout the extraction process. Your accurate identification of text positions is essential for the seamless progression of this extraction method.

This process is crucial for organizing and clarifying important information from FDA Town Hall meetings on COVID-19 diagnostics, ensuring accurate and accessible information dissemination while maintaining the transcript's integrity and completeness.
"""
def tools_qa_incremental():
def get_next_chunk(transcript, start_position, next_tokens):
    """
    Get the next chunk of transcript to process, based on the algorithm specification.
    
    :param transcript: Complete transcript text.
    :param start_position: Starting character position in the transcript.
    :param next_tokens: Number of tokens to look ahead.
    :return: Tuple of (chunk_text, end_position).
    """
def get_last_qa_block_start_position(qa_file_path):
    """
    Read the last processed start position from the existing QA file.
    
    :param qa_file_path: String of the path to the QA file.
    :return: Integer of the transcript start position, or 0 if not found.
    """
def fcall_qa_incremental(transcript, next_tokens, fcall_prompt, start_position):
    """
    Processes a transcript string incrementally to extract the next question-answer pair using OpenAI function calling.
    This function yields each QA block along with the current position in the transcript, allowing for incremental processing and resumption from the last processed position.  

    :param transcript: String of the transcript content.
    :param next_tokens: Integer of the number of tokens to look ahead.
    :param fcall_prompt: String of the prompt to be used for function calling.
    :param start_position: Integer of the starting position in the transcript.
    :yield: Tuple of (qa_block, current_position) or (None, current_position) if an error occurred.
    """
        prev_block_prompt = "Please identify the first question-answer pair in the following transcript chunk:" if not previous_block else f"""
        Previous Question-Answer Block:
        {previous_block}
        Please identify the next question-answer pair after this one in the following transcript chunk:
        """
def create_qa_file_from_transcript_incremental(file_path, fcall_prompt):
    """
    Manages the incremental extraction of question-answer pairs from a transcript file.
    This function handles the overall process, including reading the transcript, determining the next chunk to process, and appending the extracted QA blocks to a new file.

    :param file_path: String of the path to the transcript file to be processed.
    :param fcall_prompt: String of the prompt to be used for function calling.
    :return: String of the path to the newly created QA file.
    """
### QA EVAL (497 tokens)
def validate_qa_transcript_positions(transcript, qa_dict):
    """
    Validate the extracted QA block against the original transcript based on reported positions.
    
    :param transcript: String of the full transcript text.
    :param qa_dict: Dictionary containing the extracted QA information.
    :return: Tuple of (bool, str) indicating pass/fail and a mismatch description if applicable.
    """
def evaluate_qa_extraction(transcript, qa_file_path):
    """
    Evaluate the QA extraction process using LLM-based checks and position validation.
    
    :param transcript: String of the full transcript text.
    :param qa_file_path: String path to the file containing extracted QA blocks.
    :return: List of dictionaries containing evaluation results for each QA block.
    """
        eval_prompt = f"""
        Evaluate the following question-answer pair extracted from an FDA Town Hall transcript:
        
        Verbatim Question: {qa_dict['VERBATIM QUESTION']}
        Verbatim Answer: {qa_dict['VERBATIM ANSWER']}
        Clarified Question: {qa_dict['CLARIFIED QUESTION']}
        Clarified Answer: {qa_dict['CLARIFIED ANSWER']}
        
        Please evaluate based on the following criteria:
        1. Accuracy (0-5 scale): How well does the extracted information match the content and intent of the original transcript?
        2. Formatting (Pass/Fail): Are all texts on a single line without newline characters or speaker identifications?
        3. Topic Relevance (Pass/Fail): Do the extracted topics align with the content of the Q&A pair?
        
        Provide your evaluation in JSON format with the following structure:
        {{
            "accuracy_score": int,
            "formatting": "Pass" or "Fail",
            "topic_relevance": "Pass" or "Fail",
            "comments": "Any additional comments or explanations"
        }}
        """
def generate_evaluation_report(evaluation_results, output_file):
    """
    Generate a readable report from the evaluation results.
    
    :param evaluation_results: List of dictionaries containing evaluation results.
    :param output_file: String path to write the report.
    """
def run_automated_evaluation(transcript_file, qa_file):
    """
    Run the automated evaluation process.
    
    :param transcript_file: String path to the original transcript file.
    :param qa_file: String path to the file containing extracted QA blocks.
    """
## primary/vectordb.py (1,465 tokens)
### VECTOR DB SUPPORT (1,171 tokens)
def generate_embedding(text, model=EMBEDDING_MODEL):
    """ 
    Generates an embedding vector for the provided text using the specified OpenAI embeddings model.

    :param text: string of text to generate an embedding for.
    :param model: string of the OpenAI embeddings model to use.
    :return: list of floats representing the embedding vector.
    """
def generate_vectors_qa(folder_paths, suffixpat_include, include_subfolders=True):
    """ 
    Generates vectors from markdown files in the specified folder paths.

    :param folder_paths: list of strings of the paths to the folders containing markdown files.
    :param include_subfolders: boolean indicating whether to search for markdown files in subfolders. Default is True.
    :return: vectors as a list of dictionaries, each containing an id, values, and metadata for a block of text.
    """
def vectors_to_json(vectors, file_path):
    """
    Converts a list of dictionaries into a JSON file.

    :param vectors: list of dictionaries to be converted.
    :param file_path: name of the JSON file to be created.
    :return: None.
    """
def json_to_vectors(file_path):
    """
    Loads vectors from a JSON file.

    :param file_path: Path to the JSON file containing the vectors.
    :return: List of vectors loaded from the JSON file. Returns an empty list if an error occurs.
    """
def validate_vectors(vectors, required_fields=None, verbose=False):
    """ 
    Validates that each vector in the list has the required fields and correct data types.

    :param vectors: list of dictionaries, each representing a vector with an id, values, and metadata.
    :param required_fields: list of required field names (in uppercase). If None, uses a default set.
    :param verbose: boolean, if True, prints additional information during validation.
    :return: None. Raises ValueError if validation fails.
    """
def upsert_vectors_pinecone(vectors, vector_index_name, new_index=True):
    """ 
    Upserts vectors into a Pinecone index in batches of 100, creating the index if it does not exist and if new_index is True.

    :param vectors: list of dictionaries, each representing a vector to be upserted.
    :param vector_index_name: string of the name of the Pinecone index.
    :param new_index: boolean indicating whether to create a new index if it does not exist. Default is True.
    :return: None.
    """
def delete_pinecone_index(vector_index_name, user_prompt=True):
    """
    Deletes a Pinecone index if it exists, optionally prompting the user for confirmation.

    :param vector_index_name: string of the name of the Pinecone index to be deleted.
    :param user_prompt: boolean indicating whether to prompt the user for confirmation before deletion. Default is True.
    :return: Boolean indicating whether the index was actually deleted.
    """
def update_pinecone_index_list_md(file_name='pinecone_index_list.md', log_folder_path=VZIP_LOG_FOLDER):
    """
    Updates a markdown file with a list of Pinecone indices.

    :param file_name: Name of the markdown file to update. Default is 'pinecone_index_list.md'.
    :param log_folder_path: Path to the folder where the file will be saved. Default is VZIP_LOG_FOLDER.
    """
def save_splits_to_json(all_chunks, output_base_filename, metadata, log_folder_path=VZIP_LOG_FOLDER):
    """
    Saves the text splits and metadata to a JSON file, organized by source.

    :param all_chunks: List of Document objects containing the text splits.
    :param output_base_filename: Base filename for the output JSON file.
    :param metadata: Dictionary containing metadata to be included in the JSON.
    :return: Path to the saved JSON file.
    """
def setup_create_vectordb(folder_paths, vector_index_base, suffixpat_include=None):
    """
    Sets up the initial parameters for creating a vector database.
    
    :param folder_paths: List of folder paths to process
    :param vector_index_base: Base name for the vector index
    :param suffixpat_include: Pattern to filter files (optional)
    :return: Tuple of (vector_index_name, vector_index_name_with_timestamp, datetime, all_file_paths)
    """
def check_and_create_pinecone_index(vector_index_name, dimension=1536, metric='cosine'):
    """
    Initializes Pinecone, checks if the specified index exists, creates it if it doesn't,
    and prompts the user for action if the index already exists.
    
    :param vector_index_name: Name of the Pinecone index to check/create
    :param dimension: Dimension of the vectors (default is 1536 for OpenAI embeddings)
    :param metric: Distance metric to use (default is 'cosine')
    :return: Boolean indicating whether to continue with the vector database creation
    """
def log_zip_vectordb(vectors_file_path, vector_index_name_with_timestamp, metadata, file_paths_list, log_folder_path=VZIP_LOG_FOLDER):
    """
    Creates a log file for vector database creation and zips source files.

    :param vectors_file_path: Path to the vectors file to be zipped.
    :param vector_index_name_with_timestamp: Name of the vector index with timestamp.
    :param metadata: Metadata dictionary containing relevant information.
    :param file_paths_list: List of all file paths processed.
    :param log_folder_path: Folder to store log files and zips.
    :return: Tuple of (log_file_path, zip_file_path)
    """
### VECTOR DB CREATION (286 tokens)
def create_vectordb_vrag_langchain(folder_paths, vector_index_base, suffixpat_include=None, skip_pinecone=False):  # pinecone index names can only contain - and not _ 
    """ 
    Establishes a Pinecone database using documents from the directory of markdown files. 
    If vector index name already exists in Pinecone, this aborts - so the index must be manually deleted in portal prior to running this.
    VRAG is a different pipeline than QRAG, and currently does not support custom metadata. (RT 6-10-2024)
    VRAG Is set up to mainly accept unstructured documents, and QRAG only accepts structured input documents.

    :param folder_paths: list of strings of the paths leading to the Obsidian vaults.
    :param vector_index_base: string of the base name for the Pinecone index, (may only contain -'s), to which the number of files and date are added. 
    :param suffixpat_include: string or None, specifying which file suffix patterns (_suffix and/or extension) to include.
    :param skip_pinecone: boolean, whether to skip the pinecone index creation and upserting (for splitting and testing).
    :return: None
    """ 
def create_qrag_vectordb(folder_paths, vector_index_base, suffixpat_include=None):
## primary/rag.py (2,297 tokens)
### RETRIEVAL (96 tokens)
def pinecone_retriever(query, vector_index_name, num_chunks=5):
    """ 
    Retrieves relevant question chunks from a Pinecone index based on the input question.

    :param question: string of the input question to search for.
    :param vector_index_name: string of the name of the Pinecone index to query.
    :return: tuple containing fetched question chunks and a dictionary of retrieved IDs with their scores.
    """
### VRAG (276 tokens)
def print_vrag_display_text(json_object, show_prompt=False):
    """
    Prints a formatted display text for VRAG (Vector Retrieval Augmented Generation) results.

    :param json_object: dictionary containing VRAG results with 'content' key.
    :param show_prompt: boolean to determine whether to show the full LLM prompt.
    :return: None.
    """
def vrag_llm_call(user_question, vector_index_name, vrag_preamble=VRAG_PREAMBLE_V1, llm_model=DEFAULT_LLM_MODEL, user_id='default', vrag_version="1.0"):
    """
    Initiates a chat session using vector retrieval augmented generation (VRAG) with a specified question,
    prompt template, and index name. Returns a JSON object with the results.

    :param user_question: string of the question to initiate the chat with.
    :param vector_index_name: string of the name of the pinecone index to use for retrieval.
    :param vrag_preamble: string of the preamble used to format the chat prompt.
    :param llm_model: string of the language model to use.
    :param user_id: string of the user identifier.
    :param bot_version: string of the bot version.
    :return: dictionary containing the chat response and metadata.
    """
### QRAG (1,919 tokens)
def select_chunks_qrag_1or2(fetched_qa_chunks, retrieved_ids_scores):
    """ 
    Sorts and returns the most relevant chunks based on similarity score and 'STARS' rating.
    Filters down to 1 or 2 chunks from the 5 fetched.

    :param fetched_qchunks: dictionary of fetched question chunks from Pinecone.
    :param retrieved_ids_scores: dictionary of retrieved IDs with their similarity scores.
    :return: tuple containing the highest similarity chunk and the highest 'STARS' rated chunk (if different).
    """
def parse_chunk_all(chunk, simscores=None):
    """ 
    Formats information from a chunk and its optional similarity scores into a structured dictionary,
    including all fields present in the chunk's metadata. Handles various data types including lists.

    :param chunk: dictionary containing metadata and content of a document chunk.
    :param simscores: optional dictionary of similarity scores keyed by chunk id.
    :return: dictionary containing formatted chunk information.
    """
    def safe_convert(value):
def parse_chunk_qa_dd(chunk, simscores, prefix=''):
        """Converts value to appropriate type, handling various data types including lists."""
        if isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, list):
            return [safe_convert(item) for item in value]
        else:
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return str(value)

    result = {}

    # Process all metadata fields
    for key, value in chunk['metadata'].items():
        result[key.lower()] = safe_convert(value)

    # Add similarity score if available
    if simscores is not None and chunk['id'] in simscores:
        result['sim'] = safe_convert(simscores[chunk['id']])

    return result

    """ 
    def safe_int(value, default=0):
    def safe_float(value, default=0.0):
def qrag_routing_call(user_question, vector_index_name, routes_dict, routes_bounds=[0.3, 0.9], 
    """
    # Call the general parsing function
    general_result = parse_chunk_all(chunk, simscores)

        try:
            return int(value) if value != '' else default
        except (ValueError, TypeError):
            return default

        try:
            return float(value) if value != '' else default
        except (ValueError, TypeError):
            return default

    # Modify the result to match the original function's output
    result = {
        f'{prefix}source': str(general_result.get('source', 'Unknown source')),
        f'{prefix}timestamp': str(general_result.get('timestamp', 'Unknown timestamp')),
        f'{prefix}question': str(general_result.get('question', 'Unknown question')),
        f'{prefix}answer': str(general_result.get('answer', 'Unknown answer')),
        f'{prefix}sim': safe_float(general_result.get('sim', 0.0)),
        f'{prefix}stars': safe_int(general_result.get('stars', 0))
    }

    # Create the display string
    stars = result[f'{prefix}stars']
    sim_score = result[f'{prefix}sim']
    result[f'{prefix}display'] = f"QUOTED ANSWER STARS: {stars}\nQUOTED QUESTION SIMILARITY SCORE: {round(sim_score * 100)}%"

    return result

llm_model=DEFAULT_LLM_MODEL, user_id='default', qrag_version="1.0"):
    """ 
def qrag_llm_call(json_object):
    """
    routes_flow_name = "3 routes, sim-star double, separate prompts"
    
    chunks, simscores = pinecone_retriever(user_question, vector_index_name)
    
    top_sim_chunk, top_stars_chunk = select_chunks_qrag_1or2(chunks, simscores)
    top_sim_info = parse_chunk_qa_dd(top_sim_chunk, simscores, 'top_sim_')
    max_sim = top_sim_info['top_sim_sim']
    max_stars = top_sim_info['top_sim_stars']  # Will be reassigned below if there is a 2nd chunk that has the top stars 

    quoted_qa = routes_dict['quoted_qa_single'].format(**top_sim_info)

    if top_stars_chunk is not None:
        top_stars_info = parse_chunk_qa_dd(top_stars_chunk, simscores, 'top_stars_')
        max_stars = top_stars_info['top_stars_stars']
        combined_info = {**top_stars_info, **top_sim_info}
        quoted_qa = routes_dict['quoted_qa_double'].format(**combined_info)
            
    lower_sim_bound, upper_sim_bound = routes_bounds

    if max_sim >= upper_sim_bound:
        route_preamble = routes_dict['route_preamble_good_match']
    elif max_sim <= lower_sim_bound:
        route_preamble = routes_dict['route_preamble_no_match']
        quoted_qa = ""
    else:
        route_preamble = routes_dict['route_preamble_partial_match']
    
    return {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "vector_index_name": vector_index_name,  # pinecone vector db id
            "qrag_version": qrag_version,
            "llm_model": llm_model,
            "routes_info": {
                "routes_flow_name": routes_flow_name,
                "upper_sim_bound": upper_sim_bound,
                "lower_sim_bound": lower_sim_bound,
                "max_sim": "{:.3f}".format(max_sim),
                "max_stars": max_stars,
                "routes_dict_content": routes_dict
            }
        },
        "content": {
            "user_question": user_question,
            "route_preamble": route_preamble,
            "quoted_qa": quoted_qa,  # includes 'QUOTED X: ' and newlines at end
            "ai_answer": "WAITING FOR AI ANSWER...",
            "chunks": {
                "max_sim": "{:.3f}".format(max_sim),
                "max_stars": max_stars,
                "chunks": [
                    {
                        "question": top_sim_info['top_sim_question'],
                        "source": top_sim_info['top_sim_source'], 
                        "timestamp": top_sim_info['top_sim_timestamp'],
                        "answer": top_sim_info['top_sim_answer'],
                        "stars": top_sim_info['top_sim_stars'],
                        "sim": "{:.3f}".format(top_sim_info['top_sim_sim'])
                    }
                ] + ([
                    {
                        "question": top_stars_info['top_stars_question'],
                        "source": top_stars_info['top_stars_source'],
                        "timestamp": top_stars_info['top_stars_timestamp'],
                        "answer": top_stars_info['top_stars_answer'],
                        "stars": top_stars_info['top_stars_stars'],
                        "sim": "{:.3f}".format(top_stars_info['top_stars_sim'])
                    }
                ] if top_stars_chunk is not None else [])
            }
        }
    }

    """ 
def print_qrag_display_text(json_object):
    """
    # Verify necessary fields exist in the JSON object
    required_fields = ['user_question', 'route_preamble', 'quoted_qa', 'ai_answer']
    missing_fields = [field for field in required_fields if field not in json_object['content']]
    if missing_fields:
        raise ValueError(f"Missing required fields in JSON object: {', '.join(missing_fields)}")

    # Extract necessary information from json_object
    user_question = json_object['content']['user_question']
    route_preamble = json_object['content']['route_preamble']
    quoted_qa = json_object['content']['quoted_qa']
    
    # Prepare the prompt for the LLM call
    llm_prompt = route_preamble + "\n" + quoted_qa + "\nUSER QUESTION: " + user_question + "\n\nAI ANSWER: "
    
    # Make the LLM call using simple_openai_chat_completion_request function
    llm_model = json_object['metadata']['llm_model']
    llm_answer = simple_openai_chat_completion_request(llm_prompt, model=llm_model)
    
    # Add the AI answer to the json_object
    json_object['content']['ai_answer'] = llm_answer
    
    return json_object

    """ 
def qrag_2step(user_question, routes_dict, vector_index_name):
    """
    user_question = json_object['content']['user_question']
    route_preamble = json_object['content']['route_preamble']
    quoted_qa = json_object['content']['quoted_qa']
    ai_answer = json_object['content']['ai_answer']
    display_text = 'USER QUESTION: ' + user_question + '\n\n' + 'ROUTE PREAMBLE: ' + route_preamble + '\n\n' + quoted_qa + 'AI ANSWER: ' + ai_answer
    print(display_text)

    """ 
## primary/conversion.py (693 tokens)
### LLAMAINDEX (372 tokens)
def convert_llamaparse_pdf_to_md(file_path):
def convert_llamaindex_gdocs_to_md(gdoc_id_list):
    """
    # Create JSON object with routing information
    routing_json_obj = qrag_routing_call(user_question, routes_dict, vector_index_name)

    # Print the display text for the QRAG process
    print_qrag_display_text(routing_json_obj)

    # Generate and print the AI answer
    ai_answer = qrag_llm_call(routing_json_obj)['content']['ai_answer']
    print(ai_answer)






import os
import re
import logging
import pypandoc

from llama_parse import LlamaParse  # pip install llama-index llama-parse
from llama_index.core import SummaryIndex
from llama_index.readers.google import GoogleDocsReader  # pip install llama-index llama-index-readers-google
#from IPython.display import Markdown, display

from config import LLAMA_CLOUD_API_KEY


    suffix_append = "_llamaparse"
    documents = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown",verbose=True).load_data(file_path)
    print(documents[0].text[0:1000])
    md_file_path = file_path.rsplit('.', 1)[0] + suffix_append + '.md'  # Replace the file extension with .md
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(documents[0].text)
    print("Completed LlamaParse pdf to md conversion and appended suffix: " + suffix_append + " on input file_path: " + file_path)
    return md_file_path

#TODO WIP - not working because needs different gcloud auth than service account
    """
### PANDOC (315 tokens)
def convert_file_to_md_pandoc(file_path, suffix_new="_pandoc"):
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    # Hardcoded full path to the credentials file
    credentials_file = 'credentials_new.json'

    # Get the directory and original filename of the credentials file
    credentials_dir, original_filename = os.path.split(credentials_file)

    # # Save the current working directory
    # cwd = os.getcwd()

    # # Change the working directory to the one containing the credentials file
    # os.chdir(credentials_dir)

    # Temporarily rename the credentials file to credentials.json
    os.rename(original_filename, 'credentials.json')

    # Load the Google Docs data
    documents = GoogleDocsReader().load_data(gdoc_id_list=gdoc_id_list)

    # Rename the credentials file back to its original name
    os.rename('credentials.json', original_filename)

    # # Change the working directory back to the original one
    # os.chdir(cwd)

    # Create a summary index from the documents
    index = SummaryIndex.from_documents(documents)

    # # Convert each document to Markdown and display it
    # for doc in index.documents:
    #     display(Markdown(doc.text))


''' To confirm installation, run: pandoc --version
Should see:
pandoc 3.2
Features: +server +lua
Scripting engine: Lua 5.4
'''

    """
## primary/docwork.py (3,157 tokens)
### COMMON TEXT (276 tokens)
def load_custom_dictionary(file_path):
    """
    output_markdown_file_path = os.path.splitext(file_path)[0] + suffix_new + '.md'
    extra_args = [
        '--wrap=none',
        '--to=markdown_strict+pipe_tables',
        '--extract-media=./media'  # Extract media to a 'media' directory relative to the markdown file
    ]
    output = pypandoc.convert_file(file_path, 'markdown', outputfile=output_markdown_file_path, extra_args=extra_args)
    assert output == ""  # ensures that the conversion process did not return any content directly, which implies that the conversion output was successfully written to the file

    print(f"Successful file conversion to markdown using pypandoc for file: {file_path}")
    return output_markdown_file_path





import os
import re


#TODO 7-18 RT - consider whether this is OK to be in function, think it was not previously and getting Problems
    '''
    # import nltk
    # nltk.download('words')
    # nltk.download('punkt')  # Added to download the 'punkt' tokenizer models
    # from nltk.corpus import words
#TODO rename and comment this function so it's more clear what it does
    '''
    """ Load a custom dictionary from a file. """
### TRANSCRIPTS (1,897 tokens)
def replace_colon_for_non_speaker(text):
    """
    Replaces colons that do not form part of speaker names with a space and a dash.

    :param text: string of the transcript text that needs cleaning.
    :return: string of the cleaned transcript text.
    """
def reformat_transcript_text(original_text):
    """
    Reformats and cleans transcript text by separating speaker names from their dialogue.

    This function performs the following operations:
    1. Removes parentheses from the text.
    2. Replaces colons in non-speaker contexts.
    3. Identifies speaker names and separates them from their dialogue.
    4. Formats the text so that each speaker name is on its own line, followed by their dialogue.
    5. Removes extra spaces and ensures consistent formatting.

    :param original_text: string of the raw transcript text to be cleaned and reformatted.
    :return: string of the cleaned and restructured transcript text, with speaker names clearly separated from dialogue.
    """
    def flush_current_dialogue():
def validate_transcript(file_path, verbose=False):
        """Helper function to flush the current dialogue to the fixed_lines."""
        if current_speaker:
            fixed_lines.append(f"{current_speaker}:")
            fixed_lines.append(" ".join(current_dialogue).strip() + "\n")
    
    for line in lines:
        match = speaker_dialogue_pattern.match(line)
        if match:
            if time_reject_pattern.match(line):
                current_dialogue.append(line)
            else:
                # Flush the previous dialogue if there was one
                flush_current_dialogue()
                
                # Start a new dialogue block
                current_speaker, dialogue_part = match.groups()
                current_dialogue = [dialogue_part] if dialogue_part else []
        else:
            # If it's not a speaker line, accumulate dialogue lines
            if current_speaker:
                current_dialogue.append(line)
    
    # Don't forget to flush the last speaker's dialogue
    flush_current_dialogue()
    
    rejoined_text = "\n".join(fixed_lines)
    # Compresses 2 or more spaces into a single space
    final_text = re.sub(r' {2,}', ' ', rejoined_text)
    return final_text

#TODO consider refactor by creating new function to determine if a line is a speaker line get_speaker_name(line) and return None if not speaker line but consider what to do if speaker line is invalid
#TODO sync this with validate qa
    """
def extract_transcript_data(file_path):
    """
    from primary.fileops import get_heading, verbose_print
    
    transcript = get_heading(file_path, '### transcript')
    banned_characters = [':']
    valid_format = True

    lines = transcript.split('\n')
    line_number = 2  # Skip the first 2 lines

    while line_number < len(lines):
        line = lines[line_number].strip()

        # Check if line contains a speaker name
        if ':' in line:
            speaker, text_spoken = line.split(':', 1)
            speaker = speaker.strip()

            if not speaker:
                verbose_print(verbose, f'FAILED VALIDATION -  Empty speaker name at line:\n{line}')
                valid_format = False

            # Check the next line for banned characters
            if line_number + 1 < len(lines):
                text_line = lines[line_number + 1].strip()
                for char in banned_characters:
                    if char in text_line:
                        # Check if the banned character is a colon and if it's part of a time reference
                        if char == ':' and re.search(r'\d:\d{2}', text_line):
                            continue
                        verbose_print(verbose, f'FAILED VALIDATION -  Banned character "{char}" found in transcript at line:\n{line}')
                        valid_format = False
            else:
                verbose_print(verbose, f'FAILED VALIDATION -  Missing transcription after speaker name at line:\n{line}')
                valid_format = False

            # Check for an empty line after the text spoken
            if line_number + 2 >= len(lines) or lines[line_number + 2].strip():
                verbose_print(verbose, f'FAILED VALIDATION -  Missing empty line after segment at line:\n{line}')
                valid_format = False

            line_number += 3
        else:
            verbose_print(verbose, f'FAILED VALIDATION -  Invalid format (missing speaker name) at line:\n{line}')
            valid_format = False
            line_number += 1  # Move to the next line to continue checking

    if valid_format:
        verbose_print(verbose, f'PASSED validation of speaker segments for file: {file_path}')
        return True
    else:
        verbose_print(verbose, f'FAILED validation of speaker segments for file: {file_path}')
        return False

    """
def create_speaker_triples(file_path):
        """
    from primary.fileops import get_heading, get_timestamp
    
    transcript_data = []
    transcript_text = get_heading(file_path, '### transcript')
    if transcript_text is None:
        print(f"NO TRANSCRIPT from in extract_transcript_data on {file_path}")
        return None  
    lines = transcript_text.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        data_dict = {'speaker_full': None, 'speaker_name': None, 'speaker_role': None, 'timestamp': None, 'timestamp_link': None, 'dialogue': None}
        
        # Path for lines ending with a colon
        if line.endswith(':'):
            speaker_full = line.rstrip(' :')  # Remove the colon and strip any leading/trailing whitespace
            data_dict['speaker_full'] = speaker_full
            if '(' in speaker_full and ')' in speaker_full:
                speaker_role_start = speaker_full.find('(')
                speaker_role_end = speaker_full.find(')')
                data_dict['speaker_role'] = speaker_full[speaker_role_start + 1:speaker_role_end]
                data_dict['speaker_name'] = speaker_full[:speaker_role_start].strip()
            else:
                data_dict['speaker_name'] = speaker_full
            # Assign the entire next line as dialogue if available
            if i + 1 < len(lines):
                data_dict['dialogue'] = lines[i + 1].strip()

        # Path for lines with a timestamp following the speaker name
        else:
            timestamp, index = get_timestamp(line)
            if index is not None:
                speaker_full = line[:index].strip()
                data_dict['speaker_full'] = speaker_full
                if '(' in speaker_full and ')' in speaker_full:
                    speaker_role_start = speaker_full.find('(')
                    speaker_role_end = speaker_full.find(')')
                    data_dict['speaker_role'] = speaker_full[speaker_role_start + 1:speaker_role_end]
                    data_dict['speaker_name'] = speaker_full[:speaker_role_start].strip()
                else:
                    data_dict['speaker_name'] = speaker_full
                data_dict['timestamp'] = timestamp
                # Extract the timestamp link if present
                link_start = line.find('(', index)
                link_end = line.find(')', link_start)
                if link_start != -1 and link_end != -1:
                    data_dict['timestamp_link'] = line[link_start + 1:link_end]
                # Assign the entire next line as dialogue if available
                if i + 1 < len(lines):
                    data_dict['dialogue'] = lines[i + 1].strip()

        if data_dict['speaker_name']:  # Only add to list if there's a speaker
            transcript_data.append(data_dict)

    return transcript_data

    """
def create_speaker_matrix(folder_path, suffix_include=None, target_file_path="speaker_matrix.csv"):
    """
    from primary.docwork import extract_transcript_data
    
    print(f"create_speaker_triples on {file_path}")
    transcript_data = extract_transcript_data(file_path)
    if transcript_data is None:
        print(f"NO TRANSCRIPT so create_speaker_triples is returning an empty string on {file_path}")
        return ""  # Return an empty string if no data is extracted
    speaker_dict = {}

    for entry in transcript_data:
        speaker_full = entry['speaker_full'].strip()
        if speaker_full:
            speaker_dict[speaker_full] = speaker_dict.get(speaker_full, 0) + 1

    # Get the file stem (filename without extension)
    file_stem = os.path.splitext(os.path.basename(file_path))[0]

    speaker_triples = []
    for speaker, count in speaker_dict.items():
        speaker_triples.append((speaker, file_stem, count))

    # Sort the triples by count descending, then by speaker name alphabetically if counts are the same
    speaker_triples.sort(key=lambda x: (-x[2], x[0]))

    formatted_triples = [f"{speaker}, {file_stem}, {count}" for speaker, file_stem, count in speaker_triples]
    return "\n".join(formatted_triples)

    """
### PROPER NAMES (978 tokens)
def extract_proper_names(text, custom_proper_names_files=None, bool_include_custom=False, verbose=False):
    """
    from primary.fileops import apply_to_folder, create_csv_matrix_from_triples
    
    # Use apply_to_folder to process files and get speaker triples
    speaker_triples_results = apply_to_folder(create_speaker_triples, folder_path, suffix_include=suffix_include)
    # Join the speaker triples into a single string, filtering out any empty results
    triples_text = "\n".join(filter(None, speaker_triples_results.values()))

    # Check if the target file path has a folder component; if not, use the folder_path
    if not os.path.dirname(target_file_path):
        target_file_path = os.path.join(folder_path, os.path.basename(target_file_path))

    # Check if the target file already exists
    if os.path.exists(target_file_path):
        overwrite = input(f"The file {target_file_path} already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled by the user.")
            return None

    # Call the create_csv_matrix_from_triples function to create the CSV file
    return create_csv_matrix_from_triples(triples_text, target_file_path)  # function is in fileops


    """
def create_proper_names_triples(file_path, custom_proper_names_files=None, bool_include_custom=False, verbose=False):
    """
    from primary.fileops import verbose_print

    # Load the set of English words from NLTK
    english_words = set(words.words())

    # Prepare to extract words
    proper_names = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        # Tokenize the sentence into words
        words_in_sentence = nltk.word_tokenize(sentence)
        
        # Combine capitalized words
        combined_name = []
        for i, word in enumerate(words_in_sentence):
            if word[0].isupper():
                combined_name.append(word)
            else:
                if combined_name:
                    # Check if the combined name is valid
                    name = " ".join(combined_name)
                    # Check if the first word of the combined name is a common English word and it's the first word in the sentence
                    if combined_name[0].lower() in english_words and i == len(combined_name):
                        combined_name = []
                    else:
                        proper_names.append(name)
                        combined_name = []
        # Check if the last word(s) in the sentence were capitalized and not added
        if combined_name:
            name = " ".join(combined_name)
            if combined_name[0].lower() not in english_words or len(combined_name) != 1:
                proper_names.append(name)
    proper_names = sorted(set(proper_names))

    # Load capitalized words from multiple custom lists to retain as proper names
    proper_names_in_custom_dict = set()
    if custom_proper_names_files:
        for custom_list_path in custom_proper_names_files:
            with open(custom_list_path, 'r') as file:
                for line in file:
                    line_words = line.strip().split()
                    for word in line_words:
                        if word[0].isupper():
                            proper_names_in_custom_dict.add(" ".join(line_words))
                            break

    # Load the list of erroneous non-proper name words
    not_proper_names_path = 'data/capitalized_words_not_proper_names.txt'
    with open(not_proper_names_path, 'r') as file:
        not_proper_names = {line.strip() for line in file}

    # Filter proper names, excluding known non-proper names and applying other conditions
    filtered_proper_names = [
        name for name in proper_names 
        if (len(name.split()) > 1 or name.lower() not in english_words or (bool_include_custom and name in proper_names_in_custom_dict)) 
        and name not in not_proper_names
    ]
    
    # If custom names should not be included, remove all names that are in the custom proper names dictionary
    if not bool_include_custom:
        filtered_proper_names = [name for name in filtered_proper_names if name not in proper_names_in_custom_dict]
    
        # Print the filtered common words
    common_words_removed = sorted(set(proper_names) - set(filtered_proper_names))
    verbose_print(verbose, "\n\nRemoved Common Words")
    for common_word in common_words_removed:
        verbose_print(verbose, common_word)
    verbose_print(verbose, "\n\n")

    return filtered_proper_names

    """
def print_proper_names(file_path, custom_proper_names_files=None, bool_include_custom=False, verbose=False):
## primary/structured.py (2,118 tokens)
### BLOCK PROCESSING (1,055 tokens)
def get_blocks_from_file(qa_file_path, verbose=False):
    """
    try:
        with open(file_path, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        return "File not found."

    proper_names = extract_proper_names(text, custom_proper_names_files, bool_include_custom, verbose)
    proper_name_dict = {}

    for proper_name in proper_names:
        proper_name_dict[proper_name] = proper_name_dict.get(proper_name, 0) + 1

    file_stem = os.path.splitext(os.path.basename(file_path))[0]
    proper_triples = []
    for proper_name, count in proper_name_dict.items():
        proper_triples.append((proper_name, file_stem, count))

    proper_triples.sort(key=lambda x: (-x[2], x[0]))
    formatted_triples = [f"{proper_name}, {file_stem}, {count}" for proper_name, file_stem, count in proper_triples]

    return "\n".join(formatted_triples)

    proper_names_output = create_proper_names_triples(file_path, custom_proper_names_files, bool_include_custom, verbose)
    proper_names_list = [line.split(',')[0] for line in proper_names_output.split('\n')]
    proper_names_list_sorted = sorted(proper_names_list)
    print("\n\nFiltered Proper Names")
    for name in proper_names_list_sorted:
        print(name)
    print(f"Total proper names: {len(proper_names_list_sorted)}")




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
#USAGE: warnings.warn(f"Insert warning message here")


    """
def get_field_value(block, field):
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

    """
def get_all_fields_dict(block):
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

    """
def count_blocks(file_path, heading="## content"):  # quick way is to use find on a field
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

    """
### TOPICS (1,057 tokens)
def extract_topic_counts_triples(qa_file_path, verbose=False):
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


#TODO try on townhall qa files - may need to update for alternate METADATA and CONTENT format
    """
def create_topics_matrix(folder_paths, target_file_path="matrix_topics.csv", suffixpat_include="_qafixed"):
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

    """
def change_topic_in_file(file_path, find_topic, replace_topic):
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

    """
def change_topic_in_folders(folder_paths, find_topic, replace_topic, suffixpat_include="_qafixed"):
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

    """
    def process_file(file_path):
def review_singlet_topic_SONNET(folder_paths, matrix_csv_file_path, starting_letter="a"):
def review_singlet_topic(folder_paths, matrix_csv_file_path, starting_letter="a"):
## primary/corpuses.py (4,846 tokens)
### QA VALIDATION (2,358 tokens)
def validate_stars(stars_str):
def validate_topics(topics_str):
def validate_qa_blocks(blocks_list, required_fields, custom_validators=None):
    """
    from primary.fileops import apply_to_folder
    
    total_replacements = 0
    files_with_replacements = []

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







import os
import re
from collections import defaultdict

from primary.fileops import *

import warnings  # Set the warnings to use a custom format
warnings.formatwarning = custom_formatwarning
#USAGE: warnings.warn(f"Insert warning message here")


    if not stars_str.strip():  # Check if the string is blank or just whitespace
        return True
    try:
        stars = int(stars_str)
        return True  # Accept any integer, including negative numbers
    except ValueError:
        return False  # Return False if the string can't be converted to an integer

    if ",  " in topics_str or re.search(r',(?![ ])', topics_str):
        return False
    topics = re.split(r',\s*', topics_str.strip())
    return all(topic.strip() == topic for topic in topics)

    """
def is_valid_file_qa(file_path, required_fields, custom_validators, verbose=False):
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

    """
def validate_folders_qa(folder_paths, required_fields, custom_validators, suffixpat_include="_qafixed"):
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

    """
### DEUTSCH (615 tokens)
def validate_corpus_deutsch():
def validate_qa_blocks_deutsch_OLD(blocks_list):
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

DEUTSCH_FOLDER_PATHS = ["data/deutsch/f8_done_qafixed_and_vrb", "data/deutsch/f8_qafixed_talks"]
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

    """
### FDA TOWNHALLS (1,866 tokens)
def remove_lines_fda_townhall(text):
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

    """ 
def clean_fda_townhall(file_path):
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

#TODO test after July refactor
    """
def run_clean_on_fda_townhalls(source_folder, destination_folder):
    """
    from primary.fileops import get_heading, set_heading
    from primary.docwork import reformat_transcript_text

    heading = "### transcript"
    text = get_heading(file_path, heading)
    
    cleaned1_text = remove_lines_fda_townhall(text)
    cleaned2_text = reformat_transcript_text(cleaned1_text)
    
    set_heading(file_path, '\n' + cleaned2_text, heading)

#TODO test after July refactor
    """
def run_fix_names_on_fda_townhalls():  # COPY to your run file and use there
def validate_qa_blocks_townhall_OLD(blocks_list):
    """
    from primary.fileops import apply_to_folder, move_files_with_suffix

    apply_to_folder(clean_fda_townhall, source_folder)
    move_files_with_suffix(source_folder, destination_folder, "_cleaned")

#TODO WIP - add path to find_replace_csv after testing fileops func
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

    """
def validate_qa_blocks_townhall(blocks_list):
## primary/aws.py (1,197 tokens)
### AWS S3 (1,192 tokens)
def upload_file_to_s3(file_path, bucket='fofpublic', object_name=None, s3_path=None):
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

    required_fields = ["QUESTION", "ANSWER", "QUESTION SPEAKER", "ANSWER SPEAKER", "TOPICS", "STARS"]
    
    custom_validators = {
        "STARS": validate_stars,
        "TOPICS": validate_topics
    }
    
    return validate_qa_blocks(blocks_list, required_fields, custom_validators)



import boto3
import os
import json
from botocore.exceptions import ClientError, NoCredentialsError

    """
def rename_s3_object(bucket, old_key, new_key, s3_path=None):
    """

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Extract the file name from the file path if object_name is not provided
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Prepend the s3_path if provided
    if s3_path:
        object_name = os.path.join(s3_path, object_name)

    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket, object_name)
        print(f"uploaded {object_name} to {bucket}")
        return object_name

    except FileNotFoundError:
        return None
    except NoCredentialsError:
        print("Credentials not available")

    """
def get_s3_json(bucket, key, s3_path=None):
    """
    s3 = boto3.client('s3', region_name='us-west-2')

    # Adjust keys if s3_path is provided
    if s3_path:
        old_key = f"{s3_path}/{old_key}"
        new_key = f"{s3_path}/{new_key}"
        
    # Copy the old object to the new key
    copy_source = f"{bucket}/{old_key}"
    print(f"Function rename_s3_object is attempting to copy from {copy_source} to {new_key} in bucket {bucket}")
    s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=new_key)
    
    # Delete the old object
    s3.delete_object(Bucket=bucket, Key=old_key)
    print(f"Renamed {old_key} to {new_key} in bucket {bucket}")
    return

    """
## primary/rag_prompts_routes.py (1,789 tokens)
    """
    s3 = boto3.client('s3', region_name='us-west-2')

    # Adjust key if s3_path is provided
    if s3_path:
        key = f"{s3_path}/{key}"

    print(f"Function get_s3_json is attempting to access key: {key} in bucket: {bucket}")

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        json_data = json.loads(response['Body'].read().decode('utf-8'))
        return json_data
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            print(f"No such key: {key} in bucket: {bucket}")
        else:
            print(f"Client error: {e}")
        return None
    except Exception as e:
        print(f"Failed to retrieve {key} from {bucket}: {str(e)}")
        return None



#aws s3api head-object --bucket fofpublic --key deepgram-transcriptions/b4ea528e-4fc8-468a-8320-d5e7f34566b2.json

#old_key = "705a4ad4-b195-4a03-8077-cc7d3881eb1a.json"
#cur_s3_path = 'deepgram-transcriptions'
#json_data = get_s3_json('fofpublic', old_key, cur_s3_path)
#print(f"First characters of received JSON:\n\n{json.dumps(json_data)[:500]}")

#new_key = "fun1.json"
#rename_s3_object('fofpublic', old_key, new_key, s3_path=cur_s3_path)

#cur_file_path='data/pv/meetings_epc/f0_agendas_for_upcoming/2024-05-02_PV-EPC_packet.pdf'
#print(upload_file_to_s3(cur_file_path))




ROUTES_DICT_DEUTSCH_V3 = {
    'routes_dict_name': 'ROUTES_DICT_DEUTSCH_V3',  # mirror global variable name

    'prompt_initial_good_match': 'Given your knowledge of David Deutsch and his philosophy of deep optimism, as well as the QUOTED QUESTIONS AND ANSWERS from Deutsch below, to answer the USER QUESTION below.\n',

    'route_preamble_good_match': 'There is a good match of your question in David Deutsch\'s interviews. See his QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with David Deutsch\'s philosophy and your exact question.',

    'prompt_initial_partial_match': 'Given your knowledge of David Deutsch and his philosophy of deep optimism, as well as the QUOTED QUESTIONS AND ANSWERS from Deutsch below, to answer the USER QUESTION below.\n',

    'route_preamble_partial_match': 'There is a partial match of your question in David Deutsch\'s interviews. See his QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with David Deutsch\'s philosophy and your exact question.',

    'prompt_initial_no_match': 'Given your knowledge of David Deutsch and his philosophy of deep optimism, answer the USER QUESTION below.\n',

    'route_preamble_no_match': 'Your question is not addressed in David Deutsch\'s interviews. No QUOTED QUESTIONS AND ANSWERS are therefore provided but here is an AI ANSWER that synthesizes David Deutsch\'s philosophy and your question.',

    'quoted_qa_single': 'QUOTED QUESTION: {top_sim_question}\nQUOTED SOURCE: {top_sim_source}\nQUOTED TIMESTAMP: {top_sim_timestamp}\nQUOTED ANSWER: {top_sim_answer}\n{top_sim_display}\n\n',

    'quoted_qa_double': 'QUOTED QUESTION 1: {top_stars_question}\nQUOTED SOURCE 1: {top_stars_source}\nQUOTED TIMESTAMP 1: {top_stars_timestamp}\nQUOTED ANSWER 1: {top_stars_answer}\n{top_stars_display}\n\nQUOTED QUESTION 2: {top_sim_question}\nQUOTED SOURCE 2: {top_sim_source}\nQUOTED TIMESTAMP 2: {top_sim_timestamp}\nQUOTED ANSWER 2: {top_sim_answer}\n{top_sim_display}\n\n',

    'user_ai_qa': 'USER QUESTION: {user_question}\n\nAI ANSWER: '
}

ROUTES_DICT_FDA_TOWNHALLS_V1 = {
    'routes_dict_name': 'ROUTES_DICT_FDA_TOWNHALLS_V1',  # mirror global variable name

    'prompt_initial_good_match': 'Given your knowledge of FDA regulations and policies related to in vitro diagnostic testing and more specifically emergency use authorization tests for SARS-CoV-2 during the COVID public health emergency, as well as the QUOTED QUESTIONS AND ANSWERS from FDA townhalls below, answer the USER QUESTION below.\n',

    'route_preamble_good_match': 'There is a good match of your question in the FDA COVID testing townhall transcripts. See the QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with FDA policies and your exact question.',

    'prompt_initial_partial_match': 'Given your knowledge of FDA regulations and policies related to in vitro diagnostic testing and more specifically emergency use authorization tests for SARS-CoV-2 during the COVID public health emergency, as well as the QUOTED QUESTIONS AND ANSWERS from FDA townhalls below, answer the USER QUESTION below.\n',

    'route_preamble_partial_match': 'There is a partial match of your question in the FDA COVID testing townhall transcripts. See the QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with FDA policies and your exact question.',

    'prompt_initial_no_match': 'Given your knowledge of FDA regulations and policies related to in vitro diagnostic testing and more specifically emergency use authorization tests for SARS-CoV-2 during the COVID public health emergency, answer the USER QUESTION below.\n',

    'route_preamble_no_match': 'Your question is not directly addressed in the FDA COVID testing townhall transcripts. No QUOTED QUESTIONS AND ANSWERS are therefore provided but here is an AI ANSWER that synthesizes FDA policies and your question.',

    'quoted_qa_single': 'QUOTED QUESTION: {top_sim_question}\nQUOTED SOURCE: {top_sim_source}\nQUOTED TIMESTAMP: {top_sim_timestamp}\nQUOTED ANSWER: {top_sim_answer}\n{top_sim_display}\n\n',

    'quoted_qa_double': 'QUOTED QUESTION 1: {top_stars_question}\nQUOTED SOURCE 1: {top_stars_source}\nQUOTED TIMESTAMP 1: {top_stars_timestamp}\nQUOTED ANSWER 1: {top_stars_answer}\n{top_stars_display}\n\nQUOTED QUESTION 2: {top_sim_question}\nQUOTED SOURCE 2: {top_sim_source}\nQUOTED TIMESTAMP 2: {top_sim_timestamp}\nQUOTED ANSWER 2: {top_sim_answer}\n{top_sim_display}\n\n',

    'user_ai_qa': 'USER QUESTION: {user_question}\n\nAI ANSWER: '
}

#For VRAG, Langchain CONDENSE_QUESTION_PROMPT is processed to give prompt_template in rag.py

PROMPT_VRAG_DEUTSCH_V1 = """Placeholder
"""

PROMPT_VRAG_FDA_TOWNHALLS_V1 = """Placeholder
"""


PROMPT_TEMPLATE_DEUTSCH2_LONG = """In your responses, adhere rigorously to the worldview and philosophy outlined in the provided summary. Utilize the corpus of David Deutsch's books and interviews as additional context to enrich your answers. However, ensure that your responses are in complete alignment with the worldview summary.
"""

PROMPT_TEMPLATE_DEUTSCH_SMALL = """In crafting your responses, adhere closely to the ideology presented in the provided summary, which emphasizes several key principles:
"""

PROMPT_TEMPLATE_FDA_BASIC = """In creating your response, use the information from these question and answer sessions provided by the FDA and take the best and closest response and reply with a synthesis of that plus any knowledge you have of FDA Diagnostics Regulation.