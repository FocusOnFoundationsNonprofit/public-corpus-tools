all_source_defs_docstring (88,320 tokens)


## primary/fileops.py (8,089 tokens)
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
### SUFFIX (680 tokens)
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
    Renames the actual file - substitutes the suffix in the file name of the given file path with a new suffix.
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
### READ WRITE (876 tokens)
def read_complete_text(file_path):  # UPDATED 11-18-24 to use UTF-8 encoding
    """
    Reads the entire text from a file using UTF-8 encoding.

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
### JSON (398 tokens)
def pretty_print_json_object(json_obj, level_limit=None, print_values=False):
    """
    Prints the structure of a JSON object with colored output for different levels.

    :param json_obj: dict or list, the JSON object to print.
    :param level_limit: int, the maximum level of nesting to print. None means no limit.
    :param print_values: bool, whether to print values at leaf nodes.
    :return: list, the output lines generated (without color).
    """
    def print_json_structure(data, indent=0, parent_key='', level=0):
def pretty_print_json_file(json_file_path, level_limit=None, save_to_file=False):
    """
    Prints the structure of a JSON file and optionally saves it to a file with a '.pretty' extension.

    :param json_file_path: string, path to the json file.
    :param level_limit: int, the maximum level of nesting to print. None means no limit.
    :param save_to_file: bool, whether to save the output to a file.
    :return: None.
    """
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
### MISC FILE (1,542 tokens)
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
def find_and_replace_in_filenames_in_folder(folder_path, find_str, replace_str, suffixpat_include=None, suffixpat_exclude=None, include_subfolders=False):
    """
    Finds and replaces strings in filenames within the specified folder.
    Optionally filters by suffix pattern and includes subfolders.

    :param folder_path: string of the path to the folder where filenames will be processed.
    :param find_str: string to find in the filenames.
    :param replace_str: string to replace the found string with.
    :param suffixpat_include: string of the suffix pattern that included files must have.
    :param suffixpat_exclude: string of the suffix pattern that files must not have to be included.
    :param include_subfolders: boolean indicating whether to include files from subfolders.
    :return: integer representing the number of files renamed.
    """
def find_line_number_in_file(file_path, search_text):  # no unittests yet
    """
    Finds the line number where the specified text first appears in the file.

    :param file_path: string, the path to the file to search.
    :param search_text: string, the text to search for.
    :return: int, the line number where the text was found (1-based), or None if not found.
    """
### TIME AND TIMESTAMP (1,137 tokens)
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
    Changes a given timestamp by a specified number of seconds.

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :param delta_seconds: integer representing the number of seconds to change the timestamp by.
    :return: string representing the new timestamp after the change.
    """
def tune_timestamp(timestamp, delta_seconds=None):
    """
    Converts a given timestamp to a standard format with respect to digits and leading zeros.
    Optionally shifts the timestamp by a specified number of seconds.

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :param delta_seconds: integer representing the number of seconds to shift the timestamp by. Default is None.
    :return: string representing the tuned timestamp or None if the input timestamp is None.
    :raises ValueError: if delta_seconds is provided but is not an integer.
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
def track_progress(current_count, total_count, start_time, last_percentage=0, item_name="items"):
    """
    Tracks and reports progress for iterative operations.
    Reports at 2%, 5%, and every 10% thereafter, skipping early percentages if item count is too small.
    
    :param current_count: int, current number of items processed
    :param total_count: int, total number of items to process
    :param start_time: float, start time from time.time()
    :param last_percentage: int, last reported percentage (for internal tracking)
    :param item_name: str, name of items being processed (default "items")
    :return: int, updated last_percentage
    :raises ValueError: if total_count is zero
    """
### TIMESTAMP LINKS (425 tokens)
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
def redo_timestamp_links_with_delta_seconds(file_path, delta_seconds):  # no unittests
    """
    Redoes the timestamp links with a delta seconds added to the original timestamp.
    
    :param file_path: string, the path to the file where timestamp links will be redone.
    :param delta_seconds: integer, the number of seconds to add to each timestamp.
    :return: none
    """
### FIND AND REPLACE (708 tokens)
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
    Usage - cur_find_replace_pairs = [("Mervin Praison", "John Smith"), ("Summary", "Tamagotchi")]

    :param file_path: string, the path to the file where the find and replace operations will be performed.
    :param find_replace_pairs: list of tuples, each containing a string or regex pattern to be found and a string to replace it with.
    :param use_regex: boolean for whether to use regex patterns for finding. Default is False (use exact string matching).
    :return: int, the total number of replacements made.
    """
def parse_csv_for_find_replace(csv_file):
    """
    Parses a CSV file to extract find and replace pairs.
    Handles two formats for find/replace pairs:
    1. Unquoted strings: Leading and trailing spaces are stripped
    2. Single-quoted strings ('): Preserves all spaces between the quotes
    
    Example CSV content:
    find, replace
    hello  ,  world     # -> ("hello", "world")
    'hello  ', 'world ' # -> ("hello  ", "world ")
    
    :param csv_file: string, path to the CSV file containing find/replace pairs.
    :return: list of tuples, each containing (find_string, replace_string).
    """
def process_find_replace_pair(find_str, replace_str):
    """
    Helper function to process a find/replace pair based on whether they use quotes.
    Both strings must use the same format (either both quoted or both unquoted).
    
    :param find_str: string, the string to find.
    :param replace_str: string, the string to replace with.
    :return: tuple of (processed_find_str, processed_replace_str).
    :raises ValueError: if one string is quoted and the other isn't.
    """
def find_and_replace_from_csv(folder_path, find_replace_csv, suffixpat_include=None, include_subfolders=False, verbose=False):
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
### HEADINGS (923 tokens)
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
def delete_all_heading_instances(file_path, heading):
    """
    Deletes all instances of the specified markdown heading and their following text, including subheadings.
    Stops at headings of equal or higher level (fewer or same number of '#' characters).

    :param file_path: string, the path to the file from which the headings will be deleted.
    :param heading: string, the markdown heading to be deleted, including the '#' characters and the following space.
    """
### METADATA (745 tokens)
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
def set_last_updated(file_path, new_last_updated_value, prepend_today=True):
    """
    Updates the 'last updated' metadata field in a file with a new value.

    :param file_path: string, the path to the file to be updated.
    :param new_last_updated_value: string, the new value for the 'last updated' metadata field.
    :param prepend_today: boolean, if True, today's date is prepended to the new_last_updated_value. Default is True.
    :return: None
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

## primary/transcribe.py (5,529 tokens)
### YOUTUBE (1,189 tokens)
def get_authenticated_service():
    """
    Creates an authenticated YouTube service with OAuth2.
    Handles token creation and refresh.
    """
def download_mp3_from_youtube(url, output_title='audio_download', output_dir='data/audio_inbox', skip_download=False, max_retries=10):
    """
    Downloads a YouTube video as MP3 audio file.

    :param url: string of the YouTube URL to download from.
    :param output_title: string of the title to save the audio file as (must not contain path separators).
    :param output_dir: string path to directory where audio will be saved. Default 'data/audio_inbox'.
    :param skip_download: boolean to skip download if file exists. If False, will delete existing file and start download.
    :param max_retries: int number of times to retry download on failure.
    :return: string of the path to the saved MP3 file.
    :raises ValueError: if output_title contains path separators.
    """
def get_youtube_title_length(url):
    """ 
    Retrieves the title and duration of a youtube video in a formatted timestamp.

    :param url: string of the youtube url to retrieve information from.
    :return: tuple containing the video title and its duration as a string in a formatted timestamp.
    """
def download_link_list_to_mp3s(links, output_dir="data/audio_inbox", skip_download=False):  # NO CALLERS (3-3 RT)
    """
    Downloads a list of youtube links as mp3 files to a specified directory and stores the link-title pairs. Uses yt_dlp package.
    Calls download_mp3_from_youtube

    :param links: list of youtube links to be downloaded.
    :param output_dir: string of the directory path where the audio files will be saved.
    :return: dictionary mapping each youtube link to its corresponding title.
    """
def download_youtube_subtitles_url(subtitle_url): # DS, cat 1, omit unittests since called by next function
    """
    Downloads and extracts subtitle text from a given YouTube subtitle URL.
    Helper function to that is called from get_youtube_subtitles
    
    :param subtitle_url: string of the url from which subtitles are to be downloaded.
    :return: string of the extracted subtitle text, spaces between segments and stripped of new lines.
    """
def get_youtube_subtitles(url):  # 1-18 no longer working - uses yt-dlp
    """
    Retrieves English subtitles for a given YouTube video URL if available. Uses yt_dlp package.
    
    :param url: string of the youtube video url.
    :return: subtitles as a string if found, otherwise None.
    """
def get_youtube_subtitles_oauth(url):  # added 1-18 but does not work
    """
    Retrieves English subtitles or closed captions for a YouTube video.
    Tries manual subtitles first, falls back to auto-generated captions if needed.
    
    :param url: string of the youtube video url.
    :return: tuple of (subtitle text as string, source type as string) or (None, None) if not found.
    """
def parse_duration(duration_str):
    """
    Parse ISO 8601 duration format to timedelta.
    Example: 'PT1H2M10S' -> 1 hour, 2 minutes, 10 seconds

    :param duration_str: string of ISO 8601 duration format.
    :return: string of formatted duration.
    """
def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    Only accepts exact matches of standard YouTube URL formats.

    :param url: string of the youtube url.
    :return: string of the video ID or None if not found.
    """
def get_youtube_all(url):
    """
    Retrieves all available information from a YouTube video URL using YouTube Data API v3.
    
    :param url: string of the youtube video url.
    :return: dictionary with video details or None if the URL is invalid.
    """
def is_valid_youtube_url(url):
    """ 
    Determine if a string of url is a valid YouTube URL by checking video ID format
    and making an API call to verify the video exists.

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
### JSON AND TRANSCRIPT SUPPORT (736 tokens)
def get_media_length(file_path_or_url):
    """
    Retrieves the length (duration) of a media file or a YouTube video.
    For a local file, it returns the duration in seconds.
    For a YouTube video, it returns the duration in our tuned timestamp format.

    :param file_path_or_url: Path to a local media file or a URL to a YouTube video.
    :return: length (duration) of the media in seconds (for local files) or in our tuned timestamp format (for YouTube videos).
    """
def add_link_to_json_metadata(json_file_path, link):
    """ 
    Add a hyperlink to the JSON file under the 'metadata' section.

    :param json_file_path: string, the path to the JSON file to be modified.
    :param link: string, the hyperlink to be added to the JSON file.
    :return: tuple, the path to the modified JSON file and None if successful, or None and an exception if an error occurs.
    """
def get_link_from_json_metadata(json_file_path):
    """ 
    Retrieve the hyperlink from the 'metadata' section of a JSON file.

    :param json_file_path: string, the path to the JSON file from which the hyperlink is to be retrieved.
    :return: string or None, the hyperlink if found in the JSON file's 'metadata' section, otherwise None.
    """
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
### DEEPGRAM ALTERNATIVES (489 tokens)
def test_deepgram_client():  # omit unittests
    """
    Tests the Deepgram client initialization with the provided API key and prints a success or failure message.
    Raises ValueError if test fails.
    """
def transcribe_deepgram_sync(audio_file_path, model):
    """ 
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription, accpets deepgram api call model or our suffix version (see below).
    :return: a dictionary containing the transcription results.
    """
def transcribe_deepgram_sync_sdk_prerecorded(audio_file_path, model):
    """
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model, utilizing the SDK.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :return: path to the JSON file containing the transcription results.
    """
def transcribe_deepgram_callback_lambda(audio_file_path, model, callback_url=DG_CALLBACK_URL):  # old version using deepfram-callback lambda function - deprecated for presigned s3
    """
    Transcribes the given audio file using the specified Deepgram model asynchronously with a callback URL.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :param callback_url: URL to which Deepgram will send the transcription results.
    :return: Request ID from Deepgram indicating that the file has been accepted for processing.
    """
def transcribe_deepgram_callback_lambda_sdk_prerecorded(audio_file_path, model, callback_url=DG_CALLBACK_URL):
    """
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model,
    utilizing the SDK and callback functionality.

    :param audio_file_path: Path to the audio file to be transcribed.
    :param model: The Deepgram model to use for transcription.
    :param callback_url: The callback URL where Deepgram will send the transcription result.
    :return: Tuple containing the request_id, base_audio_file_name, and model.
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
### TRANSCRIBE WRAPPER (1,177 tokens)
def create_transcript_md_from_json(json_file_path, combine_segs=True):
    """
    Creates a markdown transcript from a JSON file containing Deepgram transcription data.
    If combine_segs is True, combines consecutive segments from the same speaker.

    :param json_file_path: string of the path to the json file containing transcription data.
    :param combine_segs: boolean indicating whether to combine consecutive segments from the same speaker.
    :return: string of the path to the created markdown file or None if the json file is not valid.
    """
def process_deepgram_transcription_sync(title, link, model, output_dir="data/audio_inbox", skip_download=False):  # unittests 1 TEMP SKIPPED
    """
    Processes a Deepgram transcription from a YouTube video link by downloading the audio, transcribing it, and creating a markdown transcript.

    :param title: the title of the video used to name the downloaded audio file.
    :param link: the YouTube link to the video to be transcribed.
    :param model: the Deepgram model used for transcription.
    :param output_dir: the directory path where the audio file will be downloaded.
    :param skip_download: if True, will use existing audio file instead of redownloading.
    :return: the path to the created markdown file or None if transcription fails.
    """
def process_deepgram_transcription_sync_from_audio_file(audio_file_path, link, model):  # unittests 1 TEMP SKIPPED
    """ 
    Transcribes an audio file using the Deepgram service, adds the YouTube link to the transcription, creates a markdown transcript, and assigns speaker names.

    :param audio_file_path: string of the path to the audio file to be transcribed.
    :param link: string of the youtube link to be added to the transcription json.
    :param model: string of the deepgram model to be used for transcription.
    :return: string of the path to the markdown file with the completed transcription or None if transcription fails.
    """
def transcribe_deepgram_callback_presigneds3(audio_file_path, model):
    """
    Upload the local audio file to S3 (if not already there).
    Generate a GET presigned URL for Deepgram to read it,
    Generate a PUT presigned URL for Deepgram to write the transcript
    (with a name derived from the audio filename + model suffix),
    and kick off the asynchronous transcription with callback=PUT.

    :param audio_file_path: Local path to the audio file
    :param model: Deepgram model, e.g. 'nova', mapped by DG_MODEL_SUFFIX_MAP
    :return: (request_id, transcript_s3_key, base_audio_file_name, s3_bucket)
    """
def process_deepgram_transcription_callback_presigneds3(title, link, model, output_dir="data/audio_inbox", audio_file_path=None):
    """
    Download or reuse local audio, then send it to Deepgram with presigned S3 callback.
    Write a "waiting file" with everything needed to later retrieve the final transcript from S3.

    :param title: The title (for naming local waiting file).
    :param link: The YouTube link (for metadata).
    :param model: The Deepgram model key (maps to suffix).
    :param output_dir: Where to store local audio + waiting file.
    :param audio_file_path: If provided, skip YouTube download and use this local file.
    :return: The path to the created waiting file.
    """
def download_deepgram_callback_waiting(local_folder="data/audio_inbox", prefix="WAITING-CALLBACK_"):
def process_multiple_videos(videos_to_process, model='both', bool_callback=True, bool_youtube=True):  # unittests 1 MOCK
    """
    Processes multiple videos by transcribing them and creating YouTube markdown files if bool_youtube is True.

    :param videos_to_process: list of tuples containing the title and link of each video to be processed.
    :param model: string of the deepgram model to be used for transcription. 'both' will run both whisper-medium and nova-2-general models.
    :param bool_callback: boolean indicating whether to use callback transcription. Defaults to True.
    :param bool_youtube: boolean indicating whether to create YouTube markdown files. Defaults to True.
    :return: None
    """
def check_for_waiting_files(local_folder="data/audio_inbox", prefix="WAITING-CALLBACK_"):
    """
    Checks if there are any waiting files in the specified folder with the given prefix.
    
    :param local_folder: string of the path to check for waiting files. Defaults to "data/audio_inbox"
    :param prefix: string prefix of waiting files to look for. Defaults to "WAITING-CALLBACK_"
    :return: boolean indicating whether any waiting files were found
    """
def schedule_recurring_task(interval_minutes, check_function, work_function, max_runs=1, run_immediately=True):
    """
    Schedules a recurring task that runs work_function when check_function returns True.
    Can be configured to perform an immediate first check and terminate after a specific number of executions.

    :param interval_minutes: Number of minutes between checks
    :param check_function: Function that returns a boolean indicating whether work_function should run
    :param work_function: Function to execute when check_function returns True
    :param max_runs: Maximum number of times to run work_function before terminating. None for infinite runs
    :param run_immediately: Whether to perform an immediate check before starting the schedule. Defaults to True
    :return: None
    """
    def job():

## primary/llm.py (34,993 tokens)
### PRINT AND TOKENS (1,007 tokens)
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
def get_o1_cost_from_response(response, verbose=True):
    """
    Get the cost of an o1 response from the response object.

    :param response: dict, the response object from an o1 API call containing usage information
    :param verbose: boolean, whether to print detailed cost breakdown
    :return: float, total cost of the API call in dollars
    """
def mtest_get_o1_cost_from_response():
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
def group_segments_token_cap(segments, token_cap=1000):
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
### OPENAI LLM (662 tokens)
def generate_openai_testcurl_command():
    """
    Generates a single-line curl command for testing the OpenAI API connection.
    Prints the command to the console for easy copy-pasting.
    """
def get_openai_models(api_key):
def mrun_get_openai_models():
def test_openai_chat(model=OPENAI_MODEL):
def openai_chat_completion_request(messages, tools=None, tool_choice=None, model=OPENAI_MODEL):  # APIMOCK unittests 2
    """
    Send a chat completion request to the OpenAI API with the provided messages and optional tools and tool choice.

    :param messages: a list of message dictionaries to send in the chat completion request
    :param tools: optional list of tools to include in the request
    :param tool_choice: optional tool choice to include in the request
    :param model: the model to use for the chat completion request
    :return: the response object from the OpenAI API request
    """
def openai_chat_completion_request_sdk(messages, model=OPENAI_MODEL, tools=None, tool_choice=None, reasoning_effort=None, temperature=None, max_completion_tokens=None):
    """
    Send a chat completion request using the OpenAI SDK.

    :param messages: list of message dictionaries
    :param tools: optional list of tools
    :param tool_choice: optional tool choice
    :param model: the model to use
    :param reasoning_effort: optional float to control model reasoning effort
    :param temperature: optional float to control randomness
    :param max_completion_tokens: optional int to limit response length
    :return: the response object from the OpenAI API
    """
def simple_openai_chat_completion_request(prompt, model):  # no unittests
def openai_function_call(prompt, content, tools, model=OPENAI_MODEL, verbose=False):
    """
    Send a function call request to the OpenAI API and process the response.

    :param prompt: str, system prompt to set context for the model
    :param content: str, user content to send to the model
    :param tools: list, function definitions for tool calling
    :param model: str, OpenAI model to use for completion
    :param verbose: bool, whether to print debug information
    :return response: str or dict, processed response from the API. Fields are in tool_calls[0].function.arguments
    """
                    "description": """
                    Create a two-line rhyming poem based on the content of the input text. The rhyme should capture the key message or theme while maintaining a playful, poetic style. Each line should be grammatically complete and naturally flow into the next. The rhyming words should appear at the end of each line. Keep the language simple and accessible while staying true to the original meaning.
                    """,
                    "description": """
                    The timestamp corresponding to the start of the speaker dialogue in the format H:MM:SS or MM:SS or M:SS (chose whichever is present in the input text). This timestamp is crucial for contextualizing the answer within the transcript and must be accurate to reflect the exact moment the response begins.
                    """,
### ANTHROPIC LLM (727 tokens)
def anthropic_chat_completion_request(messages, model=ANTHROPIC_MODEL, system=None, tools=None, max_tokens=4096, temperature=0.7):
    """
    Make a chat completion request to Anthropic's API.

    :param messages: List of message objects representing the conversation
    :param model: The model to use for the completion
    :param system: System message to set the behavior of the assistant
    :param tools: optional list of tools for function calling
    :param max_tokens: Maximum number of tokens to generate (default: 4096)
    :param temperature: Controls randomness in the output (0 to 1, default: 0.7)
    :return: The complete message response object from Anthropic
    """
def simple_anthropic_chat(prompt, model=ANTHROPIC_MODEL):
    """
    Simplified version of chat completion that takes a single prompt string.

    :param prompt: str, the prompt to send to the model
    :param model: str, the model to use
    :return: str, the generated response content
    """
def anthropic_function_call(prompt, content, tools, model=ANTHROPIC_MODEL, verbose=False):
    """
    Send a function call request to the Anthropic API.

    :param prompt: str, system prompt to guide the model's behavior
    :param content: str, the content to process
    :param tools: list of tools/functions available for the model
    :param model: str, the model to use
    :param verbose: bool, whether to print detailed information
    :return: The complete function call response or None if an error occurs. Fields are in content[1].input 
    """
                    "description": """
                    Create a short, family-friendly dad joke based on the content of the input text. The joke should be in a classic setup-punchline format, incorporating elements from the input while maintaining the groan-worthy charm typical of dad jokes. Keep it simple, clean, and ideally related to the topic at hand.
                    """,
                    "description": """
                    The timestamp corresponding to the start of the speaker dialogue in the format H:MM:SS or MM:SS or M:SS (chose whichever is present in the input text). This timestamp is crucial for contextualizing the answer within the transcript and must be accurate to reflect the exact moment the response begins.
                    """,
def parse_function_call_response(response, provider="openai"):
    """
    Parse function call response from different providers into a common format.
    
    :param response: The raw response from the API
    :param provider: str, either "openai" or "anthropic"
    :return: dict containing the parsed function arguments or None
    """
def convert_tools_to_anthropic_format(openai_tools):
    """
    Convert OpenAI tool format to Anthropic format.
    
    :param openai_tools: list of tools in OpenAI format
    :return: list of tools in Anthropic format
    """
def simple_anthropic_chat_rawapi(prompt, model=ANTHROPIC_MODEL):  # Not currently used
    """
    Make a simple chat completion request to Anthropic's API.

    :param prompt: String containing the user's prompt or message
    :param model: String specifying the Anthropic model to use
    :return: String containing the generated message content, or an error message if the request fails
    """
### LLM PROCESSING (867 tokens)
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
### LLM TRANSCRIPT PROCESSING (3,435 tokens)
PROMPT_SUMMARIZE_3_KEYWORDS = """
Summarize the text after the speaker line as 3 keywords that best captures what is said.
Return the new key word line as the next line directly underneath the speaker line.
"""
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
- Use double quotation marks if the speaker is quoting someone's words (e.g., Popper said, "Science must begin with myths, and with criticism of myths.").
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
### QA GENERATION (1,144 tokens)
FCALL_PROMPT_QA_DIALOGUE_STATEDQA = """
You are an expert text analyzer that is trained in identifying stated questions and answers in transcripts of dialogue. You will be given blocks of dialogue and your role is to return extracted question and answer pairs that faithfully capture the meaningful content in the dialogue, while removing filler words and minimally modifying the text for clarity and readability. You will use your tool to only return exact JSON in the format specified.
"""
FCALL_PROMPT_QA_DIALOGUE_ORIGQUERY = """
The question should capture the essence of the original query posed by the interviewer in a simplified, generic form. It should focus on the core topic or idea, removing extraneous contextual details. The modified question should have semantic alignment with {speaker}'s answer. The question should be rephrased for a third-person audience, ensuring it is generalized and does not include direct references to {speaker}. DO NOT mention the name {speaker} in the question.
""" 
FCALL_PROMPT_QA_DIALOGUE_FROMANSWER = """
You are an expert text analyzer that is trained in identifying questions or implied questions. You will be given dialogue and your role is to return a create a general, simple question from the provided answer of the speaker {speaker}. This created general question may or may not be related to the question actually asked in the dialogue preceding the answer. The created general question will be part of a question and answer set used for Retrieval Augmented Generation. The question must not mention any speaker names. You will use your tool to only return exact JSON in the format specified.
"""
FCALL_PROMPT_QA_DEUTSCH = """
You are an expert text analyzer that is trained in identifying questions or implied questions. You will be given dialogue and your role is to return a create a general, simple question from the provided answer. This created general question may or may not be related to the question actually asked by the speaker in the dialogue preceding the answer. The created general question will be part of a question and answer set used for Retrieval Augmented Generation. The question must not mention the speaker name. The question should be written in such a way that it assumes that the answer provided is the best knowledge humanity has about this topic at present moment.  Some specific phrases to use include: 1) 'multiverse quantum theory' - rather than 'many-worlds interpretation of quantum'. You will use your tool to only return exact JSON in the format specified. 
"""
CUSTOM_INSTRUCTIONS_DEUTSCH_GENERALQ = """
Analyze the following passage and create a general, simple question for which the answer will be the response. This will be part of a question and answer set such that new questions are compared against the questions, and answers retrieved. The question should not mention the author, or David Deutsch. The question should be written in such a way that it assumes that the answer provided is the best knowledge humanity has about this topic at present moment. Use the phrase 'multiverse quantum theory' rather than 'many-worlds interpretation of quantum'
"""
def tools_qa_speaker(speaker):
    """
    Generate a list of tools for question and answer extraction based on the speaker's response.

    :param speaker: string of the speaker's name whose responses are being analyzed
    :return: list of dictionaries containing tool configurations for QA extraction
    """
                    "description":f"""
                    You are an expert text analyzer that is trained in identifying questions or implied questions. You will be given dialogue and your role is to return a create a general, simple question from the provided answer of the speaker {speaker}. This created general question may or may not be related to the question actually asked in the dialogue preceding the answer. The created general question will be part of a question and answer set used for Retrieval Augmented Generation. The question must not mention any speaker names. You will use your tool to only return exact JSON in the format specified.
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
### QA INCREMENTAL (1,329 tokens)
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCTIPRT_FDA_TOWNHALLS_1 = """
    You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue. 
    Your role is to extract and clarify the next question-answer pair from the given transcript chunk.
    The previous question-answer pair is provided in both the original text verbatim version and in a modified clarified version.

    Your task is identify the next important information that comes after the previous question-answer pair. This important information may comprise an explicit question asked by a speaker, or it may not and instead be a standalone statement.
    A requirement for qualification as important information of a next question-answer pair is that it is not included in the verbatim_answer property of the provided previous question answer pair.
     
    Identify the speakers for both questions and answers. Speakers are identified on separate lines of text that precede the speaker dialogue. The speaker lines end in either just a colon, or a timestamp which optionally be followed by a timestamp link. Speaker lines will start with the speaker name, or a surrogate string such as 'Moderator'. The speaker name may be followed by a role provided in parentheses. The role may comprise or contain text that specifies that speaker as an 'Authority Speaker'. See below for the text that specifies Authority Speakers.
    
    If important information is provided by a speaker identified as an Authority Speaker (see below), and that important information is not explicitly asked as a question, then you will generate a clarified question that is the best suitable question to be paired with that important information. The important information will be considered the answer. If a statement is made by a Non-Authority Speaker, and that statement is not phrased as a question, then it must be acknowledged by an Authority Speaker with an explicit affirmation response. See property descriptions below for values to use in this case where there is no explicit verbatim question.

    You will extract both the verbatim_answer from the transcript text, and then process the verbatim_answer to create the clarified_answer. The clarified_answer may be similar or perhaps even identical to the verbatim_answer from the transcript text. Typically the clarified answer wil be modified and therefore different at least to some extent from the verbatim_answer, however the clarified_answer must NEVER contradict the corresponding verbatim_answer and must ALWAYS have the same meaning. You will create the clarified versions of the question and answer by removing filler words to improve clarity and readability.

    This specific corpus comprises transcripts of the dialogue from virtual townhall meetings held by the United States Food and Drug Administration (FDA) to help answer technical questions about the development and validation of tests for the virus SARS-CoV2, and the updated policy on COVID-19 diagnostics policy for diagnostics test for coronavirus disease 2019 during the public health emergency caused by the COVID-19 global pandemic.

    Authority Speakers in this FDA Townhall Transcript Corpus are specified by the inclusion of the string 'FDA' in the role portion of the speaker line.

    The criteria for qualification for important information to be extracted as question-answer pairs is that the information be technical in nature, procedural, or legal. Information that should not be considered important and excluded from the question-answer extraction process is information related to the orchestration of the call such as which caller or speaker is being selected by the moderator. Information, whether questions by call-in speakers or answers by FDA staff, that is related to whether the FDA authorities can answer the question are considered to be legal and always to be included. These typical include answers from the FDA Authority Speakers similar to 'we are not able to respond to questions about specific submissions that might be under review'. If you are not sure whether information qualifies as important information, then includeit and set the review_flag property of the response to True.
    """
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_2 = """
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
def tools_qa_incremental_2():
### **Output Format Example** (7,576 tokens)
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_F = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics. Your role is to extract the **next** relevant question-answer pair from the given transcript chunk, while also identifying its location within the text with precision. This is an incremental process: each time you produce a QA pair, you must identify exactly which characters in the transcript it corresponds to, so that subsequent requests can continue from beyond that position without overlap or duplication.

Your **primary goals** when extracting each question-answer pair:
1. **Prevent Duplication**  
   - Each transcript chunk should yield at most one new or distinct Q&A if it involves the same question, the same speaker, or the same snippet previously captured.
   - If the text is essentially continuing or clarifying the same question-answer pair (same speaker, same context, no new question asked), do not produce a separate QA pair. Instead, merge it into the previous QA or skip it.
   - Skip or merge any "implied" question if it simply rehashes a previously extracted question or answer. Do not produce multiple QAs for repeated or partial references to the same question or the same speaker's statement.

2. **Identify & Label Speakers and Their Roles**  
   - For example, use "Tim Stenzel (FDA IVD Director):" or "Shannon Clark (UserWise Consulting):".  
   - If a speaker's question is truly separate, it should become a distinct QA pair. If it is a minor clarifying follow-up, merge it into the previous QA if possible.

3. **Capture Verbatim Text on a Single Line**  
   - Provide a "VERBATIM QUESTION" and "VERBATIM ANSWER" as continuous text without line breaks or extra speaker labels embedded inside. Eliminate "um," "uh," repeated words, or crosstalk noise only if they disrupt clarity; otherwise, keep the text as close to verbatim as possible.
   - Provide a "CLARIFIED QUESTION" and "CLARIFIED ANSWER" that rephrase or clean up the language for clarity, **but do not** change the meaning.
   - If the speaker never actually asks a question but is giving new, important regulatory or legal info not captured in a prior QA pair, you may label it as "IMPLIED QUESTION" / "IMPLIED ANSWER." However, do this only if it is clearly a separate, substantive piece of info that was not already covered. Do not produce multiple implied questions for partial or repeated quotes from the same speaker or the same text chunk.

4. **Location Reporting (Transcript Start/End Positions)**  
   - Precisely identify the start and end character positions in the provided transcript for each **verbatim** question and answer.  
   - Ensure these positions align exactly with the extracted text, so future incremental requests can skip ahead to the next chunk.

5. **Exclusions & Focus**  
   - **Exclude** housekeeping/orchestration and meeting management (e.g., "next steps in the meeting", "Moderator," "Coordinator" instructions about lines being muted, "press star-1," teleconference issues, or feedback survey reminders).  
   - **Exclude** repeated disclaimers that "FDA can't speak about specific submissions under review."  
   - **Focus** on technical, procedural, or legal content about COVID-19 diagnostics, test development, validation, labeling, and regulatory processes.

6. **One QA per Speaker Turn**
   - By default, a single speaker's turn (plus any immediate FDA response) should become one QA pair unless the speaker explicitly asks multiple distinct questions.
   - If the same speaker's turn includes meandering or repeated questions, condense them into one QA if they address the same overall topic.
   - Example: If a speaker says: "I have a question about in silico cross-reactivity. Also, do we need new data for interfering substances?" treat that entire turn as one question.

7. **Minor Clarifications or Follow-Ups**
   - If a speaker or the FDA official continues talking but does not pose a new distinct question, do not create a new QA pair.
   - If it's simply clarifying the same question (e.g., a short "Yes, exactly" or "That's correct"), merge it into the existing QA pair or skip if it adds no new regulatory content.

8. **Incremental Approach & Avoiding Over-Segmentation**  
   - After extracting one QA pair, you stop at the exact "TRANSCRIPT END POSITION." The next time a request is made, you begin looking for a new question or important statement from that end position forward.
   - Do not break out small or partial phrases from the same speaker answer or question into multiple QA pairs. If the question or answer is continuous (no separate speaker turn), it's a single QA.
   - If it was partially extracted previously, skip it unless the newly revealed text truly adds a completely new question or significant content.

9. **Minimize Implied Q&A**
   - If you already extracted a Q&A covering the same statement from an Authority Speaker, do not create a second "implied Q&A."
   - If the statement is basically repeating prior FDA guidance (e.g., "We are open to off-label use…" repeated), skip or merge it.

10. **Review Flag**  
    - If you are uncertain whether a piece of information is important enough to become a question-answer pair, include it, but set "REVIEW FLAG: True."


For each extraction, produce something like:
CLARIFIED QUESTION: <One-sentence, cleaned-up question>
CLARIFIED ANSWER: <One-sentence, cleaned-up answer or best summary of the official FDA stance>
VERBATIM QUESTION: <Exact single-line text from the transcript, no newlines>
VERBATIM ANSWER: <Exact single-line text from the transcript, no newlines>
SPEAKER QUESTION: <Name and role>
SPEAKER ANSWER: <Name and role>
TRANSCRIPT START POSITION: <integer index in transcript>
TRANSCRIPT END POSITION: <integer index in transcript>
TOPICS: <short list of relevant topics>
REVIEW FLAG: <True/False>

**Important:**  
- Keep the "VERBATIM QUESTION" and "VERBATIM ANSWER" truly on one line each, removing speaker tags or line breaks.  
- Do not repeat the same text chunk if it's already been extracted in a previous QA pair.  
- Use your judgment to maintain clarity but remain faithful to the transcript.

By following these updated guidelines, your extraction will avoid repetition, properly scope incremental location offsets, and keep the Q&A set tightly focused on the most critical technical and regulatory content from the FDA Town Hall. 

"""
def tools_qa_incremental_F():
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_4 = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics. Your role is to extract and clarify the next question-answer pair from the given transcript chunk.

Core Requirements:
1. DO NOT REPEAT ESSENTIALLY THE SAME QUESTION OR ANSWER from previous blocks
2. Focus only on technical, procedural, or legal information
3. Exclude meeting orchestration details (e.g., starting meeting, connection issues, speaker order)

Speaker Guidelines:
- Authority Speakers are indicated by 'FDA' in their role description
- Non-Authority Speaker statements require FDA acknowledgment
- Speakers are identified by lines ending with colon or timestamp

Position Tracking:
- Precisely identify start/end positions of extracted text in the transcript
- This enables accurate progression and prevents duplicating content
- Report positions relative to the start of the provided chunk

If unsure about information importance, include it but set review_flag to True.
"""
def tools_qa_incremental_4():
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_5 = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics. Your role is to extract and clarify the next question-answer pair from the given transcript chunk and previous questions.

Core Requirement:
DO NOT REPEAT ESSENTIALLY THE SAME QUESTION given the list of previous questions

Speaker Guidelines:
- Authority Speakers are indicated by 'FDA' in their role description
- Non-Authority Speaker statements require FDA acknowledgment
- Speakers are identified by lines ending with colon or timestamp
- Treat a single speaker's turn plus FDA response as one QA pair unless multiple distinct questions
- Merge minor clarifications or follow-ups into existing QA rather than creating new pairs

Position Tracking:
- Precisely identify start/end positions of extracted text in the transcript
- This enables accurate progression and prevents duplicating content
- Report positions relative to the start of the provided chunk

Content Guidelines:
- Focus on technical, procedural, or legal aspects of COVID-19 diagnostics, test development, validation, labeling
- Minimize implied questions - only use for important new regulatory content not previously captured
- Exclude meeting orchestration details (e.g., starting meeting, connection issues, speaker order)
- Exclude repeated disclaimers about FDA not discussing specific submissions

If unsure about information importance, include it but set review_flag to True.
"""
def tools_qa_incremental_5():
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_6RT = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics. Your role is to extract and clarify the next question-answer pair from the given transcript chunk and previous questions.

Core Requirements:
1. Identify the next question or important information from the provided transcript chunk
2. Must come after the provided previous question-answer pair
3. 



NEVER EXTRACT A QUESTION THAT COVERS THE SAME CORE TOPIC AND INFORMATION AS ANY PREVIOUS QUESTION
2. If a new question seems too similar to previous ones, SKIP AHEAD in the transcript to find the next truly distinct topic
3. When multiple questions discuss the same general topic only extract the FIRST comprehensive question-answer pair
4. For follow-up questions or clarifications, merge them into the original answer rather than creating new QA pairs
5. If no novel questions remain in the current chunk, set review_flag to True and move to the next chunk

Question Diversity Guidelines:
- Each question must introduce a completely new topic or regulatory aspect
- Reject questions that merely rephrase or slightly extend previous questions
- For multi-part discussions, combine related points into a single comprehensive QA pair
- When in doubt about similarity, err on the side of skipping the question

Speaker Guidelines:
- Authority Speakers are indicated by 'FDA' in their role description
- Non-Authority Speaker statements require FDA acknowledgment
- Speakers are identified by lines ending with colon or timestamp
- Treat a single speaker's turn plus FDA response as one QA pair unless multiple distinct questions
- Merge minor clarifications or follow-ups into existing QA rather than creating new pairs

Position Tracking:
- Precisely identify start/end positions of extracted text in the transcript
- This enables accurate progression and prevents duplicating content
- Report positions relative to the start of the provided chunk

Content Guidelines:
- Focus on technical, procedural, or legal aspects of COVID-19 diagnostics, test development, validation, labeling
- Minimize implied questions - only use for important new regulatory content not previously captured
- Exclude meeting orchestration details (e.g., starting meeting, connection issues, speaker order)
- Exclude repeated disclaimers about FDA not discussing specific submissions

If unsure about information importance, include it but set review_flag to True.
"""
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_6 = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics.

Your Role:
- Determine whether there is important content that should be extracted as an additional question-answer (QA) block, with the provided context of a list of the last several previous questions and the complete previous QA block.
- If additional important content is present, extract and clarify the next question-answer pair from the provided transcript chunk.
- If no additional important content is present, respond with "NO NEW QA" for the clarified_question field and leave the other fields blank (empty strings) or zero.
- Extract only new, distinct question-answer content that appears after the text already covered by the previous QA block. Do not duplicate an already-extracted Q&A from the same text segment. However, if there is new or distinct content within a previously introduced speaker response that was never captured, you may extract it now.
- Provide both verbatim and clarified versions of the question and answer to ensure thorough coverage and readability.

Coverage & Percentage Guidance:
- Aim to capture the majority of important FDA information while minimizing redundant or overlapping Q&A blocks.
- Strive for high coverage of significant technical, procedural, or legal information. If a transcript chunk introduces new, important content not already captured, create a new QA block.
- However, do not generate duplicate or near-duplicate QA pairs.
- Regulatory updates, new test authorizations, or statements of priority from FDA speakers count as important content. If not obviously phrased as a question, treat them as implied questions and produce a new QA.
- Any significant statement of FDA updates, newly authorized tests, or top priorities from FDA staff should be captured as an implied question and answer if not already extracted.
- If an FDA speaker (or other speaker) shares new or significant updates, always create an implied question if not covered previously.

Core Requirements:
1. DO NOT REPEAT QUESTIONS THAT COVER THE SAME CORE TOPIC AND INFORMATION as any question in the provided list of previous questions.
2. If a potential question is too similar to previous ones, skip ahead in the transcript or mark "NO NEW QA" for this segment.
3. For multi-part discussions of the same topic, merge clarifications into one comprehensive QA pair.
4. If you determine there is no distinct new content for a given chunk, return "NO NEW QA" (see instructions below).

Speaker Guidelines:
- Speakers are identified by lines ending with a colon, timestamp, or by a direct statement of their role (e.g., "Dr. Smith (FDA):").
- Authority Speakers are indicated by 'FDA' in their role description.
- Non-Authority Speaker statements must be included in the clarified_answer field if they contain important details or are directly addressed by the FDA. If uncertain, set review_flag = True.

Position Tracking:
- Precisely identify start/end positions of extracted text (verbatim) within the chunk.
- Use these positions to prevent duplication and ensure incremental coverage.

Content Guidelines:
- Focus on technical, procedural, or legal aspects of COVID-19 diagnostics (test development, validation, labeling, etc.).
- Exclude trivial or orchestration details like meeting start-up or speaker order.
- If important FDA information is present but no explicit question is asked, generate an “implied” question.
- Whenever uncertain, set review_flag to True.

Verbatim vs. Clarified Output:
- Provide both verbatim_question and verbatim_answer, exactly as they appear in the transcript (minus speaker labels and newlines).
- Provide clarified_question and clarified_answer for conciseness, improved clarity, and readability.

Option to Return “No New QA”:
- If no new question is found, set "clarified_question" to the exact string "NO NEW QA" and leave the other fields blank (empty strings) or zero. 
- Set "review_flag" to True if there is significant uncertainty in whether new QA content is present, or False if there is clearly no remaining new content given the provided context in the form of the previous list of several questions and previous entire QA block.
- If the previously extracted QA block is empty or nonexistent, parse all important content in the chunk as new Q&A, since there is no older QA to conflict with.

Your output must strictly follow the schema. All fields are required, so if there is no new QA, fill them with the agreed-upon placeholders or zeros.

The transcript will be processed in a progressive manner with the response being one in a sequence.
"""
def tools_qa_incremental_6():
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_6B = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics.

Your Role:
- Determine whether there is important content that should be extracted as one or more question-answer (QA) blocks, given a list of previous questions and the previous QA block.
- If additional important content is present, extract and clarify one or more new Q&A pairs from the provided transcript chunk.
- If no additional important content is present, respond with "NO NEW QA" for the clarified_question field and leave the other fields blank (empty strings) or zero.
- Extract only new, distinct question-answer content that appears after the text already covered by the previous QA block. 
  - Do not duplicate a Q&A already extracted from the same text segment. 
  - However, if a single answer covers multiple topics (and those topics are not yet captured in any previous question), you should create multiple QA pairs—one for each distinct point.
- Provide both verbatim and clarified versions of each question and answer to ensure thorough coverage and readability.

Coverage & Percentage Guidance:
- **Aim for comprehensive coverage** of the FDA’s important regulatory and technical information. 
- If a transcript chunk introduces new or significant material not previously extracted, **create a new QA block.** 
- **Avoid overlap**: if a question has essentially the same meaning as a previous question, skip it.
- **Include high-level updates**: Regulatory updates, newly authorized tests, or statements of FDA priority should be treated as “implied questions” if they are not explicitly phrased as questions.
- **Allow multiple questions** from a single turn or answer if there are clearly separate topics or points worth indexing.

Core Requirements:
1. DO NOT REPEAT QUESTIONS THAT COVER THE SAME CORE TOPIC AND INFORMATION as any in the provided previous-questions list.
2. If a potential question is too similar to previous ones, skip it or return “NO NEW QA” for that segment.
3. For multi-part discussions of the same topic, merge clarifications into one comprehensive QA pair. However, if an answer covers multiple unrelated points, **split** them into multiple QA pairs for clarity.
4. If you determine there is no distinct new content for a given chunk, return "NO NEW QA" (instructions below).

Speaker Guidelines:
- Speakers are identified by lines ending with a colon, timestamp, or by a direct statement of their role (e.g., "Dr. Smith (FDA):").
- Authority Speakers are indicated by 'FDA' in their role description.
- Non-Authority Speaker statements must be included in the clarified_answer field if they contain important details or are directly addressed by the FDA. If uncertain, set review_flag = True.

Position Tracking:
- Precisely identify start/end positions of extracted text (verbatim) within the chunk.
- Use these positions to prevent duplication and ensure incremental coverage.

Content Guidelines:
- Focus on **technical, procedural, or legal** aspects of COVID-19 diagnostics (test development, validation, labeling, etc.).
- Exclude trivial meeting details (startup, speaker order).
- If important FDA information is present but no explicit question is asked, generate an “implied” question.
- Whenever uncertain, set review_flag to True.

Verbatim vs. Clarified Output:
- Provide both verbatim_question and verbatim_answer, exactly as they appear (minus speaker labels and newlines).
- Provide clarified_question and clarified_answer for readability, combining or splitting content *only* to improve clarity and coverage without contradicting the original meaning.

Option to Return “NO NEW QA”:
- If no new question is found, set "clarified_question" to the exact string "NO NEW QA" and leave other fields blank (empty strings) or zero.
- Set "review_flag" to True if uncertain whether new QA content is present, or False if obviously none remains.
- If the previously extracted QA block is empty or nonexistent, parse all important content in the chunk as new Q&A.

Remember, **the user’s application will index only the questions** for semantic search, so your clarified_question fields must capture all key points that a user might search for in the future. Avoid discarding or merging clearly separate topics into one question.

Your output must strictly follow the schema. All fields are required, so if there is no new QA, fill them with the agreed-upon placeholders or zeros. The transcript will be processed in a progressive manner, each output forming part of a larger incremental extraction.
"""
FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCRIPT_FDA_TOWNHALLS_6C = """
You are an expert text analyzer trained in identifying questions and answers in transcripts of dialogue, specifically for FDA Town Hall meetings on COVID-19 diagnostics.

Your Role:
- Determine whether there is content in a provided a transcript chunk of text that should be extracted as an additional question, given a list of previous questions that have previously been extracted.
- If additional important content is present, extract and clarify one or more new questions from the provided transcript chunk and create all associated fields in the question-answer (QA) block.
- If no additional important content is present, respond with "NO NEW QA" for the clarified_question field and leave the other fields blank (empty strings) or zero.

Important Note on Use Case:
- Only the clarified_question field will be indexed and used for semantic search. Therefore, the coverage of each new topic or keyword must appear in the question, ensuring users can find it later by searching. If an answer covers multiple distinct topics, you should form multiple questions—even if they overlap in the answer text—so that each topic appears in its own question for better searchability.
- In other words, the question text itself must include key terms, phrases, or concepts from the answer. This way, anyone searching for those terms will retrieve the relevant QA pair. Redundant or nearly duplicated questions should be avoided, but it’s acceptable for multiple different questions to reference the same or partially overlapping answer segments if each question addresses a unique aspect that users might search for.

Coverage & Percentage Guidance:
- **Aim for comprehensive coverage** of the FDA’s important regulatory and technical information. 
- If a transcript chunk introduces new or significant material not in the previous questions, **extract a new question.** 
- **Include high-level updates**: Regulatory updates, newly authorized tests, or statements of FDA priority should be treated as “implied questions” if they are not explicitly phrased as questions.
- **Allow multiple questions** from a single turn or answer if there are clearly separate topics or points worth extracting.
- If you determine there is no distinct new question to be extracted for a given chunk, return "NO NEW QA" (instructions below).

Speaker Guidelines:
- Speakers are identified by lines ending with a colon, timestamp, or by a direct statement of their role (e.g., "Dr. Smith (FDA):").
- Authority Speakers are indicated by 'FDA' in their role description.
- Non-Authority Speaker statements must be included in the clarified_answer field if they contain important details or are directly addressed by the FDA. If uncertain, set review_flag = True.

Position Tracking:
- Precisely identify start/end positions of extracted text (verbatim) within the chunk.
- Use these positions to prevent duplication and ensure incremental coverage.

Content Guidelines:
- Focus on **technical, procedural, or legal** aspects of COVID-19 diagnostics (test development, validation, labeling, etc.).
- Exclude trivial meeting details (startup, speaker order).
- If important FDA information is present but no explicit question is asked, generate an “implied” question.
- Whenever uncertain, set review_flag to True.

Verbatim vs. Clarified Output:
- Provide both verbatim_question and verbatim_answer, exactly as they appear (minus speaker labels and newlines).
- Provide clarified_question and clarified_answer for readability, combining or splitting content *only* to improve clarity and coverage without contradicting the original meaning.

Option to Return “NO NEW QA”:
- If no new question is found, set "clarified_question" to the exact string "NO NEW QA" and leave other fields blank (empty strings) or zero.
- Set "review_flag" to True if uncertain whether new QA content is present, or False if obviously none remains.
- If the previously extracted QA block is empty or nonexistent, parse all important content in the chunk as new Q&A.

Remember, **the user’s application will index only the questions** for semantic search, so your clarified_question fields must capture all key points that a user might search for in the future. Avoid discarding or merging clearly separate topics into one question.

Your output must strictly follow the schema. All fields are required, so if there is no new QA, fill them with the agreed-upon placeholders or zeros. The transcript will be processed in a progressive manner, each output forming part of a larger incremental extraction.
"""
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
def fcall_qa_incremental(transcript, next_tokens, fcall_prompt, start_position, debug=True):
    """
    Processes a transcript string incrementally to extract the next question-answer pair using OpenAI function calling.
    This function yields each QA block along with the current position in the transcript, allowing for incremental processing and resumption from the last processed position.  

    :param transcript: string of the transcript content.
    :param next_tokens: integer of the number of tokens to look ahead.
    :param fcall_prompt: string of the prompt to be used for function calling.
    :param start_position: integer of the starting position in the transcript.
    :yield: tuple of (qa_block, current_position) or (None, current_position) if an error occurred.
    """
    def is_no_new_qa(arguments):
def create_qa_file_from_transcript_incremental(file_path, fcall_prompt):
        """Helper function to check if response indicates no new QA"""
        return (arguments['clarified_question'].upper() == 'NO NEW QA' or 
                not arguments['clarified_answer'].strip())
    
    while current_position < len(transcript):
        chunk, next_position = get_next_chunk(transcript, current_position, next_tokens)
        print(f"chunk transcript positions: {current_position:,} to {next_position:,} of total: {total_chars_transcript:,} | Percent done: {round(current_position / total_chars_transcript * 100)}%")
        
        # Track chunk end positions - maintain rolling history
        chunk_end_history.append(next_position)
        if len(chunk_end_history) > HISTORY_SIZE:
            chunk_end_history.pop(0)
        
        verbose_print(debug, f"DEBUG: Current chunk_end_history: {chunk_end_history}")
            
        # Check for stuck processing - modified condition
        if (len(chunk_end_history) >= HISTORY_SIZE and 
            len(set(chunk_end_history)) == 1 and 
            next_position < len(transcript)):
            print(colored(f"__Detected stuck processing - chunks repeatedly ending at position {next_position:,}__", "red"))
            print(f"Forcing skip to next chunk starting at: {next_position:,}")
            current_position = next_position
            continue

        # Remove early exit for end of transcript - we still need to process the final chunk
        # Instead, just note that we're processing the final chunk
        if next_position >= len(transcript):
            print("Processing final transcript chunk")

        # Create context with previous questions and previous block
        prev_questions_context = "Previous questions (from most recent to oldest):\n"
        for i, q in enumerate(previous_questions, 1):
            prev_questions_context += f"{i}. {q}\n"
        
        if not previous_block:
            prev_block_context = ("Please identify the first question-answer pair in the following transcript chunk:")
        else:
            prev_block_context = (f"Previous Question-Answer Block:\n{previous_block}\nPlease identify the next question-answer pair after this one in the following transcript chunk:")
        
        full_prompt = (
            f"{fcall_prompt}\n\n"
            f"{prev_questions_context}\n"
            f"{prev_block_context}\n\n"
            f"{chunk}"
        )
        
        try:
            qa_response = openai_function_call(full_prompt, chunk, tools_qa_incremental_6())
            arguments = json.loads(qa_response['tool_calls'][0]['function']['arguments'])
            
            # If no new QA found and we're at the end of transcript, signal completion
            if is_no_new_qa(arguments):
                print(colored(f"No new QA found at position {current_position:,}\n", "green"))
                if next_position >= len(transcript):
                    print("Completed processing final chunk - ending extraction")
                    yield None, -1
                    return
                current_position = next_position
                continue
            
            # Update previous questions list
            previous_questions.insert(0, arguments['clarified_question'])  # Add new question at the beginning
            if len(previous_questions) > HISTORY_SIZE:
                previous_questions.pop()  # Remove oldest question if exceeding HISTORY_SIZE

            qa_block = f"QA Block {block_counter}:\n"
            qa_block += f"CLARIFIED QUESTION: {arguments['clarified_question']}\n"
            qa_block += f"CLARIFIED ANSWER: {arguments['clarified_answer']}\n"
            qa_block += f"VERBATIM QUESTION: {arguments['verbatim_question']}\n"
            qa_block += f"VERBATIM ANSWER: {arguments['verbatim_answer']}\n"
            qa_block += f"SPEAKER QUESTION: {arguments['speaker_question']}\n"
            qa_block += f"SPEAKER ANSWER: {arguments['speaker_answer']}\n"
            abs_transcript_start_pos = current_position + arguments['relative_start_position']
            abs_transcript_end_pos = current_position + arguments['relative_end_position']
            qa_block += f"TRANSCRIPT START POSITION: {abs_transcript_start_pos:,}\n"
            qa_block += f"TRANSCRIPT END POSITION: {abs_transcript_end_pos:,}\n"
            qa_block += f"TOPICS: {', '.join(arguments['topics'])}\n"
            qa_block += f"REVIEW FLAG: {arguments['review_flag']}\n\n"

            block_counter += 1  # Increment block counter after successful processing
            previous_block = qa_block  # Store the current block as previous block
            
            print(f"qa response transcript position: {abs_transcript_start_pos:,} to {abs_transcript_end_pos:,}")
            
            yield qa_block, abs_transcript_start_pos
            
        except Exception as e:
            print(f"Error in qa extraction: {str(e)}")
            if next_position >= len(transcript):
                print("Error in final chunk - ending extraction")
                yield None, -1
                return
            current_position += next_tokens
            yield None, current_position
    """
def fcall_qa_incremental_OLD(transcript, next_tokens, fcall_prompt, start_position, debug=False):
    """
    from primary.structured import count_blocks

    metadata, content = read_metadata_and_content(file_path)
    metadata = set_metadata_field(metadata, "last updated", 'Created QA Incremental')
    metadata = set_metadata_field(metadata, "source file", file_path)
    
    print("OPENAI_MODEL = " + OPENAI_MODEL)
    segment_tokens = count_segment_tokens(file_path)
    max_segment_tokens = max(segment_tokens)
    transcript = get_heading(file_path, "### transcript")
    transcript = transcript.lstrip('### transcript').rstrip('\n').lstrip('\n*')
    print(f"Number of characters in transcript: {len(transcript):,}\n")

    initial_content = "## content\n\n### qa\n"
    qa_file_path = write_metadata_and_content(file_path, metadata, initial_content, overwrite='no-sub', suffix_new='_qa-inc')
    
    current_position = 0
    max_retries = 5

    while current_position < len(transcript):
        existing_blocks = count_blocks(qa_file_path)
        block_number = existing_blocks + 1
        
        for qa_block, abs_transcript_start_pos in fcall_qa_incremental(transcript, max_segment_tokens, fcall_prompt, start_position=current_position):
            if abs_transcript_start_pos == -1:  # Check for end-of-transcript signal
                print("QA extraction completed due to end of transcript.")
                return qa_file_path
                
            retry_count = 0
            while retry_count < max_retries:
                try:
                    if qa_block is None:
                        raise Exception(f"Error occurred on block {block_number}.")
                    
                    qa_lines = qa_block.splitlines()[:2]
                    print()
                    print(qa_lines[0])
                    print(colored(qa_lines[1], "yellow"))
                    with open(qa_file_path, 'a') as f:
                        f.write(qa_block)
                    
                    current_position = abs_transcript_start_pos
                    block_number += 1
                    break  # Successfully processed the block, exit retry loop
                
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        print(f"\n********** Max retries ({max_retries}) reached for block {block_number}. Skipping this block.")
                        current_position += max_segment_tokens  # Move to next position
                    else:
                        print(f"\n********** Error encountered: {str(e)}")
                        print(f"Retry attempt {retry_count} of {max_retries}")
                        print("Retrying the same block.")
            
            if retry_count == 0:
                print("Block processed successfully.")
            elif retry_count < max_retries:
                print("Block processed after retries.")
            else:
                print("Block skipped due to repeated errors.")

    print("QA extraction completed.")
    print("QA written to " + qa_file_path)
    
    return qa_file_path

    """
    """
    current_position = start_position
    previous_block = None
    total_chars_transcript = len(transcript)
    
    # Add tracking for detecting stuck positions
    position_history = []
    stuck_threshold = 3  # Number of times to try processing same area before forcing skip
    min_position_advance = next_tokens # Minimum characters to skip if stuck

    while current_position < len(transcript):
        chunk, next_position = get_next_chunk(transcript, current_position, next_tokens)
        print(f"chunk transcript positions: {current_position:,} to {next_position:,} of total: {total_chars_transcript:,} | Percent done: {round(current_position / total_chars_transcript * 100)}%")
        
        # Track positions to detect if we're stuck
        position_history.append(current_position)
        if len(position_history) > stuck_threshold:
            position_history.pop(0)
            
            # If we've processed the same area multiple times
            if max(position_history) - min(position_history) < min_position_advance:
                print(f"Detected stuck processing - forcing skip forward by {min_position_advance} characters")
                current_position += min_position_advance
                position_history.clear()  # Reset history after skip
                continue

        prev_block_prompt = "Please identify the first question-answer pair in the following transcript chunk:" if not previous_block else f"""
### QA BY SECTIONS - FULL BLOCKS (1,618 tokens)
        """

        full_prompt = fcall_prompt + "\n" + prev_block_prompt + "\n\n" + chunk
        
        try:
            verbose_print(debug, f"DEBUG\nfull_prompt: {full_prompt}\nchunk: {chunk}\n")
            qa_response = openai_function_call(full_prompt, chunk, tools_qa_incremental_4())
            verbose_print(debug, f"qa_response: {qa_response}\n")
            
            # Extract the 'arguments' field from the function call
            arguments_json = qa_response['tool_calls'][0]['function']['arguments']

            # Attempt to parse the JSON
            try:
                arguments = json.loads(arguments_json)
                
                qa_block = f"CLARIFIED QUESTION: {arguments['clarified_question']}\n"
                qa_block += f"CLARIFIED ANSWER: {arguments['clarified_answer']}\n"
                qa_block += f"VERBATIM QUESTION: {arguments['verbatim_question']}\n"
                qa_block += f"VERBATIM ANSWER: {arguments['verbatim_answer']}\n"
                qa_block += f"SPEAKER QUESTION: {arguments['speaker_question']}\n"
                qa_block += f"SPEAKER ANSWER: {arguments['speaker_answer']}\n"
                abs_transcript_start_pos = current_position + arguments['relative_start_position']
                abs_transcript_end_pos = current_position + arguments['relative_end_position']
                qa_block += f"TRANSCRIPT START POSITION: {abs_transcript_start_pos:,}\n"
                qa_block += f"TRANSCRIPT END POSITION: {abs_transcript_end_pos:,}\n"
                qa_block += f"TOPICS: {', '.join(arguments['topics'])}\n"
                qa_block += f"REVIEW FLAG: {arguments['review_flag']}\n\n"

            except json.decoder.JSONDecodeError as e:
                print("JSONDecodeError:", e)
                current_position += min_position_advance  # Force advance on error
                yield None, current_position
                continue
            
            print(f"qa response transcript position: {abs_transcript_start_pos:,} to {abs_transcript_end_pos:,}")
            # Update previous_block for the next iteration
            previous_block = qa_block
            
            # Update position based on LLM response
            current_position = abs_transcript_start_pos
            
            # If we successfully processed a block, clear the position history
            position_history.clear()
            
            yield qa_block, abs_transcript_start_pos
        except Exception as e:
            print(f"Error in qa extraction: {str(e)}")
            current_position += min_position_advance  # Force advance on error
            yield None, current_position


FCALL_SYSTEM_PROMPT_QA_SECTIONS_TRANSCRIPT_FDA_TOWNHALLS_1A = """
"""
FCALL_SYSTEM_PROMPT_QA_SECTIONS_TRANSCRIPT_FDA_TOWNHALLS_1B = """
def tools_qa_sections_1():
def fcall_qa_section(transcript_section, fcall_prompt, provider="openai", debug=False):
"""
    return [{
        "type": "function",
        "function": {
            "name": "extract_qa",
            "description": "Extract and clarify the next question-answer block (both verbatim and clarified fields) from an FDA Town Hall transcript section. If no new question is found, fill all required fields with placeholders/zeros as instructed in the system prompt.",
            "strict": True,  # For Structured Output
            "parameters": {
                "type": "object",
                "properties": {
                    "clarified_question": {
                        "type": "string",
                        "description": (
                            "A concise, edited version of the question. If no new question is found, set this to 'NO NEW QUESTION'. The entire text should be on one line. Do not mention any specific speaker names."
                        )
                    },
                    "clarified_answer": {
                        "type": "string",
                        "description": (
                            "A concise, edited version of the answer. If no new question is found, leave this field blank (e.g., ''). The entire text of this answer should be on a single line. Do not mention any specific speaker names, instead use 'FDA' where appropriate."
                        )
                    },
                    "verbatim_question": {
                        "type": "string",
                        "description": (
                            "The exact text of the question, minus speaker labels/newlines. If no new question is found, use ''. If no explicit question is asked, use the string 'IMPLIED QUESTION'. The entire text should be on a single line. Do not start the text with the speaker name from the preceding speaker line."
                        )
                    },
                    "verbatim_answer": {
                        "type": "string",
                        "description": (
                            "The exact text of the answer, minus speaker labels/newlines. If no new question is found, use ''. The entire text should be on a single line. Do not start the text with the speaker name from the preceding speaker line."
                        )
                    },
                    "speaker_question": {
                        "type": "string",
                        "description": (
                            "Name/role of question speaker. Use '' if no new question is found. The name must be as identified in the transcript by the text in the speaker line that precedes a colon or timestamp. Do not use a different name spelling that may appear in the speaker dialogue. If the question is implied from an Authority Speaker's statement, use 'IMPLIED'."
                        )
                    },
                    "speaker_answer": {
                        "type": "string",
                        "description": (
                            "Name/role of answer speaker. Use '' if no new question is found. The name must be as identified in the transcript by the text in the speaker line that precedes a colon or timestamp. Do not use a different name spelling that may appear in the speaker dialogue. If the question is implied from an Authority Speaker's statement, use 'IMPLIED'."
                        )
                    },
                    "topics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "A list of 1-3 key topics addressed in the question-answer block. If no new question is found, return an empty list []."
                        )
                    },
                    "review_flag": {
                        "type": "boolean",
                        "description": (
                            "Set True if significant uncertainty in the response. Otherwise False."
                        )
                    }
                },
                "required": [
                    "clarified_question", "clarified_answer","verbatim_question", "verbatim_answer",
                    "speaker_question", "speaker_answer", "topics", "review_flag"
                ],
                "additionalProperties": False
            }
        }
    }]
    """
    def is_no_new_question(arguments):
    """
    HISTORY_SIZE = 10  # Number of previous questions to maintain
    previous_questions = []  # List to store previous questions
    previous_block = None  # Store the most recent QA block
    qa_blocks_found = 0  # Track number of QA blocks found in this section
    max_retries = 3  # Maximum attempts to get at least one QA block
    
        """Helper function to check if response indicates no new question"""
def create_qa_file_from_transcript_sections(file_path, fcall_prompt, provider="openai", delimiter='---'):
    """
    Extract QA blocks from a transcript file by processing sections delimited by a separator.
    
    :param file_path: string path to the transcript file
    :param fcall_prompt: string prompt for function calling
    :param provider: string indicating which provider to use ("openai" or "anthropic")
    :param delimiter: string used to separate transcript sections
    :return qa_file_path: string path to the created QA file
    """
### Q SIMILARITY (885 tokens)
def get_questions_from_qa_file(qa_file_path, heading):
    """
    Gets questions and their section numbers from a QA file, handling different heading formats.
    For custom headings (not "### qa"), this function will find any line containing a colon
    under the specified heading and treat everything after the colon (and any following whitespace)
    as a question, ignoring any prefixes or numbering schemes before the colon.

    :param qa_file_path: string, path to the QA file to parse.
    :param heading: string, heading format to determine parsing method.
    :return questions: list, tuples of (section number, question text).
    """
def get_questions_from_extract_log(qa_file_path, heading_level=5, verbose=False):
    """
    Gets all questions from a QA file by finding unique headings at the specified level
    and extracting questions from each heading section.

    :param qa_file_path: string, path to the QA file to parse
    :param heading_level: integer, markdown heading level to search for (e.g., 5 for #####)
    :param verbose: boolean, whether to print heading counts
    :return: list of tuples (section_number, question_text) sorted by section number
    """
def compare_question_tuple_lists(list1, list2, list1_name="List 1", list2_name="List 2"):
    """
    Compares two lists of question tuples and identifies differences between them.
    
    :param list1: list of tuples (section_number, question_text)
    :param list2: list of tuples (section_number, question_text)
    :param list1_name: string name for first list in output
    :param list2_name: string name for second list in output
    :return: boolean True if lists are identical, False otherwise
    """
def mrun_get_questions_from_qa_file():
def generate_and_save_question_embeddings(qa_file_path, questions, verbose=True):
    """
    Generates embeddings for questions and saves them to a file.

    :param qa_file_path: string, path to the QA file to parse.
    :param questions: list, questions to generate embeddings for.
    :param verbose: bool, whether to print progress messages.
    :return: string, path to the saved embeddings file.
    """
def mrun_generate_and_save_question_embeddings():
def calc_question_list_similarities(embeddings_file, similarity_threshold=0.781):
    """
    Calculates pairwise similarities between questions within the same section.

    :param embeddings_file: string, path to the saved embeddings file.
    :param similarity_threshold: float, threshold for similarity score to remove questions
    :return: tuple of (similarities dict, list of questions to remove, output string)
        - similarities: dict containing grouped questions and their similarity matrices by section
        - questions_to_remove: list of strings in format "section-question" for shorter questions in similar pairs
        - output_str: string containing the formatted output of similar questions and removal decisions
    """
def mrun_calc_question_list_similarities():
def visualize_question_similarities_1(vectors_file_path, min_similarity=0.7):  # uses seaborn which cannot do tooltips
    """
    Creates separate heatmaps for questions within each section, showing only the lower triangular portion.
    Takes a vectors file path as input, calculates similarities, and saves visualization.

    :param vectors_file_path: string, path to the NPZ file containing question vectors
    :param min_similarity: float, minimum similarity threshold to report
    :return: string, path to the saved visualization file
    """
def visualize_question_similarities(vectors_file_path, min_similarity=0.7, fixed_colorscale=True):
    """
    Creates interactive heatmaps for questions within each section using Plotly.
    Shows similarity scores and questions in tooltips when hovering.

    :param vectors_file_path: string, path to the NPZ file containing question vectors
    :param min_similarity: float, minimum similarity threshold to report
    :param fixed_colorscale: bool, if True keeps color scale fixed while thresholding, if False rescales colors
    :return: string, path to the saved visualization file
    """
def mrun_visualize_question_similarities():
### QA BY SECTIONS - Q ONLY (10,476 tokens)
def create_extract_log_header(fcall_prompt, provider, model, round_num, round_name):
    """
    Create the extract log header information for a specific round.

    :param fcall_prompt: string prompt for function calling
    :param provider: string indicating which provider to use
    :param model: string indicating which model is being used
    :param round_num: integer indicating which round this is
    :param round_name: string name of the extraction round
    :return: list of log lines
    """
def get_transcript_metadata_and_sections(transcript_file_path, delimiter='---'):
    """
    Read a transcript file and extract metadata, content and transcript sections.

    :param transcript_file_path: string, path to the transcript file
    :param delimiter: string, used to separate transcript sections
    :return metadata: dict, metadata from file
    :return sections: list, transcript sections split by delimiter
    :return total_sections: int, total number of sections
    """
def log_section_items(log_lines, section_num, items, round_name, prefix):
    """
    Add items to the log under the appropriate section heading,
    ensuring that all sections from 1..section_num include the round heading
    (even if no items are provided for earlier sections).
    
    :param log_lines: list of existing log lines
    :param section_num: current section number
    :param items: list of items (questions) to add
    :param round_name: name of the current round (e.g. "Explicit Questions Extraction")
    :param prefix: prefix for item numbering (e.g., "QE" or "QI")
    :return: updated log lines
    """
    def is_blank(line):
def mtest_log_section_items():
#### extract log header (5 tokens)
#### Section 1 of 2 (8 tokens)
#### Section 2 of 2""" (37 tokens)
    initial_log_text_1 = """### extract log
datetime: 2024



    expected_output_1 = """### extract log
#### extract log header (5 tokens)
#### Section 1 of 2 (8 tokens)
##### Explicit Questions Extraction (5 tokens)
#### Section 2 of 2 (37 tokens)
##### Explicit Questions Extraction (5 tokens)
QE 2-1: What is the process for LAMP testing validation?"""

    # Test Case 2: Starting with Explicit -> Adding Implicit Questions
    initial_log_text_2 = expected_output_1

    expected_output_2 = """### extract log
#### extract log header (5 tokens)
#### Section 1 of 2 (8 tokens)
##### Explicit Questions Extraction (5 tokens)
##### Implicit Questions Extraction (5 tokens)
#### Section 2 of 2 (37 tokens)
##### Explicit Questions Extraction (5 tokens)
##### Implicit Questions Extraction (5 tokens)
def mrun_log_section_items():
QI 2-1: What validation is needed for test modifications?"""

    # Test Case 1: Adding Explicit Questions
    log_lines_1 = initial_log_text_1.split('\n')
    result_1 = log_section_items(log_lines_1, 1, 
                              [],
                              "Explicit Questions Extraction", "QE")
    result_1 = log_section_items(result_1, 2, 
                              ["What is the process for LAMP testing validation?"],
                              "Explicit Questions Extraction", "QE")
    
    # Test Case 2: Adding Implicit Questions
    log_lines_2 = initial_log_text_2.split('\n')
    result_2 = log_section_items(log_lines_2, 1,
                              ["What are the FDA's requirements for pooling tests?"],
                              "Implicit Questions Extraction", "QI")
    result_2 = log_section_items(result_2, 2,
                              ["What validation is needed for test modifications?"],
                              "Implicit Questions Extraction", "QI")

    # Compare results for test case 1
    test1_result = '\n'.join(result_1)
    test1_passed = test1_result == expected_output_1
    if test1_passed:
        print("\n\n\n********** Test Case 1 - Adding Explicit Questions: PASS")
    else:
        print("\n\n\n********** Test Case 1 - Adding Explicit Questions: FAIL")
        print("\n=========== Initial:")
        print(initial_log_text_1)
        print("\n=========== Result:")
        print(test1_result)
        print("\n=========== Expected:")
        print(expected_output_1)

    # Compare results for test case 2  
    test2_result = '\n'.join(result_2)
    test2_passed = test2_result == expected_output_2
    if test2_passed:
        print("\n\n\n********** Test Case 2 - Adding Implicit Questions: PASS")
    else:
        print("\n\n\n********** Test Case 2 - Adding Implicit Questions: FAIL")
        print("\n=========== Initial:")
        print(initial_log_text_2) 
        print("\n=========== Result:")
        print(test2_result)
        print("\n=========== Expected:")
        print(expected_output_2)
        
    print(f"\ntestcase1-{'pass' if test1_passed else 'fail'}")
    print(f"testcase2-{'pass' if test2_passed else 'fail'}")
    pass
#if __name__ == "__main__":
    cur_qa_file_path = "data/floodlamp/reg/fda-townhalls/dev-qa-extract/VTH 36 just2_qa-qonly-REF QE.md"
    log_text = get_heading(cur_qa_file_path, "### extract log")
    log_lines = log_text.split('\n')
    print("log_lines before:")
    print("\n".join(log_lines))
    print("\n\nlog_lines after:")
    new_log_lines = log_section_items(log_lines, 2, ["First fake implicit question?", "Second implicit question?"], "Implicit Questions Extraction", prefix="QI")
    print("\n".join(new_log_lines))

FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1D = """
def tools_qa_qonly_explicit():
def fcall_qa_qonly_explicit(transcript_section, fcall_prompt, provider="openai", debug=False):
"""
    return [{
        "type": "function",
        "function": {
            "name": "extract_explicit_questions",
            "description": "Extract and clarify all explicitly asked questions from the text, breaking multi-part questions into separate entries",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of clarified, explicitly asked questions. Each should be concise and clear, without speaker names."
                    }
                },
                "required": ["questions"],
                "additionalProperties": False
            }
        }
    }]
    """
def do_qonly_round_1_explicit(transcript_file_path, fcall_prompt, provider="openai", delimiter='---', suffix_new='_qa-qonly'):
    """
    max_retries = 2  # Maximum attempts to get questions from a section
    
    # Add debug print for initial inputs
    verbose_print(debug, f"\nProcessing section of length: {len(transcript_section)} chars")
    
    # Get appropriate tools format for the provider
    tools = tools_qa_qonly_explicit()
    if provider == "anthropic":
        tools = convert_tools_to_anthropic_format(tools)
    
    while max_retries > 0:
        try:
            verbose_print(debug, f"Attempting function call with {provider}")
            # Make the appropriate function call based on provider
            if provider == "openai":
                response = openai_function_call(fcall_prompt, transcript_section, tools)
            elif provider == "anthropic":
                response = anthropic_function_call(fcall_prompt, transcript_section, tools)
            else:
                raise ValueError("Provider must be either 'openai' or 'anthropic'")
            
            verbose_print(debug, f"Got response: {response}")
            
            # Parse the response
            arguments = parse_function_call_response(response, provider)
            verbose_print(debug, f"Parsed arguments: {arguments}")
            
            if not arguments:
                raise Exception("Failed to parse function call response")
            
            questions = arguments.get('questions', [])
            verbose_print(debug, f"Extracted questions: {questions}")
                
            return questions  # Can be empty list if no questions found
            
        except Exception as e:
            print(colored(f"Error in question extraction: {str(e)}", "red"))
            verbose_print(debug, f"Full error details: {str(e)}")
            if max_retries > 1:
                max_retries -= 1
                print(colored(f"Error occurred. Retrying... ({max_retries} attempts remaining)", "red"))
                continue
            return None
    
    return None
    """
def mrun_do_qonly_round_1_explicit():
    """
    round_num = 1
    round_name = "Explicit Questions Extraction"
    start_time = time.time()

    # Set model based on provider
    if provider == "openai":
        model = OPENAI_MODEL
    elif provider == "anthropic":
        model = ANTHROPIC_MODEL
    else:
        raise ValueError("Provider must be either 'openai' or 'anthropic'")
    
    # Initialize log lines
    log_lines = create_extract_log_header(fcall_prompt, provider, model, round_num, round_name)
    print("\n".join(log_lines))  # Print header information

    # Get transcript sections and metadata
    metadata, sections, total_sections = get_transcript_metadata_and_sections(transcript_file_path, delimiter)

    # Get current datetime string to update metadata for new qa file
    current_datetime = get_current_datetime_humanfriendly()
    date = current_datetime.split(' ')[0]
    metadata = set_metadata_field(metadata, "last updated", f"{date} Created QA Sections")
    metadata = set_metadata_field(metadata, "source file", transcript_file_path)

    # Create output file with initial content
    initial_content = "## content\n"  # Note: ### qa section will be added later
    qa_file_path = write_metadata_and_content(transcript_file_path, metadata, initial_content, overwrite='no-sub', suffix_new=suffix_new)

    # First pass: Create section heading lines
    for section_num, section in enumerate(sections, 1):
        section_header = f"#### Section {section_num} of {total_sections}"
        log_lines.append(section_header)
        log_lines.append("")

    log_text = "\n".join(log_lines)
    #print(f"DEBUG ===***===*** log_text after first pass: {log_text}")  
     
    # Second pass: Process each section
    for section_num, section in enumerate(sections, 1):
        section = section.strip()
        if not section:
            raise ValueError(f"Empty section found at position {section_num}. All sections should exist in qa file extract log section.")
        try:
            print(f"\n\nProcessing Round {round_num} {round_name} - section {section_num} of {total_sections}")
            # Process this section (keeping fcall in main loop)
            questions = fcall_qa_qonly_explicit(section, fcall_prompt, provider=provider)
            
            # Get formatted log lines and append them
            log_lines = log_section_items(log_lines, section_num, questions, round_name, prefix="QE")
                    
        except Exception as e:
            error_msg = f"\n********** Error encountered in section {section_num}: {str(e)}"
            print(colored(error_msg, "red"))
            log_lines.append(error_msg)
            continue

    # Append extract log to the file
    with open(qa_file_path, 'a') as f:
        f.write("\n\n" + "\n".join(log_lines))

    print(f"\n{round_name} completed in {(time.time() - start_time) / 60:.1f} minutes.")
    print("Extract log written to " + qa_file_path)
    return qa_file_path
    pass
#if __name__ == "__main__":
    #cur_file_path = "data/floodlamp/reg/fda-townhalls/dev-qa-extract/VTH 36_cemanual-sections.md"
    cur_file_path = CUR_TRANSCRIPT_FILE_PATH
    #cur_file_path = "data/floodlamp/reg/fda-townhalls/dev-qa-extract/VTH 36 just2_trans.md"
    qa_file_path = do_qonly_round_1_explicit(cur_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1D)
    print(f"QA file created at: {qa_file_path}")   
FCALL_SYSTEM_PROMPT_QA_QONLY_IMPLICIT_1A = """
def tools_qa_qonly_implicit():
"""
    """
def fcall_qa_qonly_implicit(transcript_section, fcall_prompt, prev_questions, provider="openai", debug=False, abort_on_error=True):
    """
    return [{
        "type": "function",
        "function": {
            "name": "extract_implicit_questions",
            "description": (
                "Extract and clarify any implied questions from the transcript, excluding any questions that match or "
                "overlap with a given list of explicit questions."
            ),
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "implicit_questions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "A list of distinct implied questions relevant to FDA regulations, diagnostics, disease testing, COVID-19, the pandemic, the public health response, and any other important or relevant topics."
                            "No duplicates of previously identified explicit questions."
                        )
                    }
                },
                "required": ["implicit_questions"],
                "additionalProperties": False
            }
        }
    }]
    """
def do_qonly_round_2_implicit(transcript_file_path, fcall_prompt, provider="openai", delimiter='---', suffix_new='_qa-qonly'):
    """
    max_retries = 2  # Maximum attempts to get questions from a section
    
    # Add debug print for initial inputs
    verbose_print(debug, f"\nProcessing section with {len(prev_questions)} previous questions")
    
    # Get appropriate tools format for the provider
    tools = tools_qa_qonly_implicit()
    if provider == "anthropic":
        tools = convert_tools_to_anthropic_format(tools)
    verbose_print(debug, f"Using provider: {provider}")
    
    # Create context with previous questions list
    prev_questions_context = "Previously extracted explicit questions - **DO NOT extract similar or overlapping questions**:\n"
    for i, q in enumerate(prev_questions, 1):
        prev_questions_context += f"{i}. {q}\n"
    verbose_print(debug, f"Previous questions context:\n{prev_questions_context}")
    
    # Create full prompt with context
    full_prompt = (
        f"{fcall_prompt}\n\n"
        f"{prev_questions_context}\n\n"
        f"Please identify any implied questions in the following transcript section:\n\n"
        f"{transcript_section}"
    )
    verbose_print(debug, f"Full prompt:\n{full_prompt}")
    
    while max_retries > 0:
        try:
            verbose_print(debug, f"Attempting function call with {provider}")
            # Make the appropriate function call based on provider
            if provider == "openai":
                response = openai_function_call(full_prompt, transcript_section, tools)
            elif provider == "anthropic":
                response = anthropic_function_call(full_prompt, transcript_section, tools)
            else:
                raise ValueError("Provider must be either 'openai' or 'anthropic'")
            
            verbose_print(debug, f"Got response: {response}")
            
            # Parse the response
            arguments = parse_function_call_response(response, provider)
            verbose_print(debug, f"Parsed arguments: {arguments}")
            
            if not arguments:
                if abort_on_error:
                    raise Exception("Failed to parse function call response")
                return None
            
            questions = arguments.get('implicit_questions', [])
            verbose_print(debug, f"Extracted questions: {questions}")
            
            # No need to retry if we got a valid response (even if empty questions list)
            return questions
            
        except Exception as e:
            error_msg = str(e)
            if error_msg:  # Only print error if there's an actual message
                print(colored(f"Error in implicit question extraction: {error_msg}", "red"))
                verbose_print(debug, f"Full error details: {error_msg}")
                if abort_on_error:
                    raise  # Re-raise the exception to abort processing
            if max_retries > 1:
                max_retries -= 1
                print(colored(f"Error occurred. Retrying... ({max_retries} attempts remaining)", "red"))
                continue
            return None
    
    return None
    """
def mrun_do_qonly_round_2_implicit():
def single_section_qonly_round_2_implicit(transcript_file_path, fcall_prompt, section_num, provider="openai", delimiter='---', suffix_new='_qa-qonly'):
def mrun_single_section_qonly_round_2_implicit():
    """
    round_num = 2
    round_name = "Implicit Questions Extraction"
    start_time = time.time()

    # Verify QA file exists
    qa_file_path = sub_suffix_in_str(transcript_file_path, suffix_new)
    if not os.path.exists(qa_file_path):
        raise ValueError(f"QA file not found: {qa_file_path}")

    # Get existing explicit questions
    prev_questions_all = get_questions_from_qa_file(qa_file_path, heading="##### Explicit Questions Extraction")

    # Set model based on provider
    if provider == "openai":
        model = OPENAI_MODEL
    elif provider == "anthropic":
        model = ANTHROPIC_MODEL
    else:
        raise ValueError("Provider must be either 'openai' or 'anthropic'")
    
    # Get the existing extract log for log_lines
    log_text = get_heading(qa_file_path, "### extract log")
    log_lines = log_text.split('\n')
    #print("\n".join(log_lines))  # Print header information

    # Get transcript sections and metadata
    _, sections, total_sections = get_transcript_metadata_and_sections(transcript_file_path, delimiter)

    # Process each section
    for section_num, section in enumerate(sections, 1):
        section = section.strip()
        if not section:
            raise ValueError(f"Empty section found at position {section_num}. All sections should exist in qa file extract log section.")
        try:
            print(f"\n\nProcessing Round {round_num} {round_name} - section {section_num} of {total_sections}")
            # Process this section with implicit question extraction
            prev_questions_section = [q[1] for q in prev_questions_all if q[0] == section_num]  # Filter questions for this section
            #print(f"prev_questions_section: {prev_questions_section}")
            questions = fcall_qa_qonly_implicit(section, fcall_prompt, prev_questions_section, provider=provider)
            
            # Get formatted log lines and append them
            log_lines = log_section_items(log_lines, section_num, questions, round_name, prefix="QI")
                    
        except Exception as e:
            error_msg = str(e)
            if error_msg:  # Only log actual errors
                error_msg = f"\n********** Error encountered in section {section_num}: {error_msg}"
                print(colored(error_msg, "red"))
                log_lines.append(error_msg)
            raise  # Re-raise to abort processing

    updated_extract_log = f"\n".join(log_lines)
    
    set_heading(qa_file_path, updated_extract_log, "### extract log")
    print(f"\n{round_name} completed in {(time.time() - start_time) / 60:.1f} minutes.")
    print("Extract log updated in " + qa_file_path)
    return qa_file_path
    pass
#if __name__ == "__main__":
    #cur_transcript_file_path = "data/floodlamp/reg/fda-townhalls/dev-qa-extract/VTH 36_cemanual-sections.md"
    cur_transcript_file_path = CUR_TRANSCRIPT_FILE_PATH
    #cur_transcript_file_path = "data/floodlamp/reg/fda-townhalls/dev-qa-extract/VTH 36 just2_trans.md"

    # ONLY USE THIS AFTER copying the _qa-qonly file as a different name
    # qa_file_path = CUR_FILE_PATH
    # qa_file_path = sub_suffix_in_str(qa_file_path, '_qa-qonly')
    # delete_all_heading_instances(qa_file_path, "##### Implicit Questions Extraction")

    qa_file_path = do_qonly_round_2_implicit(cur_transcript_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_IMPLICIT_1A)
    print(f"Implicit Round 2 - QA file updated: {qa_file_path}")
    get_questions_from_extract_log(qa_file_path, verbose=True)
    # Verify QA file exists
    qa_file_path = sub_suffix_in_str(transcript_file_path, suffix_new)
    if not os.path.exists(qa_file_path):
        raise ValueError(f"QA file not found: {qa_file_path}")

    # Get existing explicit questions
    prev_questions_all = get_questions_from_qa_file(qa_file_path, heading="##### Explicit Questions Extraction")

    # Set model based on provider
    if provider == "openai":
        model = OPENAI_MODEL
    elif provider == "anthropic":
        model = ANTHROPIC_MODEL
    else:
        raise ValueError("Provider must be either 'openai' or 'anthropic'")

    # Get transcript sections and metadata
    _, sections, total_sections = get_transcript_metadata_and_sections(transcript_file_path, delimiter)

    # Process only the requested section
    section = sections[section_num - 1].strip()
    if not section:
        raise ValueError(f"Empty section found at position {section_num}. All sections should exist in qa file extract log section.")
    try:
        print(f"\n\nProcessing section {section_num} of {total_sections}")
        # Process this section with implicit question extraction
        prev_questions_section = [q[1] for q in prev_questions_all if q[0] == section_num]  # Filter questions for this section
        print(f"prev_questions_section: {prev_questions_section}")
        questions = fcall_qa_qonly_implicit(section, fcall_prompt, prev_questions_section, provider=provider)    
                
    except Exception as e:
        error_msg = str(e)
        if error_msg:  # Only log actual errors
            error_msg = f"\n********** Error encountered in section {section_num}: {error_msg}"
            print(colored(error_msg, "red"))
        raise  # Re-raise to abort processing

    prefix="QI"
    # Prepend prefix and section number to each question
    questions = [f"{prefix} {section_num}-{i+1}: {q}" for i, q in enumerate(questions)]
    return questions
    pass
#if __name__ == "__main__":
    cur_file_path = CUR_TRANSCRIPT_FILE_PATH
    section_num = 1
    questions = single_section_qonly_round_2_implicit(cur_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_IMPLICIT_1A, section_num)
    print("Implicit Questions:")
    for question in questions:
        print(question)
FCALL_SYSTEM_PROMPT_QA_QONLY_BLOCKS_1A = """
def tools_qa_qonly_blocks():
"""
    """
def fcall_qa_qonly_block(transcript_section, fcall_prompt, question, provider="openai", debug=False):
    """
    return [{
        "type": "function",
        "function": {
            "name": "extract_final_qa_block",
            "description": (
                "Given a final question (verbatim) and an excerpt of transcript text, extract the best possible answer."
                " Return only ONE QA block containing the relevant data fields. If no answer is found, set verbatim_answer "
                "to 'NO RELEVANT ANSWER IN TRANSCRIPT' and clarified_answer to an empty string or minimal note."
            ),
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "verbatim_question": {
                        "type": "string",
                        "description": (
                            "The exact text from the transcript section text that corresponds to the provided question, minus speaker labels/newlines. The entire text should be on a single line. Do not start the text with the speaker name from the preceding speaker line. If the question is implicit, use the string 'IMPLICIT'."
                        )
                    },
                    "verbatim_answer": {
                        "type": "string",
                        "description": (
                            "The exact text of the answer as it appears in the transcript section text, minus speaker labels/newlines. Do not start the text with the speaker name from the preceding speaker line."
                        )
                    },
                    "clarified_answer": {
                        "type": "string",
                        "description": (
                            "A concise, edited version of the answer. The entire text of this answer should be on a single line. Do not mention any specific speaker names, instead use 'FDA' where appropriate."
                        )
                    },
                    "speaker_question": {
                        "type": "string",
                        "description": (
                            "Name/role of question speaker. The name must be as identified in the transcript by the text in the speaker line that precedes a colon or timestamp. Do not use a different name spelling that may appear in the speaker dialogue. If the question is implied from an Authority Speaker's statement, use 'NOT APPLICABLE'."
                        )
                    },
                    "speaker_answer": {
                        "type": "string",
                        "description": (
                            "Name/role of answer speaker. The name must be as identified in the transcript by the text in the speaker line that precedes a colon or timestamp. Do not use a different name spelling that may appear in the speaker dialogue. If the question is implicit, use the speaker name of the statement that implied the question."
                        )
                    },
                    "topics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "A list of 1-3 key topics addressed in the question-answer block. If no new question is found, return an empty list []."
                        )
                    },
                    "review_flag": {
                        "type": "boolean",
                        "description": (
                            "Set True if significant uncertainty in the response. Otherwise False."
                        )
                    }
                },
                "required": [
                    "verbatim_question", "verbatim_answer", "clarified_answer",
                    "speaker_question", "speaker_answer", "topics", "review_flag"
                ],
                "additionalProperties": False
            }
        }
    }]
    """
def get_last_qa_block_identifier(qa_file_path):
    """
    max_retries = 1  # Maximum attempts to get a QA block
    
    # Get appropriate tools format for the provider
    tools = tools_qa_qonly_blocks()
    if provider == "anthropic":
        tools = convert_tools_to_anthropic_format(tools)
    
    # Create full prompt with question context
    full_prompt = (
        f"{fcall_prompt}\n\n"
        f"<PROVIDED QUESTION>\n{question}\n</PROVIDED QUESTION>\n\n"    
        f"<TRANSCRIPT SECTION>\n{transcript_section}\n</TRANSCRIPT SECTION>\n\n"
        f"Return only a single JSON object, nothing else."
    )
    verbose_print(debug, f"full_prompt: {full_prompt}")

    while max_retries > 0:
        try:
            # Make the appropriate function call based on provider
            if provider == "openai":
                qa_response = openai_function_call(full_prompt, transcript_section, tools)
            elif provider == "anthropic":
                qa_response = anthropic_function_call(full_prompt, transcript_section, tools)
            else:
                raise ValueError("Provider must be either 'openai' or 'anthropic'")
            
            # Parse the response using the common parser
            arguments = parse_function_call_response(qa_response, provider)
            
            if not arguments:
                raise Exception("Failed to parse function call response")
            
            # Create QA block
            qa_block = ""
            qa_block += f"CLARIFIED QUESTION: {question}\n"  # Use the provided question
            qa_block += f"CLARIFIED ANSWER: {arguments['clarified_answer']}\n"
            qa_block += f"VERBATIM QUESTION: {arguments['verbatim_question']}\n"
            qa_block += f"VERBATIM ANSWER: {arguments['verbatim_answer']}\n"
            qa_block += f"SPEAKER QUESTION: {arguments['speaker_question']}\n"
            qa_block += f"SPEAKER ANSWER: {arguments['speaker_answer']}\n"
            qa_block += f"TOPICS: {', '.join(arguments['topics'])}\n"
            qa_block += f"REVIEW FLAG: {arguments['review_flag']}\n"

            return qa_block, None
            
        except Exception as e:
            error_msg = str(e)
            if error_msg:  # Only print error if there's an actual message
                print(colored(f"Error in QA block extraction: {error_msg}", "red"))
            if max_retries > 1:
                max_retries -= 1
                print(colored(f"Error occurred. Retrying... ({max_retries} attempts remaining)", "red"))
                continue
            return None, error_msg
    
    return None, "Max retries exceeded"
    """
def mtest_get_last_qa_block_identifier():
def do_qonly_round_3_blocks(transcript_file_path, fcall_prompt, provider="openai", delimiter='---', suffix_new='_qa-qonly'):
    """
    # Get QA section content
    qa_content = get_heading(qa_file_path, "### qa")
    if not qa_content:
        return None
        
    # Split into blocks and get the last non-empty block
    blocks = [block.strip() for block in qa_content.split('\n\n') if block.strip()]
    if not blocks:
        return None
        
    # Get the first line of the last block which should contain "QA Block X-Y"
    last_block_first_line = blocks[-1].split('\n')[0]
    
    # Parse the section and question numbers using regex
    match = re.match(r'QA Block (\d+)-(\d+)', last_block_first_line)
    if not match:
        return None
        
    # Convert to integers and return as tuple
    section_num = int(match.group(1))
    question_num = int(match.group(2))
    return (section_num, question_num)
    pass
#if __name__ == "__main__":
    qa_file_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/run_auto/2021-12-15_Virtual Town Hall 75_qa-qonly.md"
    section_num, question_num = get_last_qa_block_identifier(qa_file_path)
    print(f"Last QA Block: Section {section_num}, Question {question_num}")
    """
def mrun_do_qonly_round_3_blocks():
def move_removed_qa_blocks(qa_file_path, removed_questions, new_section_name="### removed qa blocks"):
    """
    round_num = 3
    round_name = "QA Blocks Extraction"
    start_time = time.time()

    # Verify QA file exists
    qa_file_path = sub_suffix_in_str(transcript_file_path, suffix_new)
    if not os.path.exists(qa_file_path):
        raise ValueError(f"QA file not found: {qa_file_path}")

    # Get all questions (both explicit and implicit)
    questions_all = get_questions_from_extract_log(qa_file_path)

    # Set model based on provider
    if provider == "openai":
        model = OPENAI_MODEL
    elif provider == "anthropic":
        model = ANTHROPIC_MODEL
    else:
        raise ValueError("Provider must be either 'openai' or 'anthropic'")
    
    # Get transcript sections and metadata
    _, sections, total_sections = get_transcript_metadata_and_sections(transcript_file_path, delimiter)

    # Get the last processed block (if any)
    last_block = get_last_qa_block_identifier(qa_file_path)
    if last_block:
        last_section, last_question = last_block
        print(f"Resuming from after section {last_section}, question {last_question}")
    else:
        last_section = last_question = 0
        # Add a new heading at the end of the file for the QA section
        with open(qa_file_path, 'r+') as f:
            content = f.read().rstrip()  # Remove trailing whitespace/newlines
            f.seek(0)
            f.write(content + "\n\n\n### qa\n\n")  # 3 newlines before, 2 after
            f.truncate()

    # Process each section
    for section_num, section in enumerate(sections, 1):
        section = section.strip()
        if not section:
            raise ValueError(f"Empty section found at position {section_num}")
            
        # Skip sections we've already processed
        if section_num < last_section:
            continue
            
        try:
            print(f"\n========== Round {round_num} {round_name} - Section {section_num} of {total_sections} ==========")
            
            # Get questions for this section
            section_questions = [q[1] for q in questions_all if q[0] == section_num]
            
            # Process each question in this section
            for i, question in enumerate(section_questions, 1):
                # Skip questions we've already processed in the last section
                if section_num == last_section and i <= last_question:
                    continue
                    
                print(f"  Processing question {i} of {len(section_questions)}")
                qa_block, error = fcall_qa_qonly_block(section, fcall_prompt, question, provider=provider)
                if qa_block:
                    # Add QA block identifier at the top
                    qa_block = f"QA Block {section_num}-{i}\n{qa_block}"
                    with open(qa_file_path, 'a') as f:
                        f.write(qa_block + "\n")
                elif error:
                    print(colored(f"Error processing question: {error}", "red"))
                    
        except Exception as e:
            error_msg = str(e)
            if error_msg:  # Only log actual errors
                error_msg = f"\n********** Error encountered in section {section_num}: {error_msg}"
                print(colored(error_msg, "red"))
            raise  # Re-raise to abort processing

    print(f"\n{round_name} completed in {(time.time() - start_time) / 60:.1f} minutes.")
    print(f"{round_name} - QA blocks written to {qa_file_path}")
    return qa_file_path

    pass
#if __name__ == "__main__":
    #cur_transcript_file_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/2020-08-05_Virtual Town Hall 20_fixnames.md"
    cur_transcript_file_path = CUR_TRANSCRIPT_FILE_PATH
    qa_file_path = do_qonly_round_3_blocks(cur_transcript_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_BLOCKS_1A)
    
    print(f"Implicit Round 3 - QA file updated: {qa_file_path}")

    """
def mrun_move_removed_qa_blocks():
def rerun_qa_block_fcall(transcript_file_path, fcall_prompt, first_2_qa_block_lines, provider="openai", delimiter='---', suffix_new='_qa-qonly'):
def mrun_rerun_qa_block_fcall():
    """
    # Get all QA blocks text
    all_blocks_text = get_heading(qa_file_path, "### qa")
    if not all_blocks_text:
        return
    
    # Split into individual blocks (split on double newline)
    all_blocks = [block.strip() for block in all_blocks_text.split('\n\n') if block.strip()]
    
    # Separate blocks into removed and remaining
    removed_blocks = []
    remaining_blocks = []
    
    for block in all_blocks:
        # Check if block matches any of the removed question patterns
        is_removed = False
        for question_id in removed_questions:
            if block.startswith(f"QA Block {question_id}"):
                removed_blocks.append(block)
                is_removed = True
                break
        
        if not is_removed:
            remaining_blocks.append(block)
    
    # Create text content for both sections
    removed_blocks_text = '\n\n'.join(removed_blocks) + '\n\n\n'
    remaining_blocks_text = '\n\n'.join(remaining_blocks) + '\n\n\n'
    
    # Update the file: delete qa section, add removed blocks, then add remaining blocks
    delete_heading(qa_file_path, "### qa")
    set_heading(qa_file_path, removed_blocks_text, new_section_name)
    set_heading(qa_file_path, remaining_blocks_text, "### qa")
    pass
#if __name__ == "__main__":
    qa_file_path = sub_suffix_in_str(CUR_TRANSCRIPT_FILE_PATH, '_qa-qonly')
    removed_questions = ['16-4', '16-5']
    move_removed_qa_blocks(qa_file_path, removed_questions)

    # Verify QA file exists
    qa_file_path = sub_suffix_in_str(transcript_file_path, suffix_new)
    if not os.path.exists(qa_file_path):
        raise ValueError(f"QA file not found: {qa_file_path}")

    # Set model based on provider
    if provider == "openai":
        model = OPENAI_MODEL
    elif provider == "anthropic":
        model = ANTHROPIC_MODEL
    else:
        raise ValueError("Provider must be either 'openai' or 'anthropic'")
    
    # Parse section number and question from input lines
    lines = first_2_qa_block_lines.strip().split('\n')
    if len(lines) < 2:
        raise ValueError("Input must contain at least 2 lines")
    
    # Parse section number from "QA Block X-Y" format
    section_match = re.match(r'QA Block (\d+)-', lines[0])
    if not section_match:
        raise ValueError("First line must be in format 'QA Block X-Y'")
    section_num = int(section_match.group(1))
    
    # Parse question from "CLARIFIED QUESTION: X" format
    question_match = re.match(r'CLARIFIED QUESTION: (.*)', lines[1])
    if not question_match:
        raise ValueError("Second line must start with 'CLARIFIED QUESTION:'")
    question = question_match.group(1)

    # Get transcript sections
    _, sections, _ = get_transcript_metadata_and_sections(transcript_file_path, delimiter)
    
    # Verify section number is valid
    if section_num < 1 or section_num > len(sections):
        raise ValueError(f"Invalid section number: {section_num}")
    
    # Get the specific section we want to process
    section = sections[section_num - 1].strip()
    if not section:
        raise ValueError(f"Empty section found at position {section_num}")

    # Process the single question
    print(f"\nProcessing section {section_num}, question: {question}")
    qa_block, error = fcall_qa_qonly_block(section, fcall_prompt, question, provider=provider)
    
    if qa_block:
        # Add QA block identifier at the top
        qa_block = f"QA Block {section_num}-1\n{qa_block}"
        print("\nGenerated QA Block:")
        print(qa_block)
        return qa_block
    elif error:
        print(colored(f"Error processing question: {error}", "red"))
        return None    
    else:
        print(colored("No QA block generated", "yellow"))
        return None
    pass
#if __name__ == "__main__":
    transcript_file_path = CUR_TRANSCRIPT_FILE_PATH
    first_2_qa_block_lines = """
def search_for_no_answers_in_qa_blocks(qa_file_path):
CLARIFIED QUESTION: How high should the CT values be for low positives in retrospective studies of a rapid antigen test?"""
    rerun_qa_block_fcall(transcript_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_BLOCKS_1A, first_2_qa_block_lines)

#NOTE Can also manually search for 'ANSWER: NO'
    """
def auto_process_qa_qonly(transcript_file_path):
def mrun_auto_process_qa_qonly():
def mrun_auto_process_qa_qonly_folder():
def mrun_auto_check_qa_qonly_folder():
    """
    from primary.structured import get_blocks_from_file
    
    # Search patterns that indicate missing/no answers, ordered from most specific to most general
    NO_ANSWER_PATTERNS = [
        r"^VERBATIM ANSWER:\s*NO\s+(?:RELEVANT\s+)?ANSWER(?:\s+IN\s+TRANSCRIPT)?$",  # Matches exact "NO ANSWER" phrases
        r"^VERBATIM ANSWER:\s*[A-Z\s]+$"  # Matches VERBATIM ANSWER: followed by all caps text
    ]
    
    # Get QA section content
    qa_content = get_heading(qa_file_path, heading="### qa")
    if not qa_content:
        return []
    
    # Store matches with full blocks
    matches = []
    
    # Split content into QA blocks
    qa_blocks = get_blocks_from_file(qa_file_path, heading="### qa")
    
    # Search through blocks
    for block in qa_blocks:
        block_lines = block.split('\n')
        block_matched = False
        for pattern in NO_ANSWER_PATTERNS:
            if block_matched:
                break
            for line in block_lines:
                if re.search(pattern, line):
                    matches.append({
                        'pattern': pattern,
                        'line': line.strip(),
                        'block': block.strip()
                    })
                    block_matched = True
                    break
    
    # Print results
    if not matches:
        print(colored("***** No 'NO ANSWER' matches found *****", "green"))
    else:
        print(colored("***** Found 'NO ANSWER' matches *****", "red"))
        for match in matches:
            print(f"Pattern: {match['pattern']}")
            print(colored(f"Matching line: {match['line']}", "yellow"))
            print(f"{match['block']}")
            print()  # Blank line between matches
        print(f"Total 'NO ANSWER' matches found: {len(matches)}")
        print(colored("*****************************************", "red"))
    return matches
    qa_file_path = sub_suffix_in_str(transcript_file_path, '_qa-qonly')  # can remove this
    
    # Check if QA file exists and has QA section
    qa_content = None
    if os.path.exists(qa_file_path):
        qa_content = get_heading(qa_file_path, "### qa")
        
    # Run all rounds if no QA file or no QA content
    if not os.path.exists(qa_file_path) or not qa_content:
        qa_file_path = do_qonly_round_1_explicit(transcript_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1D)
        qa_file_path = do_qonly_round_2_implicit(transcript_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_IMPLICIT_1A)
        qa_file_path = do_qonly_round_3_blocks(transcript_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_BLOCKS_1A)
    else:
        # Skip first two rounds if QA section exists
        print("QA section found - skipping rounds 1 and 2") 
        qa_file_path = do_qonly_round_3_blocks(transcript_file_path, FCALL_SYSTEM_PROMPT_QA_QONLY_BLOCKS_1A)

    matches = search_for_no_answers_in_qa_blocks(qa_file_path)

    questions_extract_log = get_questions_from_extract_log(qa_file_path, verbose=True)
    print(f"Number of questions in extract log: {len(questions_extract_log)}")
    questions_qa_blocks = get_questions_from_qa_file(qa_file_path, heading="### qa")
    print(f"Number of questions in qa blocks: {len(questions_qa_blocks)}")
    compare_question_tuple_lists(questions_extract_log, questions_qa_blocks, "Extract log", "QA blocks")

    questions_qa_blocks = get_questions_from_qa_file(qa_file_path, heading="### qa")
    embeddings_file_path = generate_and_save_question_embeddings(qa_file_path, questions_qa_blocks)
    _, questions_to_remove, output_text = calc_question_list_similarities(embeddings_file_path)
    print(f"\n\n***** Questions to Remove ***** output_text:\n{output_text}")
    move_removed_qa_blocks(qa_file_path, questions_to_remove)
    pass
#if __name__ == "__main__":
    auto_process_qa_qonly(CUR_TRANSCRIPT_FILE_PATH)
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/run_auto"
    files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_fixnames')
    total_start_time = time.time()
    
    for i, file_path in enumerate(files_to_run, 1):
        print(colored(f"\nAuto Processing file {i}/{len(files_to_run)}: {file_path}", "blue"))
        file_start_time = time.time()
        auto_process_qa_qonly(file_path)
        file_end_time = time.time()
        print(colored(f"Auto Process Time taken for file: {(file_end_time - file_start_time)/60:.1f} minutes", "blue"))
    
    total_end_time = time.time()
    print(f"\nAuto Processed {len(files_to_run)} files in {(total_end_time - total_start_time)/60:.1f} minutes")
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/done_auto"
    qa_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_qa-qonly')
    
    for i, qa_file_path in enumerate(qa_files_to_run, 1):
        print(colored(f"\n{qa_file_path}", "blue"))
        search_for_no_answers_in_qa_blocks(qa_file_path)

SCALL_PROMPT_SECTION_TITLE = """
def write_section_titles(transcript_file_path, scall_prompt, provider="openai", delimiter='---', prepend="\n\n#### ", suffix_new='_section-titles'):
"""
    """
def propagate_section_titles_to_qa(transcript_file_path, section_heading='####', suffix_new='_qa-qonly'):
    """
    start_time = time.time()

    # Set model based on provider
    if provider == "openai":
        model = OPENAI_MODEL
    elif provider == "anthropic":
        model = ANTHROPIC_MODEL
    else:
        raise ValueError("Provider must be either 'openai' or 'anthropic'")

    # Get transcript sections and metadata
    metadata, sections, total_sections = get_transcript_metadata_and_sections(transcript_file_path, delimiter)

    # Update metadata
    current_datetime = get_current_datetime_humanfriendly()
    date = current_datetime.split(' ')[0]
    metadata = set_metadata_field(metadata, "last updated", f"{date} Added Section Titles")
    metadata = set_metadata_field(metadata, "source file", transcript_file_path)

    # Process sections and generate titles
    processed_content = []
    for section_num, section in enumerate(sections, 1):
        section = section.strip()
        if not section:
            continue

        print(f"\nProcessing section {section_num} of {total_sections}")
        try:
            # Generate section title based on provider
            if provider == "openai":
                title = simple_openai_chat_completion_request(scall_prompt + "\n\n" + section, model)
            elif provider == "anthropic":
                title = simple_anthropic_chat_completion_request(scall_prompt + "\n\n" + section, model)
            else:
                raise ValueError("Provider must be either 'openai' or 'anthropic'")
            
            # Add section with title
            processed_content.append(f"{prepend} {section_num}. {title.strip()}\n")  # Title with heading format
            processed_content.append(section)
            print(colored(title.strip(), "blue"))
            
        except Exception as e:
            error_msg = f"\n********** Error generating title for section {section_num}: {str(e)}"
            print(colored(error_msg, "red"))
            processed_content.append(section)  # Include original section without title
            continue

    # Create output file with processed content
    initial_content = "## content\n\n### transcript"
    new_content = initial_content + "\n".join(processed_content)
    new_file_path = write_metadata_and_content(
        transcript_file_path, 
        metadata, 
        new_content, 
        overwrite='no-sub', 
        suffix_new=suffix_new
    )

    print(f"\nSection titles generation completed in {(time.time() - start_time) / 60:.1f} minutes.")
    print(colored("New file written to " + new_file_path, "green"))
    return new_file_path
    """
def mrun_section_titles():
### ADD SECTIONS (1,215 tokens)
def get_speaker_lines_by_speakers(file_path, remove_speakers, remove_duplicates=False, verbose=False):
    """
    # Verify QA file exists
    qa_file_path = sub_suffix_in_str(transcript_file_path, suffix_new)
    if not os.path.exists(qa_file_path):
        raise ValueError(f"QA file not found: {qa_file_path}")

    # Get transcript lines from the transcript section
    transcript_text = get_heading(transcript_file_path, "### transcript")
    transcript_lines = transcript_text.splitlines()

    # Extract section titles with their numbers
    section_titles = {}
    for line in transcript_lines:
        if line.strip().startswith(section_heading):
            # Extract section number and title
            match = re.match(rf"{section_heading}\s+(\d+)\.\s+(.+)", line.strip())
            if match:
                section_num = int(match.group(1))
                section_title = line.strip()  # Keep full heading line
                section_titles[section_num] = section_title

    # Get QA lines
    qa_text = get_heading(qa_file_path, "### qa")
    qa_lines = qa_text.splitlines()

    # Process QA lines and insert section titles
    new_qa_lines = []
    current_section = None
    
    for line in qa_lines:
        # Check for QA block header
        match = re.match(r'QA Block (\d+)-', line.strip())
        if match:
            section_num = int(match.group(1))
            # If this is a new section and we have a title for it
            if section_num != current_section and section_num in section_titles:
                if new_qa_lines:  # Add extra newline if not at the start
                    new_qa_lines.append('')
                new_qa_lines.append(section_titles[section_num])
                new_qa_lines.append('')  # Add blank line after title
                current_section = section_num
        new_qa_lines.append(line)

    # Join the lines and ensure proper spacing
    new_qa_text = '\n'.join(new_qa_lines).strip() + '\n\n'
    
    # Write the updated text back using set_heading
    set_heading(qa_file_path, new_qa_text, "### qa")

    print(f"Section titles propagated to QA file: {qa_file_path}")
    return qa_file_path
    pass
#if __name__ == "__main__":
    # cur_file_path = "tests/test_manual_files/md_to_html/2020-12-09_Virtual Town Hall 36_fixnames.md"
    # write_section_titles(cur_file_path, SCALL_PROMPT_SECTION_TITLE)
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/done_auto"
    #files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_fixnames')
    files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_section-titles')

    for i, file_path in enumerate(files_to_run, 1):
        #write_section_titles(file_path, SCALL_PROMPT_SECTION_TITLE)
        propagate_section_titles_to_qa(file_path)

    """
def mtest_get_speaker_lines_by_speakers():
def get_speaker_lines_by_perfect_segments(eval_seg_csv_path, ref_transcript_path):
def add_transcript_section_delimiters(file_path, line_numbers, delimiter="---"):
    """
    # Get the heading text and find the starting line number
    transcript = get_heading(file_path, "### transcript")
    if transcript is None:
        print(f"No transcript found in {file_path}")
        return []
    
    # Count lines until we find the heading to get the correct line number
    heading_line_start = find_line_number_in_file(file_path, "### transcript")
    
    speaker_lines = []
    lines = transcript.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Handle lines ending with colon
        if line.endswith(':'):
            speaker_full = line.rstrip(' :')  # Remove colon and whitespace
            absolute_line_num = heading_line_start + i
            speaker_lines.append((speaker_full, absolute_line_num))
            
        # Handle lines with timestamp following speaker name
        else:
            timestamp, index = get_timestamp(line)
            if index is not None:
                speaker_full = line[:index].strip()
                absolute_line_num = heading_line_start + i
                speaker_lines.append((speaker_full, absolute_line_num))
    
    # Remove specified speakers
    if remove_speakers:
        speaker_lines = [
            (speaker, line_num) 
            for speaker, line_num in speaker_lines 
            if not any(rm_speaker.lower() in speaker.lower() for rm_speaker in remove_speakers)
        ]
    
    # Remove consecutive duplicates if requested
    if remove_duplicates and speaker_lines:
        filtered_lines = [speaker_lines[0]]  # Keep first entry
        for current in speaker_lines[1:]:
            if current[0] != filtered_lines[-1][0]:  # Compare speaker_full strings
                filtered_lines.append(current)
        speaker_lines = filtered_lines
    
    if verbose:
        for speaker, line_num in speaker_lines:
            print(f"({speaker}, {line_num})")
    return speaker_lines
    pass
#if __name__ == "__main__":
    cur_file_path = "data/floodlamp/reg/fda-townhalls/dev-qa-extract/VTH 36_cemanual.md"
    speaker_lines = get_speaker_lines_by_speakers(cur_file_path, remove_speakers=["FDA"], remove_duplicates=True, verbose=True)
    pass
    """
def mrun_add_transcript_section_delimiters():
def mrun_add_transcript_section_delimiters_folder():
### OLD PROMPTS (883 tokens)
def tools_qonly_explicit_list():  # not tried - think this is incorrect format
    """
    # Read all lines from file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Convert line numbers from 1-based to 0-based indexing
    zero_based_lines = [line_num - 1 for line_num in line_numbers]
    
    # Check if any line numbers are out of bounds
    if any(line_num >= len(lines) for line_num in zero_based_lines):
        raise ValueError(f"Line numbers {[ln + 1 for ln in zero_based_lines if ln >= len(lines)]} are out of bounds. File has {len(lines)} lines.")
    
    # Check if specified lines are blank
    non_blank_lines = []
    for line_num in zero_based_lines:
        line_content = lines[line_num].replace('\n', '').replace('\r', '')
        if line_content:  # If line contains anything after removing newlines
            print(f"Line {line_num + 1} content: '{lines[line_num]}'")  # Debug print (showing 1-based line numbers)
            non_blank_lines.append(line_num + 1)  # Convert back to 1-based for error message
    
    if non_blank_lines:
        raise ValueError(f"The following line numbers are not blank: {non_blank_lines}\nFor file: {file_path}")
    
    # Add delimiters
    for line_num in zero_based_lines:
        lines[line_num] = delimiter + '\n'
    
    # Write modified content back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Added {len(line_numbers)} section delimiters to file: {file_path}")
    pass
#if __name__ == "__main__":
    cur_file_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/2020-05-20_Virtual Town Hall 9_fixnames.md"
    speaker_tuples = get_speaker_lines_by_speakers(cur_file_path, remove_speakers=["FDA"], remove_duplicates=True)
    
    # Extract line numbers and subtract 1 from each
    prev_line_numbers = [line_num - 1 for _, line_num in speaker_tuples]
    print(f"prev_line_numbers: {prev_line_numbers}")
    add_transcript_section_delimiters(cur_file_path, prev_line_numbers)
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/run_delimiter"
    files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_fixnames')
    total_start_time = time.time()
    
    for i, file_path in enumerate(files_to_run, 1):
        speaker_tuples = get_speaker_lines_by_speakers(file_path, remove_speakers=["FDA"], remove_duplicates=True)
        # Extract line numbers and subtract 1 from each
        prev_line_numbers = [line_num - 1 for _, line_num in speaker_tuples]
        print(f"prev_line_numbers: {prev_line_numbers}")
        add_transcript_section_delimiters(file_path, prev_line_numbers)  


    return [{
        "type": "function",
        "function": {
            "name": "extract_explicit_questions",
            "description": "Return a list of clarified questions extracted from the transcript. Each question is explicitly asked in the text.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "clarified_questions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "An array of clarified question strings, each representing a distinct explicit question."
                    }
                },
                "required": ["clarified_questions"],
                "additionalProperties": False
            }
        }
    }]
FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1A = """
"""
FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1B_o1pro = """
"""
FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1C = """
### NOT USED - LLM SECTIONS (687 tokens)
"""

PROMPT_MEETING_SECTIONS_1 = """
def scall_meeting_sections(file_path, system_prompt, heading="### transcript"):
"""
    # Get the heading text and find the starting line number
    heading_text = get_heading(file_path, heading)
    
    # Count lines until we find the heading to get the correct line number
    heading_line_start = find_line_number_in_file(file_path, heading)
    #print(f"heading line start: {heading_line_start}")
    
    # Get the response from OpenAI
    prompt = system_prompt + heading_text
    response = simple_openai_chat_completion_request(prompt, model=OPENAI_MODEL)
    print(f"response: {response}")
    
    # Convert string response to Python list
    # Remove brackets and split by commas
    numbers_str = response.strip('[]').split(',')
    # Convert strings to integers and add heading_line_start to each
    line_numbers = [int(num.strip()) + heading_line_start for num in numbers_str]
    
    return line_numbers
PROMPT_MEETING_SECTIONS_2 = """
"""
TOOLS_MEETING_SECTIONS_2 = [{
    "type": "function",
    "function": {
        "name": "analyze_meeting_sections",
        "description": "Analyze FDA town hall transcript to identify natural section breaks at topic transitions",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "line_numbers": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": """
                    """
                }
            },
            "required": ["line_numbers"],
            "additionalProperties": False
        }
    }
}]
PROMPT_MEETING_SECTIONS_sonnet_rules = """
"""
TOOLS_MEETING_SECTIONS_sonnet_rules = [{
    "type": "function",
    "function": {
        "name": "analyze_meeting_sections",
        "description": "Analyze FDA town hall transcript to identify natural section breaks at complete Q&A transitions",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "line_numbers": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": """
                    """
                }
            },
            "required": ["line_numbers"],
            "additionalProperties": False
        }
    }
}]
PROMPT_MEETING_SECTIONS = """
"""
TOOLS_MEETING_SECTIONS = [{
    "type": "function",
    "function": {
        "name": "analyze_meeting_sections",
        "description": "Analyze a transcript to identify natural section breaks at topic transitions",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "line_numbers": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": """
def fcall_meeting_sections(file_path, system_prompt=PROMPT_MEETING_SECTIONS, heading="### transcript"):
                    """
                }
            },
            "required": ["line_numbers"],
            "additionalProperties": False
        }
    }
}]
    """
def get_delimiter_line_numbers(file_path, heading="### transcript", delimiter="---"):
### QA EVAL (1,561 tokens)
def validate_qa_transcript_positions(transcript, qa_dict):
    """
    # Get the heading text and find the starting line number
    heading_text = get_heading(file_path, heading)
    heading_line_start = find_line_number_in_file(file_path, heading)
    
    # Get the response from OpenAI using function calling
    response = openai_function_call(system_prompt, heading_text, TOOLS_MEETING_SECTIONS)
    
    if response and "tool_calls" in response:
        try:
            # Extract and parse the function arguments
            arguments_json = response['tool_calls'][0]['function']['arguments']
            arguments = json.loads(arguments_json)
            
            # Get the line numbers and adjust them by the heading start line
            line_numbers = [num + heading_line_start for num in arguments['line_numbers']]
            return line_numbers
            
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error processing function call response: {str(e)}")
            return []
    
    print("No valid response received from function call")
    return []
    # Get the heading text and find the starting line number
    transcript = get_heading(file_path, heading)
    
    # Count lines until we find the heading to get the correct line number
    heading_line_start = find_line_number_in_file(file_path, heading)
    #print(f"heading line start: {heading_line_start}")
    
    # Get line numbers relative to heading and add heading_line_start
    delimiter_line_numbers = [i + heading_line_start for i, line in enumerate(transcript.splitlines()) if delimiter in line]
    return delimiter_line_numbers


    """
def evaluate_qa_extraction(transcript, qa_file_path):
    """
    start_pos = int(qa_dict['TRANSCRIPT START POSITION'].replace(',', ''))
    end_pos = int(qa_dict['TRANSCRIPT END POSITION'].replace(',', ''))
    
    original_text = transcript[start_pos:end_pos].strip()
    extracted_text = (qa_dict['VERBATIM QUESTION'] + ' ' + qa_dict['VERBATIM ANSWER']).strip()
    
    # Remove any newlines and extra spaces for comparison
    original_text = ' '.join(original_text.split())
    extracted_text = ' '.join(extracted_text.split())
    
    if original_text == extracted_text:
        return True, ""
    else:
        return False, f"Mismatch between original and extracted text.\n    ORIGINAL TRANSCRIPT: '{original_text}'\n    EXTRACTED VERBATIM: '{extracted_text}'"
    """
    """
    from primary.structured import get_all_fields_dict, count_blocks
    _, qa_content = read_metadata_and_content(qa_file_path)
    
    # Split the QA content into blocks, excluding empty blocks and those starting with '#'
    qa_blocks = [block for block in qa_content.split('\n\n') if block.strip() and not block.strip().startswith('#')]
    evaluation_results = []

    num_blocks = count_blocks(qa_file_path)
    
    for i, block in enumerate(qa_blocks, start=1):
        # if i == 4:  # Debug: Process only the first two blocks
        #     break
        qa_dict = get_all_fields_dict(block)
        
        # Perform position validation
        #print(f"DEBUG\n{qa_dict}")
        position_valid, mismatch_description = validate_qa_transcript_positions(transcript, qa_dict)
        
        # Prepare input for LLM evaluation
        eval_prompt = f"""
def generate_evaluation_report(evaluation_results, output_file):
        """
        
        # Make LLM call for evaluation using openai_chat_completion_request
        messages = [
            {"role": "system", "content": "You are an expert evaluator of text extraction quality."},
            {"role": "user", "content": eval_prompt}
        ]
        response = openai_chat_completion_request(messages, model=OPENAI_MODEL)
        
        if isinstance(response, Exception):
            print(f"Error in LLM call: {response}")
            continue
        
        try:
            llm_evaluation = json.loads(response.json()['choices'][0]['message']['content'])
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON from LLM response")
            continue
        except KeyError:
            print("Error: Unexpected response structure from LLM")
            continue
        
        # Combine all evaluation results
        evaluation_result = {
            "accuracy_score": llm_evaluation["accuracy_score"],
            "formatting": llm_evaluation["formatting"],
            "topic_relevance": llm_evaluation["topic_relevance"],
            "position_validation": "Pass" if position_valid else "Fail",
            "mismatch_description": mismatch_description,
            "llm_comments": llm_evaluation["comments"]
        }
        
        print(f"\nAuto Evaluation of block {i} of {num_blocks}")
        print(f"CLARIFIED QUESTION: {qa_dict['CLARIFIED QUESTION']}")
        print(evaluation_result)
        evaluation_results.append(evaluation_result)
    
    return evaluation_results
    """
def run_automated_evaluation(transcript_file, qa_file):
    """
    with open(output_file, 'w') as f:
        f.write("# QA Extraction Auto Evaluation Report\n\n\n")
        
        # Calculate and write summary statistics
        avg_accuracy = sum(r['accuracy_score'] for r in evaluation_results) / len(evaluation_results)
        formatting_pass = sum(1 for r in evaluation_results if r['formatting'] == "Pass")
        topic_relevance_pass = sum(1 for r in evaluation_results if r['topic_relevance'] == "Pass")
        position_validation_pass = sum(1 for r in evaluation_results if r['position_validation'] == "Pass")
        
        f.write("## Summary Statistics:\n")
        f.write(f"Average Accuracy Score: {avg_accuracy:.2f}/5\n")
        f.write(f"Formatting Pass Rate: {formatting_pass}/{len(evaluation_results)}\n")
        f.write(f"Topic Relevance Pass Rate: {topic_relevance_pass}/{len(evaluation_results)}\n")
        f.write(f"Position Validation Pass Rate: {position_validation_pass}/{len(evaluation_results)}\n\n\n")
        
        for i, result in enumerate(evaluation_results, 1):
            f.write(f"## QA Block {i}:\n")
            f.write(f"Accuracy Score: {result['accuracy_score']}/5\n")
            f.write(f"Formatting: {result['formatting']}\n")
            f.write(f"Topic Relevance: {result['topic_relevance']}\n")
            f.write(f"Position Validation: {result['position_validation']}\n")
            if result['mismatch_description']:
                f.write(f"Mismatch Description: {result['mismatch_description']}\n")
            f.write(f"LLM Comments: {result['llm_comments']}\n\n")
    """
    """
    transcript = get_heading(transcript_file, "### transcript")
    transcript = transcript.lstrip('### transcript').rstrip('\n').lstrip('\n*')
    
    evaluation_results = evaluate_qa_extraction(transcript, qa_file)
    
    output_file = manage_file_overwrite(qa_file, "_autoeval", overwrite="no")
    generate_evaluation_report(evaluation_results, output_file)
    
    print(f"Evaluation completed. Report written to {output_file}")

PROMPT_QUESTION_ERRORS = """
def create_question_errors_file(file_path, split_file_function, prompt, *args, **kwargs):
"""
    """

## primary/vectordb.py (3,333 tokens)
### VECTOR DB SUPPORT (2,906 tokens)
def generate_embedding(text, model=EMBEDDING_MODEL):
    """
    blocks_file_path = split_file_function(file_path, *args, **kwargs)
    errors_file_path = scall_replace(blocks_file_path, prompt, retain_delimiters=True, suffix_new='_errors')
    delete_file(blocks_file_path)
    return errors_file_path

#===== END OF FILE primary/llm.py =====




#===== START OF FILE primary/vectordb.py =====
#Library for vector database operations

import sys
import os
import json
import zipfile
import shutil
from datetime import datetime

from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

#Exclude for qrag chalicelib
from langchain_pinecone import Pinecone as LangchainPinecone
from langchain_community.document_loaders import ObsidianLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


#---API KEYS AND SECRETS---
from dotenv import load_dotenv
load_dotenv(override=True)  # Load environment variables from .env file
OPENAI_API_KEY = os.environ["OPENAI_API_KEY_LOCAL"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]


#---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

VZIP_LOG_FOLDER = 'logs/vectordb_pinecone_log_zips/'
EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI 1536 dimensions and $0.02/1M tokens - batch is 1/2 that, large is $.13)

#These vector db wrapper functions are used manually and are not called by the rag_bots functions. (RT 6-10-2024)
#Pinecone indexes can be seen in the pinecone.io portal > go to Serverless in UL - login sends email to fofgeneral20


    """ 
def generate_vectors_qa(folder_paths, suffixpat_include, include_subfolders=True, embedding_field='QUESTION', date_from_filename=False):
    """
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    response = openai_client.embeddings.create(input=text,
    model=model)
    embedding = response.data[0].embedding
    return embedding

#TODO review the timestamp lines
    """
def vectors_to_json(vectors, file_path):
    """
    from primary.fileops import get_files_in_folder, get_timestamp
    from primary.structured import get_blocks_from_file, get_all_fields_dict, validate_iso_dates_in_filename, validate_blocks_in_folders

    # Pre-validate ISO dates if date_from_filename is True
    if date_from_filename:
        if not validate_iso_dates_in_filename(folder_paths, suffixpat_include):
            raise ValueError("Invalid ISO date format found in one or more filenames")
    
    # Pre-validate that all blocks have the required embedding field
    required_fields = [embedding_field]
    invalid_file = validate_blocks_in_folders(folder_paths, required_fields, {}, suffixpat_include)
    if invalid_file:
        raise ValueError(f"Missing required embedding field '{embedding_field}' in file: {invalid_file}")

    vectors = []
    total_files = 0
    num_vectors = 0
    print("\nStarting vector generation...")
    
    for folder_path in folder_paths:
        file_paths = get_files_in_folder(folder_path, suffixpat_include=suffixpat_include, include_subfolders=include_subfolders)
        total_files += len(file_paths)
        for i, path in enumerate(file_paths, 1):
            file_name_with_extension = os.path.basename(path)
            print(f"Generating vectors for file {i}/{len(file_paths)}: {file_name_with_extension}")
            
            blocks = get_blocks_from_file(path)
            block_num = 0
            file_name_with_extension = os.path.basename(path)
            
            # Extract date from filename if enabled (we know it's valid at this point)
            if date_from_filename:
                date_str = file_name_with_extension.split('_')[0]
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                # Convert to Unix timestamp for Pinecone metadata
                date_timestamp_unix = int(file_date.timestamp())
            
            for block in blocks:
                fields = get_all_fields_dict(block)
                fields['SOURCE'] = file_name_with_extension
                
                # Add date metadata as timestamp if enabled
                if date_from_filename:
                    fields['DATE'] = date_timestamp_unix  # Store as Unix timestamp instead of ISO string
                
                vector_id = (os.path.splitext(file_name_with_extension)[0] + "_" + str(block_num)).replace(" ", "_")
                
                text_to_embed = fields[embedding_field]
                embedding = generate_embedding(text_to_embed)
                
                vector = {'id': vector_id, 'values': embedding, 'metadata': fields}
                vectors.append(vector)
                num_vectors += 1
                block_num += 1
                
    print(f"Vectors generated for {total_files} files - number of vectors: {num_vectors}")
    return vectors

    """
def json_to_vectors(file_path):
    """

    try:
        # Write the JSON data to a file
        with open(file_path, 'w') as json_file:
            json.dump(vectors, json_file, indent=4)
        print(f"Successfully created {file_path}.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    """
def validate_vectors(vectors, required_fields=None, verbose=False):
    """
    try:
        with open(file_path, 'r') as json_file:
            vectors = json.load(json_file)
        print(f"Successfully loaded {file_path}.")
        return vectors
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

    """ 
def upsert_vectors_pinecone(vectors, vector_index_name, new_index=True):
    """
    if required_fields is None:
        required_fields = ["QUESTION", "ANSWER", "QUESTION NAME", "ANSWER NAME", "TOPICS", "STARS", "SOURCE"]
    
    for i, vector in enumerate(vectors):
        if not isinstance(vector.get('id'), str):
            raise ValueError(f"Vector {i}: Missing or invalid 'id'. It should be a string.")
        if not isinstance(vector.get('values'), list) or not all(isinstance(v, float) for v in vector.get('values', [])):
            raise ValueError(f"Vector {i}: Missing or invalid 'values'. It should be a list of floats.")
        if 'metadata' not in vector or not isinstance(vector['metadata'], dict):
            raise ValueError(f"Vector {i}: Missing or invalid 'metadata'. It should be a dictionary.")
        
        for field in required_fields:
            if field not in vector['metadata']:
                raise ValueError(f"Vector {i}: Missing required field '{field}' in metadata.")
        
        if verbose:
            print(f"Validated vector {i}: id={vector['id']}, metadata fields: {', '.join(vector['metadata'].keys())}")
    
    print(f"All {len(vectors)} vectors have required fields and correct format.")

    """ 
def delete_pinecone_index(vector_index_name, user_prompt=True):
    """
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if new_index:
        if vector_index_name not in pc.list_indexes().names():
            pc.create_index(
                name=vector_index_name, 
                dimension=1536, 
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-west-2')
            )
    index = pc.Index(vector_index_name)
    
    # Break up the vectors list into chunks of 100
    for i in range(0, len(vectors), 100):
        batch = vectors[i:i+100]
        index.upsert(vectors=batch)

#don't use - manually delete in pinecone portal before overwriting
    """
def update_pinecone_index_list_md(file_name='pinecone_index_list.md', log_folder_path=VZIP_LOG_FOLDER):
    """
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if vector_index_name in pc.list_indexes().names():
        if user_prompt:
            user_input = input(f"Vector DB Pinecone Index '{vector_index_name}' already exists. Are you sure you want to delete it? (yes/no): ")
            if user_input.lower() != 'yes':
                print(f"Index '{vector_index_name}' was not deleted.")
                return False
        pc.delete_index(vector_index_name)
        print(f"Deleted existing index: {vector_index_name}")
        return True
    else:
        print(f"Index '{vector_index_name}' does not exist.")
        return False

    """
def save_splits_to_json(all_chunks, output_base_filename, metadata, log_folder_path=VZIP_LOG_FOLDER):
    """
    from primary.fileops import get_current_datetime_humanfriendly

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_names = pc.list_indexes().names()

    file_path = os.path.join(log_folder_path, file_name)
    
    with open(file_path, 'w') as f:
        # Write the last updated line
        last_updated = get_current_datetime_humanfriendly()
        f.write(f"Last updated: {last_updated}\n\n")
        
        # Write the list of indices
        for index_name in index_names:
            f.write(f"- {index_name}\n")
    
    print(f"Updated Pinecone index list in {file_path}")

    """
def setup_create_vectordb(folder_paths, vector_index_base, suffixpat_include=None):
    """
    # Create the full output filename
    output_filename = f"{log_folder_path}{output_base_filename}.json"

    # Organize content by source
    content_by_source = {}
    for doc in all_chunks:
        source = doc.metadata.get('source', 'Unknown source')
        if source not in content_by_source:
            content_by_source[source] = {"num_chunks": 0, "chunks": []}
        content_by_source[source]["num_chunks"] += 1
        content_by_source[source]["chunks"].append(doc.page_content)

    # Update metadata
    if "total_chunks (vectors)" in metadata:
        metadata["total_chunks"] = metadata.pop("total_chunks (vectors)")

    # Prepare the data structure
    data = {
        "metadata": metadata,
        "content": {
            "chunks_by_source": content_by_source
        }
    }

    # Save the data to a JSON file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Get the full path of the saved file
    json_full_path = os.path.abspath(output_filename)

    print(f"\nSaved {len(all_chunks)} splits from {len(content_by_source)} sources to {json_full_path}")
    return json_full_path

    """
def check_and_create_pinecone_index(vector_index_name, dimension=1536, metric='cosine'):
    """
    from primary.fileops import get_files_in_folder, get_current_datetime_filefriendly
    import inspect

    # Get the name of the calling function
    calling_function = inspect.stack()[1].function
    print(f"Running {calling_function}!!")

    file_count = 0
    all_file_paths = []
    for folder in folder_paths:
        folder_file_paths = get_files_in_folder(folder, suffixpat_include=suffixpat_include)
        folder_file_count = len(folder_file_paths)
        all_file_paths += folder_file_paths
        file_count += len(folder_file_paths)
        print(f"Including folder: {folder} with {folder_file_count} files.")
    print(f"Total file count: {file_count}")

    datetime = get_current_datetime_filefriendly()
    date_nodashes = datetime.split('_')[0].replace('-', '')
    timestamp = datetime.split('_')[1]
    vector_index_name = vector_index_base + f"-{file_count}f-{date_nodashes}"
    vector_index_name_with_timestamp = vector_index_base + f"-{file_count}f_{datetime}"

    return vector_index_name, vector_index_name_with_timestamp, datetime, all_file_paths

    """
def log_zip_vectordb(vectors_file_path, vector_index_name_with_timestamp, metadata, file_paths_list, log_folder_path=VZIP_LOG_FOLDER):
    """
    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

    # Initialize Pinecone
    print(f"Initializing Pinecone and checking for the existence of vector index: {vector_index_name}")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    while True:
        # Check if the index already exists
        if vector_index_name in pc.list_indexes().names():
            print(f"The index '{vector_index_name}' already exists in Pinecone.\nPlease manually delete the Pinecone vector DB index in the Pinecone portal if you want to continue.")
            user_input = input("Do you want to continue after deleting the index? (yes/no): ").strip().lower()
            if user_input not in ["yes", "y"]:
                print("Aborting create_vectordb: User chose not to continue.")
                return False
        else:
            break
    
    # Create new Pinecone index
    pc.create_index(
        name=vector_index_name,
        dimension=dimension,
        metric=metric,
        spec=ServerlessSpec(cloud='aws', region='us-west-2'),
        # deletion_protection = "enabled"  # don't use now but consider later
    )
    print(f"Created new index: {vector_index_name}")
    
    return True

    """
### VECTOR DB CREATION (419 tokens)
def create_vectordb_vrag_langchain(folder_paths, vector_index_base, suffixpat_include=None, skip_pinecone=False):  # pinecone index names can only contain - and not _ 
    """
    log_file_name = f"vectordb-log_{vector_index_name_with_timestamp}.md"
    log_file_path = os.path.join(log_folder_path, log_file_name)
    
    log_entry = f"{log_file_path}\n\n"

    for key, value in metadata.items():
        log_entry += f"{key}: {value}\n"

    log_entry += "\nfile paths:\n"
    log_entry += "\n".join(f"    {path}" for path in file_paths_list)
    log_entry += "\n"

    os.makedirs(log_folder_path, exist_ok=True)
    
    with open(log_file_path, 'w') as f:
        f.write(log_entry)

    print(f"Logging entry added to {log_file_path}")

    # Create zip file of source documents
    zip_file_path = os.path.join(log_folder_path, f'vectordb-zip_{vector_index_name_with_timestamp}.zip')
    
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for file_path in file_paths_list:
            zipf.write(file_path, os.path.join('vectordb-sources', os.path.basename(file_path)))
        zipf.write(log_file_path, os.path.basename(log_file_path))
        zipf.write(vectors_file_path, os.path.basename(vectors_file_path))

    print(f"Source files, vectors file, and log zipped to {zip_file_path}")

    # Delete the original vectors file after zipping
    os.remove(vectors_file_path)
    print(f"Deleted the original vectors file: {vectors_file_path}")

    return log_file_path, zip_file_path


    """ 
def create_qrag_vectordb(folder_paths, vector_index_base, suffixpat_include=None, embedding_field="QUESTION", date_from_filename=False):

## primary/rag.py (4,498 tokens)
### RETRIEVAL (1,616 tokens)
def pinecone_retriever(query, vector_index_name, num_chunks, date_range=None):
    """ 
    from primary.fileops import apply_to_folder, create_new_file_from_heading, sub_suffix_in_file, move_files_with_suffix, remove_timestamp_links, find_and_replace_pairs
    
    # os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY_CONFIG_LLM  # 10-4-24 commented out - think we can delete this

    # Setup vector database creation
    vector_index_name, vector_index_name_with_timestamp, datetime, all_file_paths = setup_create_vectordb(folder_paths, vector_index_base, suffixpat_include)
    
    # Check and create Pinecone index, and get user confirmation
    if not skip_pinecone:
        if not check_and_create_pinecone_index(vector_index_name):
            return

    all_docs = []

    for folder_path in folder_paths:
        # Create a temporary folder for VRAG sources, removing it if it already exists
        temp_folder_path = VZIP_LOG_FOLDER + "_temp_vrag_sources"
        if os.path.exists(temp_folder_path):
            shutil.rmtree(temp_folder_path)
        os.makedirs(temp_folder_path)

        apply_to_folder(create_new_file_from_heading, folder_path, heading='## content', suffix_new='_temp', suffixpat_include=suffixpat_include, remove_heading=True)
        move_files_with_suffix(folder_path, temp_folder_path, '_temp')
        apply_to_folder(sub_suffix_in_file, temp_folder_path, '')
        apply_to_folder(remove_timestamp_links, temp_folder_path)
        
        # Define find and replace pairs to remove newline after unlinked timestamp
        regex_spk_compress = [(r'(\s*[A-Za-z\s]+\s+(?:\d+:)?\d+:\d+)\n', r'\1  ')]
        apply_to_folder(find_and_replace_pairs, temp_folder_path, regex_spk_compress, use_regex=True)
        print(f"SUCCESS: Extracted transcript sections to temporary files in {temp_folder_path}")
        
        # Load documents from Obsidian vault
        loader = ObsidianLoader(temp_folder_path)
        docs = loader.load()
        all_docs.extend(docs)
        print(f"SUCCESS: Loaded {len(docs)} documents from {folder_path}")
        
        if not skip_pinecone:
            shutil.rmtree(temp_folder_path)
            print(f"CLEANUP: Removed temporary files from {temp_folder_path}")

    # Split documents into chunks
    target_chunk_size = 1000
    chunk_overlap = 150
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=target_chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = text_splitter.split_documents(all_docs)
    print(f"SUCCESS: Split {len(all_docs)} documents into {len(all_chunks)} splits with a target chunk size of {target_chunk_size}")

    if not skip_pinecone:
        # Populate vector store in Pinecone cloud database
        print("PROCESS: Populating vector store in Pinecone cloud database.")
        LangchainPinecone.from_documents(documents=all_chunks, embedding=OpenAIEmbeddings(), index_name=vector_index_name)
        print(f"SUCCESS: Populated and saved vector store in Pinecone cloud database.")

    # Logging vectordb index creation
    metadata = {
    "create vector function": "create_vectordb_vrag_langchain",
    "date and time": datetime,
    "pinecone vector_index_name": vector_index_name,
    "folder_paths": folder_paths,
    "suffixpat_include": suffixpat_include,
    "total_files": len(all_file_paths),
    "total_chunks": len(all_chunks),
    "text_splitter": "Langchain RecursiveCharacterTextSplitter",
    "target_chunk_size": target_chunk_size,
    "chunk_overlap": chunk_overlap
    }
    
    # Convert splits to JSON and save to file
    vectors_file_path = save_splits_to_json(all_chunks, f"vectordb-splits_{vector_index_name_with_timestamp}", metadata)
    print(f"SUCCESS: Saved splits to JSON file at {vectors_file_path}")
    
    # Create log file and zip source documents
    log_file_path, vectordb_zip_path = log_zip_vectordb(vectors_file_path, vector_index_name_with_timestamp, metadata, all_file_paths, VZIP_LOG_FOLDER)

    print(f"Logging completed. Log file created at {log_file_path}")
    print(f"Source files zipped to {vectordb_zip_path}")

    update_pinecone_index_list_md()
    return log_file_path

    # Set OpenAI and Pinecone API keys
    #os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY_CONFIG_LLM  # 10-4-24 commented out - think we can delete this
    
    # Setup vector database creation
    vector_index_name, vector_index_name_with_timestamp, datetime, all_file_paths = setup_create_vectordb(folder_paths, vector_index_base, suffixpat_include)
    print("If you are replacing the vector database, you can go to the Pinecone portal and delete the existing index now.")

    # Generate vectors - Fix the parameter order
    vectors = generate_vectors_qa(
        folder_paths, 
        suffixpat_include,
        include_subfolders=True,  # Explicitly name the parameter
        embedding_field=embedding_field,
        date_from_filename=date_from_filename
    )

    # Check and create Pinecone index, and get user confirmation
    if not check_and_create_pinecone_index(vector_index_name):
        return None

    # Upsert vectors to Pinecone
    upsert_vectors_pinecone(vectors, vector_index_name)
    
    # Prepare metadata
    metadata = {
        "create vector function": "create_qrag_vectordb",
        "date and time": datetime,
        "pinecone vector_index_name": vector_index_name,
        "folder_paths": folder_paths,
        "suffixpat_include": suffixpat_include,
        "embedding_field": embedding_field,
        "date_from_filename": date_from_filename,
        "total_files": len(all_file_paths),
        "total_vectors": len(vectors),
    }

    # Save vectors to JSON
    vectors_file_path = f"{VZIP_LOG_FOLDER}vectordb-vectors_{vector_index_name_with_timestamp}.json"
    vectors_to_json(vectors, vectors_file_path)

    # Create log file and zip source documents
    log_file_path, vectordb_zip_path = log_zip_vectordb(vectors_file_path, vector_index_name_with_timestamp, metadata, all_file_paths, VZIP_LOG_FOLDER)

    print(f"Logging completed. Log file created at {log_file_path}")
    print(f"Source files zipped to {vectordb_zip_path}")

    update_pinecone_index_list_md()
    return log_file_path


#===== END OF FILE primary/vectordb.py =====




#===== START OF FILE primary/rag.py =====
#Library of functions and execution code to do RAG tasks

import os
from datetime import datetime
from pinecone import Pinecone
from termcolor import colored

from primary.vectordb import generate_embedding
from primary.llm import simple_openai_chat_completion_request
from primary.rag_prompts_routes import *


#---API KEYS AND SECRETS---
from dotenv import load_dotenv
load_dotenv(override=True)  # Load environment variables from .env file
OPENAI_API_KEY = os.environ["OPENAI_API_KEY_LOCAL"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY_LOCAL"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
 

#---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

DEFAULT_LLM_MODEL = 'gpt-4o'

    """ 
### VRAG (489 tokens)
def print_vrag_display_text(json_object, show_prompt=False):
    """
    pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

    vectorized_query = generate_embedding(query)
    index = pinecone_client.Index(vector_index_name)
    
    # Prepare query parameters
    query_params = {
        "namespace": "",
        "vector": vectorized_query,
        "top_k": num_chunks,
        "include_values": False
    }
    
    # Add date range filter if provided
    if date_range and len(date_range) == 2:
        # Convert ISO date strings to Unix timestamps
        start_date_timestamp_unix = int(datetime.fromisoformat(date_range[0]).timestamp())
        end_date_timestamp_unix = int(datetime.fromisoformat(date_range[1]).timestamp())
        
        query_params["filter"] = {
            "DATE": {
                "$gte": start_date_timestamp_unix,
                "$lte": end_date_timestamp_unix
            }
        }
    
    retrieved_qchunks = index.query(**query_params)
    
    # Extract the IDs from the retrieved question chunks
    retrieved_ids_scores = {vector['id']: vector['score'] for vector in retrieved_qchunks['matches']}
    
    # Fetch the question chunks using the IDs
    ids = list(retrieved_ids_scores.keys())
    fetched_chunks = index.fetch(ids=ids, namespace="")

    return fetched_chunks, retrieved_ids_scores


    """
def vrag_llm_call(user_question, vector_index_name, num_chunks, vrag_preamble=VRAG_PREAMBLE_V1, llm_model=DEFAULT_LLM_MODEL, user_id='default', vrag_version="1.0"):
    """
    user_question = json_object['content']['user_question']
    ai_answer = json_object['content']['ai_answer']
    
    display_text = f"USER QUESTION: {user_question}\n\n"
    
    if show_prompt:
        llm_prompt = json_object['content']['llm_prompt']
        display_text += f"LLM PROMPT:\n{llm_prompt}\n\n"
    else:
        chunk_texts = json_object['content']['chunk_texts']
        display_text += f"RETRIEVED CHUNKS:\n{chunk_texts}\n\n"
    
    display_text += f"AI ANSWER: {ai_answer}"
    
    print(display_text)
    
    """
### QRAG (2,387 tokens)
def sort_chunks_by_stars(fetched_qa_chunks, retrieved_ids_scores, num_chunks):
    """
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(user_question, vector_index_name, num_chunks)
    chunk_texts = ''
    for chunk_id, chunk_data in fetched_chunks['vectors'].items():
        text = chunk_data['metadata'].get('text', '')
        if text:
            chunk_texts += text + '\n'
    chunk_texts = chunk_texts.rstrip('\n')  # Remove trailing newline if present

    llm_prompt = vrag_preamble + "\n" + chunk_texts + "\nUSER QUESTION: " + user_question + "\n\nAI ANSWER: "
    llm_answer = simple_openai_chat_completion_request(llm_prompt, model=llm_model)
    
    return {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "vector_index_name": vector_index_name,
            "vrag_version": vrag_version,
            "llm_model": llm_model,
            "vrag_info": {
                "vrag_preamble": vrag_preamble,
                "num_chunks": len(fetched_chunks['vectors'])
            }
        },
        "content": {
            "user_question": user_question,
            "chunk_texts": chunk_texts,
            "llm_prompt": llm_prompt,
            "ai_answer": llm_answer
        }
    }
 

    """
def sort_chunks_by_sim(fetched_qa_chunks, retrieved_ids_scores, num_chunks):
    """
    # Extract chunks and their metadata
    chunks = []
    for chunk_id, chunk_data in fetched_qa_chunks['vectors'].items():
        metadata = chunk_data['metadata']
        metadata['id'] = chunk_id
        metadata['sim_score'] = retrieved_ids_scores.get(chunk_id, 0)
        # Convert STARS to integer, set to 0 if blank
        metadata['STARS'] = int(metadata.get('STARS', 0)) if metadata.get('STARS') else 0
        chunks.append(metadata)

    # Sort chunks by star rating (descending) and then by similarity score (descending)
    sorted_chunks = sorted(chunks, key=lambda x: (-x['STARS'], -x['sim_score']))

    # Return the top `num_chunks` chunks
    return sorted_chunks[:num_chunks]

    """
def parse_chunks(chunks, simscores):
    """
    # Extract chunks and their metadata
    chunks = []
    for chunk_id, chunk_data in fetched_qa_chunks['vectors'].items():
        metadata = chunk_data['metadata']
        metadata['id'] = chunk_id
        metadata['sim_score'] = retrieved_ids_scores.get(chunk_id, 0)
        # Convert STARS to integer, set to 0 if blank
        metadata['STARS'] = int(metadata.get('STARS', 0)) if metadata.get('STARS') else 0
        chunks.append(metadata)

    # Sort chunks by similarity score in descending order
    sorted_chunks = sorted(chunks, key=lambda x: x['sim_score'], reverse=True)

    # Return the top `num_chunks` chunks
    return sorted_chunks[:num_chunks]

    """ 
def qrag_routing_call(user_question, vector_index_name, num_chunks, routes_dict, date_range=None, routes_bounds=[0.3, 0.9], 
    """
    parsed_chunks = []
    for chunk in chunks:
        chunk_id = chunk['id']
        sim_score = simscores.get(chunk_id, 0)

        # Map CLARIFIED_QUESTION/ANSWER fields to QUESTION/ANSWER fields if present
        question = (
            chunk.get('CLARIFIED QUESTION') or  # Try CLARIFIED_QUESTION first
            chunk.get('QUESTION')  # Fall back to standard fields
        )
        if question is None:
            raise ValueError("Missing required question field in chunk")

        answer = (
            chunk.get('CLARIFIED ANSWER') or  # Try CLARIFIED_ANSWER first
            chunk.get('ANSWER')  # Fall back to standard fields
        )
        if answer is None:
            raise ValueError("Missing required answer field in chunk")

        parsed_chunk = {
            "question": question,
            "answer": answer,
            "verbatim_question": chunk.get("VERBATIM QUESTION", ""),
            "verbatim_answer": chunk.get("VERBATIM ANSWER", ""),
            "speaker_question": chunk.get("SPEAKER QUESTION", ""),
            "speaker_answer": chunk.get("SPEAKER ANSWER", ""),
            "topics": chunk.get("TOPICS", ""),
            'source': str(chunk.get('SOURCE', 'No source')),
            "timestamp": chunk.get("TIMESTAMP", "No timestamp"),
            "stars": int(chunk.get("STARS", 0)),
            "sim": float(sim_score),
            "display": (
                f"ANSWER STARS: {int(chunk.get('STARS', 0))}\n"
                f"QUESTION SIMILARITY SCORE: {round(sim_score * 100)}%"
            ),
        }
        parsed_chunks.append(parsed_chunk)
    return parsed_chunks

                      llm_model=DEFAULT_LLM_MODEL, user_id='default', user_context=None, qrag_version="1.0"):
    """
def qrag_llm_call(json_object):
    """
    routes_flow_name = "3 routes, separate route prompts"

    # Retrieve chunks from Pinecone
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(user_question, vector_index_name, num_chunks, date_range)

    # Select and sort chunks by similarity
    selected_chunks = sort_chunks_by_sim(fetched_chunks, retrieved_ids_scores, num_chunks)

    # Parse the selected chunks
    parsed_chunks = parse_chunks(selected_chunks, retrieved_ids_scores)

    # Retrieve the item template from routes_dict
    quoted_qa_item_template = routes_dict.get('quoted_qa_item_template', "")

    # Construct the quoted_qa by iterating over parsed chunks
    # This duplicated text is provided for ease of use by downstream web javascript code
    quoted_qa_list = []
    for chunk in parsed_chunks:
        # Map the fields to match the template expectations
        template_fields = {
            "question": chunk["question"],
            "answer": chunk["answer"],
            "verbatim_question": chunk.get("verbatim_question", ""),
            "verbatim_answer": chunk.get("verbatim_answer", ""),
            "speaker_question": chunk.get("speaker_question", ""),
            "speaker_answer": chunk.get("speaker_answer", ""),
            "topics": chunk.get("topics", ""),
            "source": chunk["source"],
            "timestamp": chunk["timestamp"],
            "display": chunk["display"]
        }
        chunk_formatted = routes_dict['quoted_qa_item_template'].format(**template_fields)
        quoted_qa_list.append(chunk_formatted)

    quoted_qa_formatted = ''.join(quoted_qa_list)
    quoted_qa = routes_dict['quoted_qa_template'].format(quoted_qa_formatted=quoted_qa_formatted)

    # Determine max similarity and stars
    max_sim = max(chunk['sim'] for chunk in parsed_chunks) if parsed_chunks else 0
    max_stars = max(chunk['stars'] for chunk in parsed_chunks) if parsed_chunks else 0

    lower_sim_bound, upper_sim_bound = routes_bounds

    if max_sim >= upper_sim_bound:
        route_preamble = routes_dict['route_preamble_good_match']
    elif max_sim <= lower_sim_bound:
        route_preamble = routes_dict['route_preamble_no_match']
        quoted_qa = ""
    else:
        route_preamble = routes_dict['route_preamble_partial_match']

    # Prepare chunk metadata for the response
    chunks_metadata = []
    for chunk in parsed_chunks:
        chunks_metadata.append({
            "question": chunk['question'],
            "source": chunk['source'],
            "timestamp": chunk['timestamp'],
            "answer": chunk['answer'],
            "stars": chunk['stars'],
            "sim": "{:.3f}".format(chunk['sim'])
        })

    response = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            # Add user_context if provided
            **({"user_context": user_context} if user_context else {}),
            "vector_index_name": vector_index_name,
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
            "quoted_qa": quoted_qa,
            "ai_answer": "WAITING FOR AI ANSWER...",
            "chunks": {
                "max_sim": "{:.3f}".format(max_sim),
                "max_stars": max_stars,
                "chunks": chunks_metadata
            }
        }
    }

    # Add date range if provided
    if date_range is not None:
        response["metadata"]["date_range"] = date_range

    return response

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
    json_object['content']['llm_prompt'] = llm_prompt  # Optionally include the prompt

    return json_object

    """ 
def qrag_2step(user_question, routes_dict, vector_index_name, num_chunks=2, verbose=True):
    """
    user_question = json_object['content']['user_question']
    route_preamble = json_object['content']['route_preamble']
    quoted_qa = json_object['content']['quoted_qa']
    ai_answer = json_object['content']['ai_answer']
    display_text = 'USER QUESTION: ' + user_question + '\n\n' + 'ROUTE PREAMBLE: ' + route_preamble + '\n\n' + quoted_qa + 'AI ANSWER: ' + ai_answer
    print(display_text)

    """ 

## primary/conversion.py (4,120 tokens)
### LLAMAINDEX (643 tokens)
def convert_llamaparse_pdf_to_md(file_path):
def mrun_convert_llamaparse_pdf_to_md():
def convert_llamaindex_gdocs_to_md(gdoc_id_list):
    """
    from primary.fileops import pretty_print_json_object

    # Create JSON object with routing information
    routing_json_obj = qrag_routing_call(user_question, vector_index_name, num_chunks, routes_dict)

    if verbose:
        pretty_print_json_object(routing_json_obj, print_values=True)
    
    # Print the display text for the QRAG process
    print_qrag_display_text(routing_json_obj)

    # Generate and print the AI answer
    ai_answer = qrag_llm_call(routing_json_obj)['content']['ai_answer']
    print(colored(ai_answer, 'red'))

#===== END OF FILE primary/rag.py =====



#===== START OF FILE primary/conversion.py =====
#Library of functions and execution code to do conversion tasks    

import os
import re
import logging
import pypandoc
from llama_parse import LlamaParse  # pip install llama-index llama-parse
from llama_index.core import SummaryIndex
from llama_index.readers.google import GoogleDocsReader  # pip install llama-index llama-index-readers-google
from markitdown import MarkItDown
from openai import OpenAI
from nltk.corpus import words
from collections import defaultdict

#from IPython.display import Markdown, display

from primary.fileops import *

#---API KEYS AND SECRETS---
from dotenv import load_dotenv
load_dotenv(override=True)  # Load environment variables from .env file
LLAMA_CLOUD_API_KEY = os.environ["LLAMA_CLOUD_API_KEY"]
#INSERT in chalice/config.json "LLAMA_CLOUD_API_KEY": "LLAMA_CLOUD_API_KEY"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY_ORIG"]

#---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

    suffix_append = "_llamaparse"
    documents = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown",verbose=True).load_data(file_path)
    #print(documents[0].text[0:1000])
    md_file_path = file_path.rsplit('.', 1)[0] + suffix_append + '.md'  # Replace the file extension with .md
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(documents[0].text)
    print("Completed LlamaParse pdf to md conversion and appended suffix: " + suffix_append + " on input file_path: " + file_path)
    return md_file_path
    pass
#if __name__ == "__main__":
    file_path = 'data/misc_books/The Sovereign Child.pdf'
    print(convert_llamaparse_pdf_to_md(file_path))

#TODO WIP - not working because needs different gcloud auth than service account
    """
def mtest_convert_llamaindex_gdocs_to_md(gdoc_id_list):
### PANDOC (397 tokens)
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
    pass
#if __name__ == "__main__": 
    cur_gdoc_id_list = ['19yTV3UUkOQrfbqOPcL5hhBw9eJyc_5ra5Uz_tKQcs24']
    convert_llamaindex_gdocs_to_md(cur_gdoc_id_list)

''' To confirm installation, run: pandoc --version
Should see:
pandoc 3.2
Features: +server +lua
Scripting engine: Lua 5.4
'''

    """
def mtest_convert_file_to_md_pandoc():
### MEGAPARSE (313 tokens)
def convert_megaparse_pdf_to_md(file_path, use_llama_parse=False, use_vision=False):
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
    pass
#if __name__ == "__main__": 
    #cur_file_path = 'tests/test_manual_files/file_conversion/2021-05-18_Instructions for Use - FloodLAMP QuickColor COVID-19 Test v1.1.docx'
    cur_file_path = 'data/floodlamp_fda/subs/2021-05-18_Pre-EUA Sub - FloodLAMP Proposed Pooling and Asymptomatic Screening Study.docx'
    print(convert_file_to_md_pandoc(cur_file_path))

    """
def mrun_convert_megaparse_pdf_to_md():
### MS MARKITDOWN (403 tokens)
def convert_file_to_md_msmid(file_path, new_suffix="_msmid"):
    """
    from megaparse import MegaParse
    
    if use_llama_parse:  # not working - see several github issues about this
        suffix_append = "_megaparse-lp"
        # from megaparse.parser.llama_parse import LlamaParser
        # parser = LlamaParser(api_key=os.getenv("LLAMA_CLOUD_API_KEY"))
    elif use_vision:
        suffix_append = "_megaparse-v" 
        from megaparse.parser.megaparse_vision import MegaParseVision
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4-vision-preview", api_key=OPENAI_API_KEY)
        parser = MegaParseVision(model=model)
    else:
        suffix_append = "_megaparse-u"
        from megaparse.parser.unstructured_parser import UnstructuredParser
        parser = UnstructuredParser()
    
    # Initialize MegaParse with selected parser
    megaparse = MegaParse(parser)
    
    # Process the document
    response = megaparse.load(file_path)
    
    # Create output path
    md_file_path = file_path.rsplit('.', 1)[0] + suffix_append + '.md'
    
    # Save to markdown
    megaparse.save(md_file_path)
    
    parser_type = "with LlamaParse" if use_llama_parse else "without LlamaParse"
    print(f"Completed MegaParse with {parser_type} for pdf to md conversion.")
    return md_file_path
    pass
#if __name__ == "__main__":
    file_path = 'data/misc_books/The Sovereign Child.pdf'
    print(convert_megaparse_pdf_to_md(file_path))

    """
def mrun_convert_file_to_md_msmid():
def get_image_description_msmid(image_file_path, verbose=True):
### TEXT (1,164 tokens)
def initialize_nltk(silent=True):
    """
    md = MarkItDown()
    result = md.convert(file_path)
    
    # Create output path with new suffix
    md_file_path = file_path.rsplit('.', 1)[0] + new_suffix + '.md'
    
    # Save the markdown content to file
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(result.text_content)
    
    print(f"Completed Microsoft MarkItDown conversion and appended suffix: {new_suffix} on input file_path: {file_path}")
    return md_file_path
    pass
#if __name__ == "__main__":
    file_path = 'data/misc_books/The Sovereign Child.pdf'
    print(convert_file_to_md_msmid(file_path))

#TODO not tested - from readme at https://github.com/microsoft/markitdown/blob/main/README.md
    # To use Large Language Models for image descriptions, provide llm_client and llm_model:
    client = OpenAI()
    md = MarkItDown(llm_client=client, llm_model="gpt-4o")
    result = md.convert(image_file_path)
    description = result.text_content   
    verbose_print(verbose, description)
    return description

_word_set = None  # Declare the global variable
    """
def mrun_initialize_nltk():
def load_custom_dictionary(file_path):
    """
    import nltk.data
    global _word_set
    
    resources = [
        ('corpora/words', 'words'),
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng'),
        ('corpora/stopwords', 'stopwords'),
        ('chunkers/maxent_ne_chunker_tab', 'maxent_ne_chunker_tab')
    ]
    
    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
            print(f"Resource '{resource_name}' is already available.")
        except LookupError:
            print(f"Resource '{resource_name}' not found. Downloading...")
            if silent:
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore")
                    nltk.download(resource_name, quiet=True)
            else:
                nltk.download(resource_name)
            print(f"Resource '{resource_name}' downloaded successfully.")
    
    # Initialize word set after ensuring resources are available
    _word_set = set(w.lower() for w in words.words())
    _word_set.update({
        'curiosity', 'priorities',
        # Add more as needed
    })
    pass
#if __name__ == "__main__":
    initialize_nltk(silent=False)
#TODO 7-18 RT - consider whether this is OK to be in function, think it was not previously and getting Problems
    """ Load a custom dictionary from a file. """
def lines_alphabetize_and_remove_duplicates(file_path):
    """
    Alphabetizes and removes duplicates from a list.
    """
def mrun_lines_alphabetize_and_remove_duplicates():
def lines_compare_files(file_path_1, file_path_2, print_same=False, silent=False):
    """
    Compares lines between two files and returns lists of differences and matches.
    
    :param file_path_1: Path to first file
    :param file_path_2: Path to second file
    :param print_same: Boolean to control whether to print lines that appear in both files
    :return: Tuple of (lines only in file 1, lines only in file 2, lines in both files)
    """
def mrun_lines_compare_files():
def normalize_text(text):
def format_divider(title, total_length=69, start_pos=None, char='=', md_level=3, start_newline=False, end_newline=True):
    """
    Creates a formatted header with equal signs and optional markdown heading level.
    
    :param total_length: Total desired length of the header line
    :param title: Title text to display in the middle
    :param start_pos: Position where title should start (if None, centers the title)
    :param md_level: Number of markdown hashtags to prepend (None for no markdown)
    :param start_newline: Whether to start with a newline
    :param end_newline: Whether to end with a newline
    :param char: Character to use for the header line (default '=')
    :return: Formatted header string
    """
def get_context(text, position, surrounding_chars=None, surrounding_words=None, complete_words=True):
    """
    Extract surrounding context from text around a specific position.

    :param text: str, the full text to extract context from
    :param position: int, the center position to get context around
    :param surrounding_chars: int or None, number of characters to include on each side
    :param surrounding_words: int or None, number of words to include on each side
    :param complete_words: bool, whether to expand to complete words
    :return context: str, the extracted context snippet
    """
def remove_extraneous_spaces_in_words(text, verbose=False):
    """
    Removes extraneous spaces that split valid words in text.
    Uses NLTK's word list with custom additions.
    
    :param text: str, text to process for split words
    :param verbose: bool, whether to print debug info
    :return: str, processed text with split words rejoined
    """
def mtest_remove_extraneous_spaces_in_words():
### MARKDOWN (290 tokens)
def convert_csv_to_md_table(csv_content):
    """
    Convert CSV content to a markdown table.
    """
def analyze_quotes_characters(md_file_path):
    """
    Analyzes a markdown file for different types of quotes and apostrophes.
    Displays a formatted table of quote types, their Unicode values, and counts.
    """
def mrun_analyze_quotes_characters():
def convert_markdown_to_md_mod_text(md_file_path):
    """
    Converts a markdown file to a modified text file with specific replacements.
    Changes the suffix to 'md-mod' and extension to '.txt'.
    Creates a copy of the input file before making modifications.
    
    :param md_file_path: string, path to the markdown file to be converted
    :return: string, path to the modified text file
    """
def mrun_convert_markdown_to_md_mod_text():
def combine_files_into_md(file_paths, target_file_path, max_file_size_mb=10):
    """
    Combine multiple files into a single markdown file.
    
    :param file_paths: List of file paths to combine (relative to repo root)
    :param target_file_path: Path for the output markdown file (relative to repo root)
    :param max_file_size_mb: Maximum allowed file size in MB (default: 10)
    :return: The relative path of the combined markdown file
    """
def mrun_combine_files_into_md():
### HTML (593 tokens)
def wrap_qa_blocks_in_details(html_file_path, question_field="CLARIFIED QUESTION", answer_field="CLARIFIED ANSWER"):
    """
    Wraps QA blocks in nested details tags for collapsible viewing.
    
    :param html_file_path: string, path to the HTML file to modify
    :param question_field: string, field name for questions (default: CLARIFIED QUESTION)
    :param answer_field: string, field name for answers (default: CLARIFIED ANSWER)
    :return: None
    """
    def wrap_qa_block(match):
def clean_summaries_in_html_file(html_file_path):
    """
    Removes href links from all summary tags in an HTML file while preserving the link text.
    Processes all levels of nested summaries.
    
    :param html_file_path: string, path to the HTML file to clean
    :return: None
    """
    def clean_summary_content(match):
def add_additional_html_from_template(html_file_path, template_file_path):
    """
    Adds non-empty HTML elements from a template file to their corresponding parent locations in the target HTML file.
    
    :param html_file_path: string, path to the HTML file to modify
    :param template_file_path: string, path to the template file to add
    :return: None
    """
def h_tune_html_file(html_file_path, tune_string, h_level, insert=True, remove_suffixext=True):
    """
    Modifies heading text in an HTML file at specified heading level.
    
    :param html_file_path: string, path to the HTML file to modify
    :param tune_string: string, text to insert or replace with
    :param h_level: int, heading level to modify (1-6)
    :param insert: bool, if True inserts tune_string after first underscore, if False replaces entire heading
    :param remove_suffixext: bool, if True removes text after and including last underscore
    :return: None
    """
    def modify_heading(match):
def convert_markdown_to_html(md_file_path, heading, collapse_h=4, css_file_path=None, cap_first=True):
    """
    Converts a markdown file to an html file using pypandoc and optionally replaces style with external CSS link.
    
    :param md_file_path: string, path to the markdown file to convert
    :param heading: string, heading to use for the document
    :param collapse_h: int, heading level to wrap with details/summary elements (default: 4)
    :param css_file_path: string or None, path to CSS file to link (if None - keeps default styles, if empty string - removes styles)
    :return: string, path to the output HTML file
    """
        def wrap_section(match):
        def capitalize_heading(match):
def mrun_convert_markdown_to_html():
### OCR IMAGES (311 tokens)
def do_ocr_on_image(image_path, mode='color', binary_threshold=None):
    """
    Performs OCR on an image file using specified processing parameters.
    
    :param image_path: string path to the image file (JPEG, PNG, etc.)
    :param mode: string, 'binary', 'grayscale', or 'color' processing mode
    :param binary_threshold: int, binary threshold value (used if mode is 'binary')
    :return: string of the extracted text
    """
def vary_ocr_on_image(image_path):
    """
    Performs OCR on an image using different modes and binary thresholds,
    outputting results to a markdown file.
    
    :param image_path: string path to the image file
    :return: string path to the output markdown file
    """
def mtest_do_ocr_on_image():
def create_md_ocr_on_image_folder(folder_path, mode='color', binary_threshold=None):
    """
    Performs OCR on all supported images in a folder and creates a single markdown file
    with the results. Each image's text will be under its own heading.
    
    :param folder_path: string path to the folder containing images
    :param mode: string, 'binary', 'grayscale', or 'color' processing mode
    :param binary_threshold: int, binary threshold value (used if mode is 'binary')
    :return: string path to the output markdown file
    """
def mtest_create_md_ocr_on_image_folder():

## primary/structured.py (1,791 tokens)
### BLOCK PROCESSING (687 tokens)
def get_blocks_from_file(qa_file_path, heading="### qa"):
    """
    Extracts and validates blocks of text from a file.

    :param qa_file_path: string of the path to the file to be read.
    :param verbose: boolean, if True, prints verbose messages. Default is False.
    :return: list of valid blocks from the file.
        """
def delete_fields_from_text(text, delete_fields):
    """
    Removes specified fields from a text block, including multi-line field values.
    Field boundary rules:
    1. Two consecutive newlines
    2. A newline followed by an all-caps field name and colon (e.g. 'STARS:')
    
    :param text: string of the text to process
    :param delete_fields: list of field names to delete
    :return: string of text with specified fields removed
    """
def mrun_delete_fields_from_text():
def get_field_value(block, field):
    """
    Extracts the content of a specified field from a block of text, including multi-line values.
    Field boundary rules:
    1. Two consecutive newlines
    2. A newline followed by a field name and colon where the field name:
       - is in all caps
       - may contain spaces, underscores, or dashes
       - will be treated as a boundary even if the field is empty
       (Updated empty field handling - RT 2024-03-19)
    
    :param block: string of the block of text to be processed.
    :param field: string of the field to be extracted from the block.
    :return: the content of the field in its appropriate data type, or None if the field is not found.
    """
def mrun_get_field_value():
def get_all_fields_dict(block):
    """
    Extracts all fields and their contents from a block of text.

    :param block: string of the block of text to be processed.
    :return: dictionary of fields and their contents in their appropriate data types.
    """
def mrun_get_all_fields_dict():
def count_blocks(file_path, heading="## content"):  # quick way is to use find on a field
    """
    Counts the number of blocks in a specific section of a file, skipping comment lines.

    :param file_path: string of the path to the file to be processed.
    :param heading: string of the markdown heading to search for. Default is "## content".
    :return: integer representing the total number of blocks found.
    """
def mtest_count_blocks():
def propagate_fields_by_subheading(file_path, full_fields, required_fields, delete_fields=[], heading="### qa", keep_only_heading=True):
    """
    Propagates fields defined under markdown subheadings to all blocks within those subheadings.


    :param file_path: Path to the input QA markdown file.
    :param full_fields: List of all possible fields for reference and ordering.
    :param required_fields: List of fields that must be present in every QA block.
    :param delete_fields: List of fields to delete from every QA block.
    :param heading: The markdown heading to process. Default is "### qa".
    :return: The relative file path of the new file with propagated fields.
    """
### BLOCK VALIDATION (594 tokens)
def validate_stars(stars_str):
def validate_topics(topics_str):
def validate_blocks(blocks_list, required_fields, custom_validators=None, show_only_first_invalid=True):
    """
    Validates the structure and content of QA blocks against required fields.

    :param blocks_list: List of QA blocks where each block is a string of text representing a qa entry.
    :param required_fields: List of required field names.
    :param custom_validators: Dictionary of field names and their corresponding validation functions.
    :param show_only_first_invalid: If True, only shows the first invalid block. If False, shows all invalid blocks.
    :return: The number of valid blocks if all are valid, or the negative count of invalid blocks.
    """
def validate_blocks_in_file(file_path, required_fields, custom_validators, verbose=False):
    """
    Function to validate QA blocks in a file and return True if all blocks are valid

    :param file_path: string of the path to the file to be validated
    :param required_fields: List of required field names.
    :param custom_validators: Dictionary of field names and their corresponding validation functions.
    :param verbose: boolean to control verbose output
    :return: boolean indicating whether all blocks in the file are valid
    """
def validate_blocks_in_folders(folder_paths, required_fields, custom_validators, suffixpat_include="_qafixed"):
    """
    Validates QA blocks in all files within specified folders, printing the number of valid files in each folder
    and statistics about required and optional fields.

    :param folder_paths: list of strings of folder paths to search for files.
    :param required_fields: List of required field names.
    :param custom_validators: Dictionary of field names and their corresponding validation functions.
    :param suffixpat_include: string of the suffix to include in file search. Default is "_qafixed".
    :return: string of the path of the first file with invalid QA blocks if any; None if all files are valid.
    """
def validate_qa_blocks_townhall_OLD(blocks_list):
    """
    Validates the structure and content of QA blocks against required and optional fields.

    :param blocks_list: list of qa blocks where each block is a string of text representing a qa entry.
    :return: the number of valid blocks if all are valid, or the negative count of invalid blocks.
    """
def validate_iso_dates_in_filename(folder_paths, suffixpat_include):
    """
    Validates that filenames in specified folders start with valid ISO dates (YYYY-MM-DD).

    :param folder_paths: list of strings of folder paths to search for files.
    :param suffixpat_include: string of the suffix to include in file search. Default is "_qafixed".
    :return: boolean indicating whether all files have valid ISO dates (True) or not (False).
    """
### TOPICS (504 tokens)
def extract_topic_counts_triples(qa_file_path, verbose=False):
    """
    Extracts topics from QA blocks in a file and counts their occurrences. 

    :param qa_file_path: string of the path to the QA file.
    :param verbose: boolean, if True, prints additional information during execution. Default is False.
    :return: string of CSV lines with each line in the format "topic, file_stem, count".
    """
def create_topics_matrix(folder_paths, target_file_path="topics_matrix.csv", suffixpat_include="_qafixed"):
    """
    Collects topics from files in specified folders and creates a CSV matrix file at the target file path.

    :param folder_paths: list of strings of folder paths to search for files.
    :param target_file_path: string of the path where the resulting CSV file will be created. If no folder is provided in the path, the parent folder of the first folder in the folder_paths list will be used.
    :param suffix_include: string of the suffix to include in file search. Default is "_qafixed".
    :return: string of the path to the created csv file.
    """
def mtest_create_topics_matrix():
def change_topic_in_file(file_path, find_topic, replace_topic):
    """
    Replaces a specified topic with another in a single file.

    :param file_path: string of the file path to process.
    :param find_topic: string of the topic to find.
    :param replace_topic: string of the topic to use as a replacement.
    :return: tuple of (int, int) representing (replacements_in_file, total_replacements)
    """
def change_topic_in_folders(folder_paths, find_topic, replace_topic, suffixpat_include="_qafixed"):
    """
    Replaces a specified topic with another across files in given folders.

    :param folder_paths: list of strings of folder paths to search for files.
    :param find_topic: string of the topic to find.
    :param replace_topic: string of the topic to use as a replacement.
    :param suffix_include: string of the suffix to include in file search.
    :return: None.
    """
    def process_file(file_path):
def review_singlet_topic_SONNET(folder_paths, matrix_csv_file_path, starting_letter="a"):
def review_singlet_topic(folder_paths, matrix_csv_file_path, starting_letter="a"):

## primary/corpuses.py (1,269 tokens)
### DEUTSCH CORPUS (56 tokens)
def validate_corpus_deutsch():
def mrun_deutsch_corpus():
def mrun_deutsch_download_new_s3_files():
def mrun_deutsch_index_exchanges_and_pii():
def mtest_qrag_2step_deutsch():
### PV EVAC CORPUS (45 tokens)
def mrun_propagate_fields_pv_evac():
def validate_corpus_pv_evac():
def mrun_pv_epc_corpus():
def mtest_qrag_2step_pv_evac():
### FDA TOWNHALLS CORPUS (651 tokens)
def remove_lines_fda_townhall(text):
    """ 
    Remove lines from a string of FDA townhall transcript text that match certain patterns.

    :param text: string of the transcript text to be cleaned.
    :return: string of the cleaned transcript text.
    """
def clean_fda_townhall_file(file_path):
    """
    Cleans the FDA townhall file by removing unnecessary lines and fixing speaker text.

    :param file_path: string of the path to the file to be cleaned.
    :param suffix_new: string of the suffix to be added to the cleaned file. Default is '_cleaned'.
    :return: The cleaned text with the heading set.
    """
def mtest_clean_fda_townhalls_file():
def clean_fda_townhalls_folder(source_folder, destination_folder):
    """
    Cleans the files in the source folder and moves the cleaned files to the destination folder.

    :param source_folder: string of the path to the source folder containing the files to be cleaned.
    :param destination_folder: string of the path to the destination folder where the cleaned files will be moved.
    :return: None
    """
def mtest_clean_fda_townhalls_folder():
def mrun_fda_townhalls_create_speaker_matrix():
def mrun_find_and_replace_on_fda_townhalls():
def mrun_fda_townhalls_corpus():
def csv_of_num_characters_transcript_and_qa(folder_path, transcript_suffix='_fixnames', qa_suffix='_qa-qonly'):
    """
    Creates a CSV file with character counts for transcript and QA files.

    :param folder_path: string, path to folder containing transcript and QA files
    :param transcript_suffix: string, suffix for transcript files
    :param qa_suffix: string, suffix for QA files
    :return csv_path: string, path to the created CSV file
    """
def mrun_csv_of_num_characters_transcript_and_qa():
def mrun_section_titles():
def mrun_convert_fda_townhalls_transcript_to_html():
def mrun_convert_fda_townhalls_qa_to_html():
def mrun_create_html_files_for_fda_townhalls():
def upload_s3_and_webflow_fda_townhalls(s3_upload=True, s3_prompt_overwrite=True, webflow_upload=True):
    """
    Uploads FDA townhall files to S3 and creates corresponding Webflow CMS items.

    :param s3_upload: bool, whether to upload files to S3
    :param s3_prompt_overwrite: bool, whether to prompt before overwriting S3 files
    :param webflow_upload: bool, whether to create Webflow CMS items
    :return: None
    """
def mrun_upload_s3_and_webflow_fda_townhalls():
def mrun_flex_fda_townhalls_folder():
def mtest_pinecone_retrieve_fda_townhalls():
def mtest_qrag_2step_fda_townhalls():
def mtest_s3_upload_fda_townhalls():
### CORPUS ORGANIZATION (510 tokens)
def create_csv_of_files_by_suffix(folder_path, suffixpat_include=None, suffixpat_exclude=None, include_subfolders=False):
    """
    Creates a CSV file organizing files by their base names and suffixes.
    The CSV will have file base names as rows and suffixes as columns.
    Cell values will be the relative file paths if the file exists, None otherwise.

    :param folder_path: string of the path to the folder from which to retrieve files.
    :param suffixpat_include: string of the suffix pattern that included files must have.
    :param suffixpat_exclude: string of the suffix pattern that files must not have to be included.
    :param include_subfolders: boolean indicating whether to include files from subfolders.
    :return: string of the path to the created CSV file.
    """
def mrun_create_csv_of_files_by_suffix():
def create_csv_of_files_by_suffix_folders_NOCALL(folders, suffixpat_include=None, suffixpat_exclude=None, include_subfolders=False):
    """
    Creates a CSV file organizing files from multiple folders by their base names and suffixes.
    Handles multiple instances of the same file/suffix combination by creating MULTI entries.

    :param folders: list of strings of folder paths to process
    :param suffixpat_include: string of the suffix pattern that included files must have
    :param suffixpat_exclude: string of the suffix pattern that files must not have
    :param include_subfolders: boolean indicating whether to include files from subfolders
    :return: string of the path to the created CSV file
    """
def create_csv_of_files_by_suffix_folders(folders, suffixpat_include=None, suffixpat_exclude=None, include_subfolders=False):
    """
    Creates a CSV file organizing files from multiple folders by their base names and suffixes.
    Makes initial call to create_csv_of_files_by_suffix for the first folder, then appends data
    from additional folders. Handles multiple instances of same file/suffix with MULTI entries.

    :param folders: list of strings of folder paths to process
    :param suffixpat_include: string of the suffix pattern that included files must have
    :param suffixpat_exclude: string of the suffix pattern that files must not have
    :param include_subfolders: boolean indicating whether to include files from subfolders
    :return: string of the path to the created CSV file
    """
def mrun_create_csv_of_files_by_suffix_folders():

## primary/aws.py (3,135 tokens)
### HMAC HASH (84 tokens)
def generate_hmac_hash(input_text, secret_key):
    """
    Generate a HMAC hash for the given input text using the provided secret key.

    :param input_text: The text to be hashed
    :param secret_key: The secret key used for hashing
    :return: The HMAC hash as a hexadecimal string of 64 characters
    """
def mtest_generate_hmac_hash():
### AWS S3 (1,221 tokens)
def upload_file_to_s3(file_path, bucket='fofpublic', object_name=None, s3_path=None, prompt_overwrite=False):
    """
    Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket: Name of the S3 bucket, default is 'fofpublic', others: 'fofsecure', 'deutsch-audio'
    :param object_name: S3 object name. If not specified, the file name is used
    :param s3_path: S3 folder path where the file will be stored, e.g. 'podcasts/'
    :param prompt_overwrite: If True, prompts for confirmation before overwriting existing files
    :return: The object name of the file in S3, or None if upload was cancelled or failed
    """
def rename_s3_object(bucket, old_key, new_key, s3_path=None):
    """
    Rename an object in an S3 bucket by copying it to a new key and deleting the old key.

    :param bucket: Name of the S3 bucket
    :param old_key: The current key (path) of the object in the S3 bucket
    :param new_key: The new key (path) for the object in the S3 bucket
    :param s3_path: Optional S3 folder path to prepend to the keys
    :return: None
    """
def get_s3_object(bucket, key, s3_path, parse_json=True):
    """
    Retrieve an object from an S3 bucket.

    :param bucket: Name of the S3 bucket
    :param key: The key (path) of the object in the S3 bucket
    :param s3_path: Optional S3 folder path to prepend to the key
    :param parse_json: Whether to parse the object content as JSON (default: True)
    :return: The object content (parsed as JSON if parse_json is True) if found, otherwise None
    """
def mtest_get_s3_object():
def list_s3_files(bucket, s3_path, file_extension='.json'):
    """
    List all files with a specific extension in the specified S3 bucket and path.

    :param bucket: Name of the S3 bucket.
    :param s3_path: The folder path (path) in the S3 bucket.
    :param file_extension: The file extension to filter by (default: '.json').
    :return: List of file names (without path) with the specified extension, sorted lexicographically.
    """
def mtest_list_s3_files():
def remove_from_file_list(folder_path, base_file_list):
    """
    Removes files found in the specified folder (including subfolders) from the given base file list.

    :param folder_path: String path to the folder to search for files.
    :param base_file_list: List of base file names (without paths) to filter.
    :return: A new list with matching files removed.
    """
def mtest_remove_from_file_list():
def download_s3_files_new(bucket, s3_path, local_folder):
    """
    Download new files from S3 to a local folder.

    :param bucket: Name of the S3 bucket.
    :param s3_path: S3 path to the files.
    :param local_folder: Local folder where both files to exclude and files to download will be saved.
    :return: None
    """
def mtest_download_s3_files_new():
def download_s3_files_date_range(bucket, s3_path, local_folder, start_date, end_date, timezone='America/Los_Angeles'):
    """
    Download files from S3 to a local folder that were last modified within a specified date range.

    :param bucket: string, name of the S3 bucket.
    :param s3_path: string, S3 path to the files.
    :param local_folder: string, local folder where files will be downloaded.
    :param start_date: string, start date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'.
    :param end_date: string, end date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'.
    :param timezone: string, timezone for date comparison. Defaults to 'America/Los_Angeles'.
    :return: None
    """
def mtest_download_s3_files_new():
def download_file_from_s3(bucket, key, s3_path, local_folder, overwrite=True):
    """
    Download a single file from S3 to a local folder.

    :param bucket: Name of the S3 bucket
    :param key: The key (filename) of the object in the S3 bucket
    :param s3_path: S3 folder path where the file is stored
    :param local_folder: Local folder where the file will be downloaded
    :param overwrite: If False, skip download if file already exists (default: False)
    :return: Path to the downloaded file if successful, None otherwise
    """
def mtest_download_file_from_s3():
def mrun_S3_mtests():
def generate_presigned_s3_url(bucket, object_key, method='get', content_type=None, expire_seconds=1800):
    """
    Generate a presigned URL for 'get' or 'put' to allow temporary access to S3 objects.

    :param bucket: S3 bucket name
    :param object_key: Full S3 key, e.g. "audio/filename.mp3"
    :param method: 'get' or 'put'
    :param content_type: Set this if you're generating a PUT URL for JSON or other media
    :param expire_seconds: How many seconds this URL remains valid (default 30 min)
    :return: The presigned URL string
    """
### AWS API KEYS (1,218 tokens)
def create_api_key(key_name, description="API key for Lambda function"):
    """
    Create an API key in API Gateway.
    
    :param key_name: Name of the API key
    :param description: Description of the API key
    :return: API key ID and value
    """
def create_usage_plan(plan_name, rate_limit=10, burst_limit=20, quota_limit=1000, quota_period='DAY'):
    """
    Create a usage plan in API Gateway.
    
    :param plan_name: Name of the usage plan
    :param rate_limit: Requests per second
    :param burst_limit: Maximum concurrent requests
    :param quota_limit: Number of requests per period
    :param quota_period: Period for quota (DAY, WEEK, or MONTH)
    :return: Usage plan ID
    """
def mrun_create_usage_plan():
def get_usage_plan_id_by_name(plan_name):
    """
    Get a usage plan ID by its name.
    
    :param plan_name: Name of the usage plan
    :return: Usage plan ID if found, None otherwise
    """
def associate_api_key_with_usage_plan(usage_plan_id, api_key_id):
    """
    Associate an API key with a usage plan.
    
    :param usage_plan_id: ID of the usage plan
    :param api_key_id: ID of the API key
    :return: True if successful, False otherwise
    """
def mrun_create_api_key_and_associate_with_usage_plan():
def associate_usage_plan_with_api_gateway(usage_plan_id, rest_api_id, stage='api'):
    """
    Associate a usage plan with an API Gateway stage.
    
    :param usage_plan_id: ID of the usage plan
    :param rest_api_id: ID of the REST API Gateway
    :param stage: API stage name (default: 'api')
    :return: True if successful, False otherwise
    """
def enable_api_key_requirement(rest_api_id, resource_id, http_method):
    """
    Enable API key requirement for a specific API method.
    
    :param rest_api_id: ID of the REST API
    :param resource_id: ID of the API resource
    :param http_method: HTTP method (GET, POST, etc.)
    :return: True if successful, False otherwise
    """
def mrun_enable_api_key_requirement():
def get_api_gateway_ids(api_name, http_method, verbose=True):
    """
    Get REST API ID and resource ID from API Gateway using the API name and HTTP method.
    
    :param api_name: Name of the API Gateway (e.g., 'testapp')
    :param http_method: HTTP method to find (e.g., 'GET', 'POST')
    :param stage: API stage name (default: 'dev')
    :return: Tuple of (rest_api_id, resource_id) or (None, None) if not found
    """
def mtest_get_api_gateway_ids():
def create_deployment(rest_api_id, stage_name='api'):
    """
    Create a deployment for the API Gateway to apply changes.
    
    :param rest_api_id: ID of the REST API
    :param stage_name: Name of the stage to deploy to (default: 'api')
    :return: True if successful, False otherwise
    """
def mrun_create_deployment():
def setup_api_security(lambda_function_base_name, api_key_id=None, usage_plan_name=USAGE_PLAN_NAME_DEMO, stage='-dev', http_method='POST'):
    """
    Set up API security for a Lambda function.
    
    Assumes:
    - API Gateway name matches the lambda_function_base_name
    - Full Lambda function name is {lambda_function_base_name}{stage}
    - Example: lambda_function_base_name='testapp', stage='-dev' → Lambda name='testapp-dev'
    
    :param lambda_function_base_name: Base name of the Lambda function (e.g., 'testapp')
    :param usage_plan_name: Name of the usage plan to associate with the API key (default: USAGE_PLAN_NAME_DEMO)
    :param stage: Stage suffix for Lambda function name (default: '-dev')
    :param http_method: HTTP method to secure (default: 'POST')
    :param api_key_id: Optional existing API key ID to use
    :return: Dictionary containing API key and usage plan details
    """
def mrun_setup_api_security():
def list_api_keys(name_prefix=None, show_api_key=False):
    """
    List all API keys with their associated usage plans and APIs.
    
    :param name_prefix: Optional prefix to filter API keys by name
    :param show_api_key: If True, show full API key value. If False, show only first 5 chars
    :return: List of API key details
    """
def mtest_list_api_keys():
def delete_api_key(key_id=None):
    """
    Delete an API key by its ID. If no key_id provided, prompts user for input.
    
    :param key_id: ID of the API key to delete (optional)
    :return: True if successful, False otherwise
    """
def mrun_delete_api_key():
def test_api_key(api_key, input_text="test@example.com", show_command=False, verbose=False):
    """
    Test an API key by making a curl request to the HMAC hash endpoint.
    """    
def mtest_test_api_key():
def detach_usage_plan_from_api(usage_plan_id, api_id, stage='api'):
    """
    Remove an API stage from a usage plan.
    
    :param usage_plan_id: ID of the usage plan
    :param api_id: ID of the API to detach
    :param stage: API stage name (default: 'api')
    :return: True if successful, False otherwise
    """
def mrun_detach_usage_plan_from_api():
### AWS WAF (364 tokens)
def quick_waf_test():
    """Didn't actually run this 12-20 RT"""
    usage_plan_id = 'djv4a9'  # from demo usage plan, can get from list_api_keys()
    apis_to_detach = [
        'lvyznjx395',  # send-email
        'n5yjgn8jak',  # vrag-llm
        'sz901mb96d',  # qrag-llm
        'us05oglu51',  # qrag-routing
        'wd3rapoqy7',  # hash-store
    ]
    for api_id in apis_to_detach:
        detach_usage_plan_from_api(usage_plan_id, api_id)
    list_api_keys()

    """Quick test to verify WAF is connected"""
def mrun_quick_waf_test():
def test_rate_limits():
    """
    Quick test of WAF and API Gateway rate limits using the HMAC hash endpoint
    """
def mrun_test_rate_limits():
def test_waf_limit_old():
    """
    Aggressive test focusing only on WAF rate limit with detailed diagnostics
    """
def test_waf_limit(initial_rapid_requests=20, wait_minutes=2, post_wait_requests=5, verbose=False):
    """
    Aggressive test focusing only on WAF rate limit with detailed diagnostics
    
    :param verbose: If True, prints detailed debugging info including full responses
    :param initial_rapid_requests: Number of initial rapid requests to send
    :param wait_minutes: Minutes to wait after initial requests (0 to skip wait and post-wait requests)
    :param post_wait_requests: Number of requests to send after waiting
    """
def mrun_test_waf_limit():
### AWS LOGGING (85 tokens)
def setup_api_gateway_logging(api_names=None):
    """
    Set up detailed logging for API Gateway stages.
    If api_names is None, will configure all APIs in LAMBDA_GLOBALS_MAPPING.
    
    :param api_names: list of str, optional list of API names to configure
    :return: dict, results of configuration attempts
    """
def mrun_setup_api_gateway_logging():
### AWS JWT (158 tokens)
def get_jwt_signing_key():
    """
    Retrieve JWT signing key from AWS Secrets Manager.

    :return str: The JWT signing key
    """
def generate_jwt(subject_claim, expiry_days):
    """
    Generate a JWT token with specified subject claim and expiry.

    :param subject_claim: str, value for the 'sub' claim in JWT
    :param expiry_days: int, number of days until token expires
    :return str: JWT token
    """
def verify_jwt(token):
    """
    Verify a JWT token.

    :param token: str, the JWT token to verify
    :return: dict with decoded claims if valid, None if invalid
    """
def mrun_verify_jwt():
def mtest_generate_and_verifyjwt():

## primary/aws_valid.py (4,506 tokens)
### AWS API GATEWAY VALIDATION (4,500 tokens)
def get_lambda_configurations():
    """
    Gather all Lambda-related global variables based on naming conventions.

    :return configurations: dict, dict of dicts with all configurations.
    """
def create_complete_request(partial_request, template_request):
    """
    Create a complete request by filling in missing fields from a template.
    Special handling: If a field's value is REMOVE_FIELD, remove it from the final request.
    
    :param partial_request: dict, the request with some fields specified.
    :param template_request: dict, complete request to use as a template for missing fields.
    :return complete_request: dict, complete request with all fields, using template values for missing fields.
    """
    def update_dict(template, partial):
def mtest_create_complete_request():
def test_lambda_requests(lambda_function, stage='dev', direct_lambda=True, with_gateway=True, debug_prompt=False, output_file="web/test_back-end_validation.md", jwt_token=None):
        """Recursively update template dict with partial dict values."""
        result = template.copy()
        for key, value in partial.items():
            if value == REMOVE_FIELD:
                result.pop(key, None)
            elif isinstance(value, dict) and key in template and isinstance(template[key], dict):
                # Recursively update nested dictionaries
                result[key] = update_dict(template[key], value)
            else:
                result[key] = value
        return result

    # Check if either has description/request structure
    partial_has_structure = isinstance(partial_request, dict) and set(partial_request.keys()) == {"description", "request"}
    template_has_structure = isinstance(template_request, dict) and set(template_request.keys()) == {"description", "request"}
    
    # If one has structure and other doesn't, that's an error
    if partial_has_structure != template_has_structure:
        raise ValueError("Both partial_request and template_request must have the same structure (either both with description/request or both without)")
    
    if partial_has_structure:
        # Process only the request portion
        complete_request_data = update_dict(template_request["request"], partial_request["request"])
        return {
            "description": partial_request["description"],
            "request": complete_request_data
        }
    else:
        # Original behavior for non-structured requests
        return update_dict(template_request, partial_request)
    pass
#if __name__ == "__main__":
    template_request = TEST_REQUESTS_QRAG_LLM['clean_requests'][0]
    partial_request = TEST_REQUESTS_QRAG_LLM['schema_invalid_requests'][0]
    complete_request = create_complete_request(partial_request, template_request)
    expected_request = {   
            "description": "Invalid llm_model value - Not in enum list",  # Use partial request's description
            "request": {
                "metadata": {
                    "timestamp": "2024-06-13T11:46:33.651753",
                    "user_id": "default", 
                    "vector_index_name": "deutsch-transcript-qrag-78f-20240926",
                    "bot_version": "1.0",
                    "llm_model": "gpt-3",
                    "routes_info": {
                        "routes_flow_name": "3 routes, sim-star double, separate prompts",
                        "upper_sim_bound": 0.9,
                        "lower_sim_bound": 0.3,
                        "max_sim": "0.216",
                        "max_stars": 5,
                        "routes_dict_content": {
                            "routes_dict_name": "ROUTES_DICT_DEUTSCH_V3"
                        }
                    }
                },
                "content": {
                    "user_question": "What should I eat for lunch?",
                    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
                    "quoted_qa": "",
                    "ai_answer": "WAITING FOR LLM RESPONSE",
                    "chunks": {
                        "max_sim": "0.216",
                        "max_stars": 5,
                        "chunks": []
                    }
                }
            }
    }
    if complete_request == expected_request:
        print("Complete request matches expected request - TEST PASSES!!")
    else:
        print("Complete request does not match expected request - TEST FAILS!!")
        print("Complete Request:")
        print(json.dumps(complete_request, indent=4))
        print("Expected Request:")
        print(json.dumps(expected_request, indent=4))

#lambda_function='deepgram-callback'  
#lambda_function='hmac-hash'      # No JWT - PASS 12-21 0540
#lambda_function='hash-store'     # No JWT - PASS 12-21 0540
#lambda_function='send-email'     # JWT - PASS 12-21 0723
lambda_function='qrag-routing'   # JWT - PASS 12-21 0540
#lambda_function='qrag-llm'       # JWT - PASS 12-21 0642
#lambda_function='vrag-llm'       # JWT - PASS 12-21 0717
all_lambdas = ['deepgram-callback', 'hmac-hash', 'hash-store', 'send-email', 'qrag-routing', 'qrag-llm', 'vrag-llm']

    """
    def write_to_both(message):
    """
    # Create StringIO object to capture output
    from io import StringIO
    import sys
    output_buffer = StringIO()
    original_stdout = sys.stdout
    sys.stdout = output_buffer

        """Helper function to write to both file and terminal"""
    def invoke_lambda(request_data):
    def invoke_gateway(request_data):
        """Direct Lambda invocation that simulates API Gateway event."""
        try:
            # Extract route from API endpoint URL
            api_endpoint_parts = api_endpoint.split('/')
            route = '/' + api_endpoint_parts[-1]  # Get the last part of the URL
            
            # Build headers with optional JWT
            headers = {
                "Content-Type": "application/json",
                "origin": "https://www.focusonfoundations.org"
            }
            if jwt_token:
                headers["Authorization"] = f"Bearer {jwt_token}"

            # Build a mock API Gateway event
            lambda_payload = {
                "resource": route,
                "path": route,
                "httpMethod": "POST",
                "headers": headers,
                "multiValueHeaders": {
                    "Content-Type": ["application/json"]
                },
                "queryStringParameters": None,
                "multiValueQueryStringParameters": None,
                "pathParameters": None,
                "stageVariables": None,
                "requestContext": {
                    "resourcePath": route,
                    "httpMethod": "POST",
                    "stage": stage,
                    "identity": {
                        "sourceIp": "127.0.0.1",
                        "userAgent": "custom-agent"
                    }
                },
                "body": json.dumps(request_data),
                "isBase64Encoded": False
            }

            response = lambda_client.invoke(
                FunctionName=aws_lambda_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(lambda_payload)
            )

            # Parse and debug the response
            response_payload = json.loads(response['Payload'].read())
            print("Lambda response payload:", json.dumps(response_payload, indent=2))
            
            return response_payload

        except Exception as e:
            print(f"Error invoking Lambda: {e}")
            return {"error": str(e)}

        """API Gateway invocation"""
    def check_lambda_success(lambda_result):
    def check_gateway_success(gateway_result):
        """Check if Lambda invocation was successful"""
        try:
            # Check if it's a direct Lambda response (contains statusCode and body)
            if "statusCode" in lambda_result:
                if lambda_result["statusCode"] != 200:
                    return False
                # Parse the body if it's a string
                body = (json.loads(lambda_result["body"]) 
                       if isinstance(lambda_result["body"], str) 
                       else lambda_result["body"])
                return body.get("status") == "Success"
            # Otherwise check if it's already parsed response
            return lambda_result.get("status") == "Success"
        except Exception as e:
            print(f"Error checking Lambda success: {e}")
            return False

        """Check if Gateway invocation was successful"""
    def summarize_results(results):
def mrun_test_lambda_requests():
def check_validation_setup(lambda_function, http_method='POST', verbose=False):
        """Summarize test results and expectations"""
        # Initialize summary
        summary = {category: {
            "total": 0,
            "lambda": {"success": 0, "error": 0},
            "gateway": {"success": 0, "error": 0}
        } for category in results.keys()}
        
        total_tests = 0
        failed_tests = 0
        
        write_to_both(f"\n## ===== API Gateway Validation Test Summary {lambda_function} =====")
        
        for category, requests in results.items():
            summary[category]["total"] = len(requests)
            total_tests += len(requests) * 2
            
            write_to_both(f"\n{category} ({summary[category]['total']} tests):")
            
            # Define expected behavior for each category
            expected_behaviors = {
                "clean_requests": {"lambda": "SUCCESS", "gateway": "SUCCESS"},
                "schema_invalid_requests": {"lambda": "SUCCESS", "gateway": "ERROR"},
                "function_invalid_requests": {"lambda": "ERROR", "gateway": "ERROR"}
            }
            
            # Get expected behavior for this category
            expected = expected_behaviors[category]
            
            # Lambda Results
            expected_lambda = "SUCCESS" if "clean" in category else "ERROR" if "function_invalid" in category else "SUCCESS"
            lambda_stats = summary[category]["lambda"]
            
            # Track successes/errors for summary stats
            for i, result in enumerate(requests, 1):
                if result["lambda_result"]:
                    if result["lambda_result"]["success"]:
                        lambda_stats["success"] += 1
                    else:
                        lambda_stats["error"] += 1
                    
                    # Compare against expected behavior for failure count
                    if ((result["lambda_result"]["success"] and expected["lambda"] == "ERROR") or 
                        (not result["lambda_result"]["success"] and expected["lambda"] == "SUCCESS")):
                        failed_tests += 1
                
                if result["gateway_result"]:
                    if result["gateway_result"]["success"]:
                        summary[category]["gateway"]["success"] += 1
                    else:
                        summary[category]["gateway"]["error"] += 1
                    
                    # Compare against expected behavior for failure count
                    if ((result["gateway_result"]["success"] and expected["gateway"] == "ERROR") or 
                        (not result["gateway_result"]["success"] and expected["gateway"] == "SUCCESS")):
                        failed_tests += 1
            
            # Display Lambda results
            lambda_passed = (
                (expected_lambda == "SUCCESS" and lambda_stats["success"] == summary[category]["total"]) or
                (expected_lambda == "ERROR" and lambda_stats["error"] == summary[category]["total"])
            )
            write_to_both(f"  Lambda Results: (expected {expected_lambda})  {'✓' if lambda_passed else '✗'}")
            for i, result in enumerate(requests, 1):
                if result["lambda_result"]:
                    status = "SUCCESS" if result["lambda_result"]["success"] else "ERROR"
                    write_to_both(f"    test {i}:  {status}")
                else:
                    write_to_both(f"    test {i}:  SKIPPED")
            
            # Display Gateway results
            expected_gateway = "SUCCESS" if "clean" in category else "ERROR"
            gateway_stats = summary[category]["gateway"]
            gateway_passed = (
                (expected_gateway == "SUCCESS" and gateway_stats["success"] == summary[category]["total"]) or
                (expected_gateway == "ERROR" and gateway_stats["error"] == summary[category]["total"])
            )
            write_to_both(f"  Gateway Results: (expected {expected_gateway})  {'✓' if gateway_passed else '✗'}")
            for i, result in enumerate(requests, 1):
                if result["gateway_result"]:
                    status = "SUCCESS" if result["gateway_result"]["success"] else "ERROR"
                    write_to_both(f"    test {i}:  {status}")
                else:
                    write_to_both(f"    test {i}:  SKIPPED")
        
        # Print final summary
        passed_tests = total_tests - failed_tests
        write_to_both(f"\nTest Results: {passed_tests} passed, {failed_tests} failed  {'✓' if failed_tests == 0 else '✗'}")

        return summary

    try:
        # Run tests and get summary
        summary = summarize_results(results)

        # Write captured output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("## API Gateway Validation Test Results\n\n")
            f.write(output_buffer.getvalue())
        
        return results

    finally:
        sys.stdout = original_stdout
        output_buffer.close()
    pass
if __name__ == "__main__":
    jwt_token = None
    if LAMBDA_JWT_REQUIRED.get(lambda_function, False):
        jwt_token = JWT_TEST

    results = test_lambda_requests(lambda_function, direct_lambda=True, with_gateway=True, jwt_token=jwt_token)

    """
def mrun_check_validation_setup():
def create_request_model(rest_api_id, model_name, schema, description=None, prompt_overwrite=True):
    """
    api_client = boto3.client('apigateway')
    rest_api_id, resource_id = get_api_gateway_ids(lambda_function, http_method, verbose=verbose)
    
    # Get method configuration
    method = api_client.get_method(
        restApiId=rest_api_id,
        resourceId=resource_id,
        httpMethod='POST'
    )
    
    if verbose:
        print("Method configuration:")
        print(json.dumps(method, indent=2))
    
    validator_id = method.get('requestValidatorId', 'None')
    model_name = method.get('requestModels', {}).get('application/json', 'None')
    
    print(f"\nAPI Gateway validation setup for {lambda_function}:")
    print(f"  Validator ID: {validator_id}")
    print(f"  Request Model: {model_name}")
    
    # Return True if both validator ID and model name exist and are not 'None'
    return validator_id != 'None' and model_name != 'None'
    pass
#if __name__ == "__main__":
    validation_exists = check_validation_setup(lambda_function)
    print(f"API Gateway validation exists for {lambda_function}: {validation_exists}")
    
    # OR TO CHECK ALL LAMBDAS:
    # for lambda_function in all_lambdas:
    #     validation_exists = check_validation_setup(lambda_function)
    #     print(f"API Gateway validation exists for {lambda_function}: {validation_exists}")

    """
def update_method_validation(rest_api_id, resource_id, http_method, model_name):
    """
    api_client = boto3.client('apigateway')
    
    try:
        # Check if model already exists
        try:
            existing_model = api_client.get_model(
                restApiId=rest_api_id,
                modelName=model_name
            )
            if prompt_overwrite:
                response = input(f"\nModel '{model_name}' already exists. Update it? (y/n): ")
                if response.lower() != 'y':
                    print("Skipping model update.")
                    return existing_model['id']
                    
                # Update existing model
                try:
                    api_client.update_model(
                        restApiId=rest_api_id,
                        modelName=model_name,
                        patchOperations=[
                            {
                                'op': 'replace',
                                'path': '/schema',
                                'value': json.dumps(schema)
                            },
                            {
                                'op': 'replace',
                                'path': '/description',
                                'value': description or f'Request validation model for {model_name}'
                            }
                        ]
                    )
                    print(f"Updated existing model '{model_name}'")
                    return existing_model['id']
                except ClientError as e:
                    print(f"Error updating existing model: {e}")
                    return None
            else:
                print(f"Model '{model_name}' already exists, skipping update.")
                return existing_model['id']
                
        except ClientError as e:
            if not 'NotFoundException' in str(e):
                raise
        
        # Create new model if it doesn't exist
        response = api_client.create_model(
            restApiId=rest_api_id,
            name=model_name,
            description=description or f'Request validation model for {model_name}',
            contentType='application/json',
            schema=json.dumps(schema)
        )
        print(f"Created model '{model_name}' for API {rest_api_id}")
        return response['id']
        
    except ClientError as e:
        print(f"Error creating model: {e}")
        return None
    """
def setup_request_validation(lambda_function, http_method='POST'):
    """
    api_client = boto3.client('apigateway')
    
    try:
        # First try to get existing validator
        validator_id = None
        try:
            validators = api_client.get_request_validators(restApiId=rest_api_id)
            for validator in validators.get('items', []):
                if validator['validateRequestBody']:
                    validator_id = validator['id']
                    print(f"Found existing request validator: {validator['name']}")
                    break
        except ClientError:
            pass

        # Create validator only if none exists
        if not validator_id:
            try:
                validator = api_client.create_request_validator(
                    restApiId=rest_api_id,
                    name='validate-body',
                    validateRequestBody=True,
                    validateRequestParameters=False
                )
                validator_id = validator['id']
                print("Created new request validator")
            except ClientError as e:
                print(f"Error creating validator: {e}")
                return False

        # First, update the method to ensure Content-Type is set up
        try:
            api_client.update_method(
                restApiId=rest_api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                patchOperations=[
                    {
                        'op': 'add',
                        'path': '/requestParameters/method.request.header.Content-Type',
                        'value': 'false'  # false means optional
                    }
                ]
            )
            print("Added Content-Type header parameter")
        except ClientError as e:
            if 'ConflictException' in str(e):
                print("Content-Type header parameter already exists")
            else:
                print(f"Warning: Could not update Content-Type header: {e}")

        # Now update the method with validator and model
        api_client.update_method(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/requestValidatorId',
                    'value': validator_id
                },
                {
                    'op': 'add',
                    'path': '/requestModels/application~1json',
                    'value': model_name
                }
            ]
        )
        print(f"Enabled request validation for {http_method} method using model '{model_name}'")
        return True
    except ClientError as e:
        print(f"Error updating method validation: {e}")
        return False
    """
def mrun_setup_request_validation():
def toggle_request_validation(lambda_function, http_method='POST'):
    """
    # Get schema for this API using the LAMBDA_GLOBALS_MAPPING
    suffix = LAMBDA_GLOBALS_MAPPING.get(lambda_function)
    schema = globals().get(f"SCHEMA_{suffix}")
    if not schema:
        print(f"No schema defined for API: {lambda_function}")
        return False
    
    # Get API Gateway IDs
    rest_api_id, resource_id = get_api_gateway_ids(lambda_function, http_method)
    if not rest_api_id or not resource_id:
        print(f"Failed to get API Gateway IDs for {lambda_function}")
        return False
    
    # Create request model
    model_name = f"{lambda_function.replace('-', '')}Model"
    model_id = create_request_model(rest_api_id, model_name, schema)
    if not model_id:
        return False
    
    # Update method to use validation
    if not update_method_validation(rest_api_id, resource_id, http_method, model_name):
        return False
    
    # Create deployment to apply changes
    if not create_deployment(rest_api_id):
        return False
    
    print(f"Successfully set up request validation for {lambda_function}")
    return True
    pass
#if __name__ == "__main__":
    check_validation_setup(lambda_function)
    if setup_request_validation(lambda_function):
        user_continue_response = input("\n*** WAIT 30 SECONDS FOR CHANGE TO TAKE EFFECT *** - Then Press any key to continue or 'x' to exit...").strip().lower()
        if user_continue_response != 'x':
            # Use the same JWT logic as mrun_test_lambda_requests
            jwt_token = None
            if LAMBDA_JWT_REQUIRED.get(lambda_function, False):
                jwt_token = JWT_TEST
                
            test_lambda_requests(
                lambda_function, 
                direct_lambda=True, 
                with_gateway=True, 
                jwt_token=jwt_token
            )

#TODO: Not tested yet
    """
def mrun_toggle_request_validation():

## primary/rag_prompts_routes.py (3,358 tokens)
    """
    api_client = boto3.client('apigateway')
    
    try:
        # Get API Gateway IDs
        rest_api_id, resource_id = get_api_gateway_ids(lambda_function, http_method)
        if not rest_api_id or not resource_id:
            print(f"Failed to get API Gateway IDs for {lambda_function}")
            return False
            
        # Get current method configuration
        method = api_client.get_method(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod=http_method
        )
        
        # Check if validation is currently enabled
        validation_enabled = ('requestValidatorId' in method and 
                            'requestModels' in method and 
                            'application/json' in method.get('requestModels', {}))
        
        if validation_enabled:
            # Disable validation by removing validator and model references
            patch_operations = [
                {
                    'op': 'remove',
                    'path': '/requestValidatorId'
                },
                {
                    'op': 'remove', 
                    'path': '/requestModels/application~1json'
                }
            ]
            
            api_client.update_method(
                restApiId=rest_api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                patchOperations=patch_operations
            )
            
            print(f"Request validation for {lambda_function} is now: DISABLED")
        else:
            # Get validator ID
            validators = api_client.get_request_validators(restApiId=rest_api_id)
            validator_id = next((v['id'] for v in validators.get('items', []) 
                              if v['validateRequestBody']), None)
            
            if not validator_id:
                print("No request validator found. Please run setup_request_validation first.")
                return False
                
            # Enable validation by adding validator and model references
            api_client.update_method(
                restApiId=rest_api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                patchOperations=[
                    {
                        'op': 'replace',
                        'path': '/requestValidatorId',
                        'value': validator_id
                    },
                    {
                        'op': 'replace',
                        'path': '/requestModels/application~1json',
                        'value': f"{lambda_function.replace('-', '')}Model"
                    }
                ]
            )
            print(f"Request validation for {lambda_function} is now: ENABLED")
        
        # Create deployment to apply changes
        if not create_deployment(rest_api_id):
            return False
            
        return True
        
    except ClientError as e:
        print(f"Error toggling validation: {e}")
        return False
    pass
#if __name__ == "__main__":
    lambda_function = "hash-store"
    #toggle_request_validation(lambda_function)
    #test_lambda_requests(lambda_function, direct_lambda=True, with_gateway=True)

'''
IMPORTANT: the chalice deploy script: web/aws_chalice/chalicelib_mirror_deploy.sh
will read whether the API Gateway validation is enabled or disabled
then it will preserve that state by rerunning the setup_request_validation if enabled.
'''

#aws apigateway delete-model --rest-api-id xusv8bpl49 --model-name hmachashModel

#===== END OF FILE primary/aws-valid.py =====




#===== START OF FILE primary/rag_prompts_routes.py =====
#Routes and prompts for RAG

#---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

ROUTES_DICT_FDA_TOWNHALLS_V1 = {
    'routes_dict_name': 'ROUTES_DICT_FDA_TOWNHALLS_V1',  # mirror global variable name
    
    'prompt_initial_good_match': "Given your knowledge of the FDA Town Hall meetings—covering test modifications, bridging studies, validation requirements, and other relevant regulatory guidelines—as well as the QUOTED QUESTIONS AND ANSWERS from FDA sources below, answer the USER QUESTION. Provide clear, concise information about any relevant FDA policies or processes referenced in the quoted material.",
    'route_preamble_good_match': "There is a good match for your question in the FDA Town Hall documentation. See the QUOTED QUESTIONS AND ANSWERS below, followed by an AI ANSWER that synthesizes these official FDA sources with your specific question.",

    'prompt_initial_partial_match': "Given your knowledge of the FDA Town Hall meetings—covering test modifications, bridging studies, validation requirements, and other relevant regulatory guidelines—as well as the QUOTED QUESTIONS AND ANSWERS from FDA sources below, answer the USER QUESTION. While the quotes only partially match the user's question, do your best to integrate relevant information from these official FDA sources.",
    'route_preamble_partial_match': "There is a partial match for your question in the FDA Town Hall documentation. See the QUOTED QUESTIONS AND ANSWERS below, followed by an AI ANSWER that synthesizes these official FDA sources with your specific question.",

    'prompt_initial_no_match': "You are a helpful assistant. Your task is to identify what topic the user's question appears to be about and respond with a single sentence stating that their question appears to be about that topic and noting that it is unrelated to the FDA Town Hall corpus.",
    'route_preamble_no_match': "There are no relevant matches for your question in the FDA Town Hall documentation. This system is designed to answer questions about FDA Town Hall content, including bridging studies, test modifications, and related regulatory processes. If your question is indeed about FDA Town Hall topics, please rephrase or clarify so we can best assist you.",

    # Note: "REVIEW FLAG" is purposely excluded per instructions
    "quoted_qa_item_template": (
        "CLARIFIED QUESTION: {question}\n"
        "CLARIFIED ANSWER: {answer}\n"
        "VERBATIM QUESTION: {verbatim_question}\n"
        "VERBATIM ANSWER: {verbatim_answer}\n"
        "SPEAKER FOR QUESTION: {speaker_question}\n"
        "SPEAKER FOR ANSWER: {speaker_answer}\n"
        "TOPICS: {topics}\n"
        "SOURCE: {source}\n"
        "{display}\n\n"
    ),

    "quoted_qa_template": "{quoted_qa_formatted}",

    'user_ai_qa': "USER QUESTION: {user_question}\n\nAI ANSWER: "
}

ROUTES_DICT_PV_EVAC_V1 = {
    'routes_dict_name': 'ROUTES_DICT_PV_EVAC_V1',  # mirror global variable name
    'prompt_initial_good_match': 'Given your knowledge of Portola Valley emergency procedures and wildfire evacuation protocols, as well as the QUOTED QUESTIONS AND ANSWERS from official sources below, answer the USER QUESTION below. Prioritize information related to Shelter in Place by placing it first in any response to a general question or one where the response includes shelter in place. Take the approach to thoughtfully but frankly communicating to parents that shelter-in-place is only considered in the extreme circumstances of a mandatory evacuation order, but if a shelter-in-place order is issued for the schools, the WFPD will bring resources to defend the shelter-in-place facilities with the highest priority, and 2) parents absolutely cannot pick their children up from school, and if they try to do so they will be stopped by fire and police authorities, and they will be putting their lives, their children\'s lives, those of first responders, and the entire community at risk. DO NOT use strong adjectives in your response, such as \'comprehensive\' and \'thorough\', to describe plans or approaches because significantly more work is needed by both authorities and parents to prepare for emergency evacuation of the schools and especially the shelter-in-place scenario.\n',
    'route_preamble_good_match': 'There is a good match for your question in our Portola Valley evacuation documentation. See the QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these official sources with current evacuation protocols and your specific question.',
    'prompt_initial_partial_match': 'Given your knowledge of Portola Valley emergency procedures and wildfire evacuation protocols, as well as the QUOTED QUESTIONS AND ANSWERS from official sources below, answer the USER QUESTION below. Prioritize information related to Shelter in Place by placing it first in any response to a general question or one where the response includes shelter in place. Take the approach to thoughtfully but frankly communicating to parents that shelter-in-place is only considered in the extreme circumstances of a mandatory evacuation order, but if a shelter-in-place order is issued for the schools, the WFPD will bring resources to defend the shelter-in-place facilities with the highest priority, and 2) parents absolutely cannot pick their children up from school, and if they try to do so they will be stopped by fire and police authorities, and they will be putting their lives, their children\'s lives, those of first responders, and the entire community at risk. DO NOT use strong adjectives in your response, such as \'comprehensive\' and \'thorough\', to describe plans or approaches because significantly more work is needed by both authorities and parents to prepare for emergency evacuation of the schools and especially the shelter-in-place scenario.\n',
    'route_preamble_partial_match': 'There is a partial match for your question in our Portola Valley evacuation documentation. See the QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these official sources with current evacuation protocols and your specific question.',
    'prompt_initial_no_match': 'You are a helpful assistant. Your task is to identify what topic the user\'s question appears to be about and respond with a single sentence stating that their question appears to be about that topic and noting that it is unrelated to Portola Valley emergency procedures.\n',
    'route_preamble_no_match': 'There are no matches for your question in the included documents. This system is designed to answer questions about Portola Valley emergency procedures and wildfire evacuation protocols only. Please rephrase your question to focus on Portola Valley emergency procedures if that was your intent.',
    "quoted_qa_item_template": (
        "QUESTION: {question}\n"
        "ANSWER: {answer}\n"
        "SOURCE: {source}\n"
        "TIMESTAMP: {timestamp}\n"
        "{display}\n\n"
    ),
    "quoted_qa_template": "{quoted_qa_formatted}",  # Wraps the entire formatted chunks
    'user_ai_qa': 'USER QUESTION: {user_question}\n\nAI ANSWER: '
}

ROUTES_DICT_DEUTSCH_V4 = {
    'routes_dict_name': 'ROUTES_DICT_DEUTSCH_V4',  # mirror global variable name
    'prompt_initial_good_match': 'Given your knowledge of David Deutsch and his philosophy of deep optimism, as well as the QUOTED QUESTIONS AND ANSWERS from Deutsch below, answer the USER QUESTION below.\n',
    'route_preamble_good_match': 'There is a good match of your question in David Deutsch\'s interviews. See his QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with David Deutsch\'s philosophy and your exact question.',
    'prompt_initial_partial_match': 'Given your knowledge of David Deutsch and his philosophy of deep optimism, as well as the QUOTED QUESTIONS AND ANSWERS from Deutsch below, answer the USER QUESTION below.\n',
    'route_preamble_partial_match': 'There is a partial match of your question in David Deutsch\'s interviews. See his QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with David Deutsch\'s philosophy and your exact question.',
    'prompt_initial_no_match': 'Given your knowledge of David Deutsch and his philosophy of deep optimism, answer the USER QUESTION below.\n',
    'route_preamble_no_match': 'Your question is not addressed in David Deutsch\'s interviews. No QUOTED QUESTIONS AND ANSWERS are therefore provided but here is an AI ANSWER that synthesizes David Deutsch\'s philosophy and your question.',
    "quoted_qa_item_template": (
        "QUESTION: {question}\n"
        "ANSWER: {answer}\n"
        "SOURCE: {source}\n"
        "TIMESTAMP: {timestamp}\n"
        "{display}\n\n"
    ),
    "quoted_qa_template": "{quoted_qa_formatted}",  # Wraps the entire formatted chunks
    'user_ai_qa': 'USER QUESTION: {user_question}\n\nAI ANSWER: '
}

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

## primary/video.py (6,530 tokens)
### YOUTUBE VIDEO (207 tokens)
def download_video_from_youtube(url, output_title, output_dir='data/0_gitignore', skip_download=False, max_retries=10):  # change skip_download=True for testing
"""


VRAG_PREAMBLE_V1 = 'Use the sources provided below to provide a insightful and accurate answer that is faithful to the information and meaning established by the given sources. If you do not know, truthfully say you do not know, but try your best to answer'

#===== END OF FILE primary/rag_prompts_routes.py =====




#===== START OF FILE primary/video.py =====
#Library of functions and execution code to process video files

import os
import sys
import yt_dlp as youtube_dl
import cv2  # pip install opencv-python
import pytesseract
from PIL import Image
import numpy as np
import glob
import csv
import shutil
import time
import re
from difflib import SequenceMatcher
import scipy.stats


    """ 
### IMAGE PROCESSING OPTIMIZATION (1,328 tokens)
def extract_frame_with_region(video_path, timestamp, region_coords):
    """
    # Validate output_title has no path separators
    if '/' in output_title or '\\' in output_title:
        raise ValueError(f"output_title must not contain path separators. Use output_dir parameter to specify path. Got: {output_title}")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file_path = os.path.join(output_dir, output_title + '.mkv')
    if os.path.exists(output_file_path):
        if skip_download:
            print(f"Video file exists at {output_file_path}. Using existing file (skip_download=True).")
            return output_file_path
        print(f"Video file exists at {output_file_path}. Will delete existing file and start download.")
        os.remove(output_file_path)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, output_title + '.%(ext)s'),
        'merge_output_format': 'mkv',  # Explicitly specify mkv as output format
    }

    for attempt in range(max_retries):
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            # If download succeeds, break out of retry loop
            break
        except Exception as e:
            if attempt < max_retries - 1:  # Don't sleep on last attempt
                sleep_time = min(2 ** attempt, 60)  # Exponential backoff, max 60 seconds
                print(f"\nDownload attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                print(f"Waiting {sleep_time} seconds before retrying...")
                time.sleep(sleep_time)
            else:
                print(f"\nAll {max_retries} download attempts failed. Last error: {str(e)}")
                raise  # Re-raise the last exception if all retries failed

    return output_file_path

REGION_LL = (0, 0.97, 0.09, 1)
REGION_C = (0.2, 0.4, 0.8, 0.6)
REGION_UR = (0.833, 0.14, 0.93, 0.165)
TC_PER_REGION_PARAMS = {
    #'LL': {'mode': 'grayscale'},
    'LL': {'mode': 'binary', 'binary_threshold': 200},
    'C':  {'mode': 'binary', 'binary_threshold': 136, 'detection_threshold': 0.95},
    #'UR': {'mode': 'grayscale'}
    'UR': {'mode': 'binary', 'binary_threshold': 200}
}
    """
def mrun_extract_frame_with_region():
def determine_optimal_thresholds(region_image):
    """
    from primary.fileops import convert_timestamp_to_seconds
    
    # Convert timestamp string to seconds
    time_seconds = convert_timestamp_to_seconds(timestamp)
    
    # Use video's directory as output folder
    output_folder = os.path.dirname(video_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # Open video and seek to timestamp
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(time_seconds * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read frame
    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise ValueError(f"Could not read frame at time_seconds {time_seconds}s")
    
    # Get frame dimensions
    height, width = frame.shape[:2]
    
    # Calculate region coordinates
    x_start_pct, y_start_pct, x_end_pct, y_end_pct = region_coords
    x_start = int(x_start_pct * width)
    y_start = int(y_start_pct * height)
    x_end = int(x_end_pct * width)
    y_end = int(y_end_pct * height)
    
    # Create copy of frame with rectangle
    frame_with_region = frame.copy()
    cv2.rectangle(frame_with_region, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
    
    # Crop region
    region_frame = frame[y_start:y_end, x_start:x_end]
    
    # Save images
    full_frame_path = os.path.join(output_folder, f"frame_full.png")
    region_frame_path = os.path.join(output_folder, f"frame_region.png")
    
    cv2.imwrite(full_frame_path, frame_with_region)
    cv2.imwrite(region_frame_path, region_frame)
    
    cap.release()
    
    print(f"Saved frame images:")
    print(f"Full frame with region: {full_frame_path}")
    print(f"Cropped region: {region_frame_path}")
    print(f"Frame dimensions: {width}x{height}")
    print(f"Region coordinates (pixels): ({x_start}, {y_start}) to ({x_end}, {y_end})")
    
    return full_frame_path, region_frame_path
    pass
#if __name__ == "__main__":
    video_path = "data/0_gitignore/video_extracted_profiles.mkv"
    # 0,0 is UL (x_start%, y_start%, x_end%, y_end%)
    # timestamp = "1:07:58"
    #region_coords = REGION_UR
    # timestamp = "1:57:14"
    #region_coords = REGION_LL
    timestamp = "1:08:23"  # "13:24" Town of Portola Valley, initial "36:01"
    region_coords = REGION_UR
    (full_frame_path, region_frame_path) = extract_frame_with_region(video_path, timestamp, region_coords)
    print(f"Full frame path: {full_frame_path}")  # data/0_gitignore/frame_full.png
    print(f"Region frame path: {region_frame_path}")  # data/0_gitignore/frame_region.png

    """
def mrun_determine_optimal_thresholds():
### VIDEO PROCESSING (3,328 tokens)
def extract_frames_and_perform_ocr(
    """
    # Convert to grayscale
    gray = cv2.cvtColor(region_image, cv2.COLOR_BGR2GRAY)

    # Flatten the image to 1D array
    pixels = gray.flatten()

    # Compute Otsu's threshold for binary thresholding
    binary_threshold, _ = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Compute skewness and kurtosis for bimodality coefficient
    skewness = scipy.stats.skew(pixels)
    kurtosis = scipy.stats.kurtosis(pixels, fisher=False)  # Pearson's kurtosis

    # Prevent division by zero in bimodality coefficient calculation
    if kurtosis == 0:
        bimodality_coefficient = 0
    else:
        bimodality_coefficient = (skewness ** 2 + 1) / kurtosis

    detection_threshold = bimodality_coefficient

    return int(binary_threshold), detection_threshold
    pass
#if __name__ == "__main__":
    cur_region_image = cv2.imread("data/0_gitignore/frame_region.png")
    binary_threshold, detection_threshold = determine_optimal_thresholds(cur_region_image)
    print(f"Binary threshold: {binary_threshold}")
    print(f"Detection threshold: {detection_threshold}")

    video_path,
    start_time_seconds,
    end_time_seconds,
    frame_interval,
    regions,
    per_region_params,
    common_profiles_path
):
    """
def calculate_region_similarity(region_frame1, region_frame2, region_name, per_region_params):
    """
    from primary.fileops import track_progress
    
    if regions is None:
        raise ValueError("At least one region must be specified for OCR processing.")
    
    # Initialize target region and profile tracking
    target_region = None  # Start with no target region
    current_profile = 'undetermined'
    previous_region_frames = {name: None for name in regions.keys()}
    
    # Initialize default per_region_params if none provided
    if per_region_params is None:
        per_region_params = {name: {} for name in regions.keys()}

    print(f"\nStarting frame extraction and OCR from {video_path}")
    print(f"Processing frames every {frame_interval} second(s)")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_secs = total_frames / fps
    
    # Set start and end frames based on timestamps
    start_frame = int(start_time_seconds * fps) if start_time_seconds else 0
    end_frame = int(end_time_seconds * fps) if end_time_seconds else total_frames - 1
    
    frame_interval_frames = int(frame_interval * fps)
    frame_count = start_frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    print(f"Video FPS: {fps:.2f}")
    print(f"Total frames in video: {total_frames:,} ({duration_secs:.1f} seconds)")
    print(f"Processing frames from {start_time_seconds or 0}s to {end_time_seconds or duration_secs}s")
    total_frames_to_process = (end_frame - start_frame) // frame_interval_frames + 1
    print(f"Will analyze approximately {total_frames_to_process:,} frames at {frame_interval}-second intervals")
    
    ocr_results = {}
    previous_frame = None
    last_percentage = 0
    start_time = time.time()
    
    # Initialize speaker string tracking per region
    last_speaker_strings = {name: None for name in regions.keys()}
    speaker_string_counts = {name: 0 for name in regions.keys()}
    
    while frame_count <= end_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, frame = cap.read()
        if not ret:
            break
        
        timestamp = frame_count / fps
        
        # Process each region independently
        region_texts = {}
        for name, region in regions.items():
            x_start_pct, y_start_pct, x_end_pct, y_end_pct = region
            height, width = frame.shape[:2]
            x_start = int(x_start_pct * width)
            y_start = int(y_start_pct * height)
            x_end = int(x_end_pct * width)
            y_end = int(y_end_pct * height)
            region_frame = frame[y_start:y_end, x_start:x_end]
            
            # Compare with previous region frame
            region_similar = False
            if previous_region_frames[name] is not None:
                similarity = calculate_region_similarity(
                    previous_region_frames[name],
                    region_frame,
                    name,
                    per_region_params
                )
                similarity_threshold = per_region_params.get(name, {}).get('similarity_threshold', 0.95)
                if similarity >= similarity_threshold:
                    region_similar = True

            if not region_similar:
                # Scale up the cropped region if needed
                scale_factor = per_region_params.get(name, {}).get('scale_factor', 1)
                if scale_factor != 1:
                    region_frame = cv2.resize(region_frame, None, 
                                          fx=scale_factor, 
                                          fy=scale_factor, 
                                          interpolation=cv2.INTER_LINEAR)
                
                # Get region-specific parameters
                region_params = per_region_params.get(name, {})
                mode = region_params.get('mode', 'binary')
                binary_threshold = region_params.get('binary_threshold', None)

                # Check for detection_threshold and apply is_white_text_on_black_background
                detection_threshold = region_params.get('detection_threshold', None)
                if detection_threshold is not None:
                    if not is_white_text_on_black_background(region_frame, detection_threshold):
                        # Set OCR result to empty string and continue to next region
                        region_texts[name] = ''
                        previous_region_frames[name] = region_frame.copy()
                        continue

                # Call perform_ocr_on_region
                region_text = perform_ocr_on_region(region_frame, mode=mode, binary_threshold=binary_threshold).strip()
                region_texts[name] = region_text
            else:
                # Use last known text
                region_texts[name] = last_speaker_strings.get(name, '')

            # Update previous region frame
            previous_region_frames[name] = region_frame.copy()

        # Update target_region and current_profile based on OCR results
        target_region, current_profile = update_target_region(region_texts, common_profiles_path)
        region_texts['profile'] = current_profile
        region_texts['status'] = 'OCR' if not all(region_similar for name in regions.keys()) else 'REPEAT'

        # Store last speaker strings
        for name in regions.keys():
            last_speaker_strings[name] = region_texts.get(name, '')

        # Store OCR results
        ocr_results[int(timestamp)] = region_texts
        
        previous_frame = frame
        frame_count += frame_interval_frames
        
        # Progress update
        frames_processed = (frame_count - start_frame) // frame_interval_frames
        last_percentage = track_progress(frames_processed, total_frames_to_process,
            start_time, last_percentage, "frames")
    
    cap.release()
    print(f"\nFrame extraction and OCR complete! Processed {len(ocr_results):,} frames")
    return ocr_results

    """
def clean_text_alphanumeric(text):
    """
    # Get parameters if needed
    # For simplicity, using the same histogram comparison as before

    # Convert to grayscale
    gray1 = cv2.cvtColor(region_frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(region_frame2, cv2.COLOR_BGR2GRAY)

    # Calculate histograms
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

    # Normalize histograms
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)

    # Compute correlation
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity

    """
def is_white_text_on_black_background(region_image, detection_threshold):
    """
    if not text:
        return ""
    
    # Keep only alphanumeric chars and spaces, convert to single spaces
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

    """
def mrun_is_white_text_on_black_background():
def perform_ocr_on_region(region_image, mode='binary', binary_threshold=None):
    """
    # Convert to grayscale
    gray = cv2.cvtColor(region_image, cv2.COLOR_BGR2GRAY)
    pixels = gray.flatten()

    # Check bimodality first
    skewness = scipy.stats.skew(pixels)
    kurtosis = scipy.stats.kurtosis(pixels, fisher=False)
    if kurtosis == 0:
        bimodality_coefficient = 0
    else:
        bimodality_coefficient = (skewness ** 2 + 1) / kurtosis

    # If not bimodal enough, return False
    if bimodality_coefficient < detection_threshold:
        return False

    # Use Otsu's method to find optimal threshold
    thresh, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Count pixels above and below threshold
    bright_pixels = np.sum(pixels > thresh)
    dark_pixels = np.sum(pixels <= thresh)
    
    # Calculate mean intensities with safety checks
    bright_pixels_mask = pixels > thresh
    dark_pixels_mask = pixels <= thresh
    
    if not np.any(bright_pixels_mask) or not np.any(dark_pixels_mask):
        return False  # No clear separation between bright and dark regions
    
    bright_mean = np.mean(pixels[bright_pixels_mask])
    dark_mean = np.mean(pixels[dark_pixels_mask])
    
    # Conditions for white text on dark background
    is_text_sparse = bright_pixels < dark_pixels
    has_good_contrast = (bright_mean - dark_mean) > 50
    is_background_dark = dark_mean < 128

    return is_text_sparse and has_good_contrast and is_background_dark
    pass
#if __name__ == "__main__":
    cur_region_image = cv2.imread("data/0_gitignore/frame_region.png")
    cur_detection_threshold = TC_PER_REGION_PARAMS['C']['detection_threshold']
    result = is_white_text_on_black_background(cur_region_image, detection_threshold=cur_detection_threshold)
    print("Is white text on black background: ", result)

    """
def find_best_profile_match(text, common_profiles, match_ratio_threshold=0.5):
    """
    # Convert to grayscale if not already
    gray = cv2.cvtColor(region_image, cv2.COLOR_BGR2GRAY)

    if mode == 'binary':
        # Apply binary thresholding
        if binary_threshold is not None:
            _, processed_image = cv2.threshold(gray, binary_threshold, 255, cv2.THRESH_BINARY)
        else:
            # Use Otsu's thresholding if no threshold is provided
            _, processed_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif mode == 'grayscale':
        processed_image = gray
    else:
        raise ValueError("Invalid mode specified. Use 'binary' or 'grayscale'.")

    # Convert back to RGB as required by pytesseract
    rgb = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)

    # Get OCR text and clean it
    text = pytesseract.image_to_string(rgb)
    return clean_text_alphanumeric(text)

    """
def update_target_region(ocr_results, common_profiles_path):
    """
    best_match = text
    highest_ratio = 0.0
    
    for profile in common_profiles:
        ratio = SequenceMatcher(None, text.lower(), profile.lower()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = profile
            
    # Only return the match if it meets the threshold
    if highest_ratio >= match_ratio_threshold:
        return best_match, highest_ratio
    return text, highest_ratio

    """
def map_and_condense_ocr_results(ocr_results):
    """
    # Initialize common_profiles as empty list
    common_profiles = []
    
    # Try to read common profiles if path is provided
    if common_profiles_path:
        try:
            with open(common_profiles_path, 'r', encoding='utf-8') as f:
                common_profiles = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Warning: Could not read common profiles from {common_profiles_path}: {e}")
            # Continue with empty common_profiles list
    
    # Logic Part 1: If only one region has text
    non_empty_regions = [name for name, text in ocr_results.items() if text]
    if len(non_empty_regions) == 1:
        target_region = non_empty_regions[0]
        text = ocr_results[target_region]
        # Only attempt profile matching if we have common profiles
        if common_profiles:
            best_profile, _ = find_best_profile_match(text, common_profiles)
            return target_region, best_profile
        return target_region, text

    # Logic Part 2: If more than one region has text
    elif len(non_empty_regions) > 1:
        best_match = None
        highest_ratio = 0
        for region_name in non_empty_regions:
            text = ocr_results[region_name]
            profile, ratio = find_best_profile_match(text, common_profiles)
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = (region_name, profile)
        if best_match:
            return best_match[0], best_match[1]

    # Logic Part 3: If one region has proper capitalization
    for region_name in non_empty_regions:
        text = ocr_results[region_name]
        if text.istitle():
            return region_name, text

    # Logic Part 4: If still undetermined
    return None, 'UNDETERMINED'

    """
def remove_consecutive_profile_repeats(input_csv_path, output_csv_path=None):
    """
    processed_results = {}
    prev_data = None

    for timestamp in sorted(ocr_results.keys()):
        region_texts = ocr_results[timestamp]
        data = {}

        # Extract profile and region texts
        profile = region_texts.get('profile', 'undetermined')
        data['profile'] = profile

        any_text_found = False
        for name, text in region_texts.items():
            if name in ['profile', 'status']:
                continue
            if text:
                any_text_found = True
            data[name] = text

        # Skip if data is the same as previous
        if prev_data is not None:
            texts_match = all(
                data.get(name, '') == prev_data.get(name, '')
                for name in data.keys()
                if name != 'seconds' and name != 'timestamp'
            )
            if texts_match and data['profile'] == prev_data['profile']:
                continue  # Skip adding this data as it is a duplicate

        processed_results[timestamp] = data
        prev_data = data

    print(f"Condensed results contain {len(processed_results)} entries after removing duplicates.")
    return processed_results

    """
### VIDEO FUNCTIONS (1,662 tokens)
def extract_profiles_from_video(
    """
    if output_csv_path is None:
        output_csv_path = input_csv_path + '.temp'
        overwrite = True
    else:
        overwrite = False
        
    with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            
            previous_profile = None
            for row in reader:
                current_profile = row['profile']
                if current_profile != previous_profile:
                    writer.writerow(row)
                    previous_profile = current_profile
    
    if overwrite:
        os.replace(output_csv_path, input_csv_path)
        return input_csv_path
    
    return output_csv_path


    video_source,
    start_time_seconds=0,
    end_time_seconds=None,
    output_folder='data/0_gitignore',
    output_title='video_extracted_profiles',
    frame_interval=1,
    frame_similarity_threshold=0.95,
    regions={'LL': REGION_LL, 'C':  REGION_C, 'UR': REGION_UR},
    text_repeat_threshold=3,
    per_region_params=TC_PER_REGION_PARAMS,
    common_profiles_path=None
):
    """
def mrun_extract_profiles_from_video():
def apply_common_profiles_csv(profiles_csv_path, common_profiles_path):
    """
    from primary.fileops import convert_seconds_to_timestamp
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # If video_source is a URL, download it, otherwise use the provided file path
    if video_source.startswith(('http://', 'https://', 'www.')):
        video_file_path = download_video_from_youtube(video_source, output_title)
    else:
        video_file_path = video_source
    
    # Process frames and perform OCR without saving frames to disk
    ocr_results = extract_frames_and_perform_ocr(
        video_file_path,
        start_time_seconds=start_time_seconds,
        end_time_seconds=end_time_seconds,
        frame_interval=frame_interval,
        regions=regions,
        per_region_params=per_region_params,
        common_profiles_path=common_profiles_path  # Pass through the parameter
    )

    # Map time to OCR text and detail the results
    detailed_results = map_and_condense_ocr_results(ocr_results)

    # Save detailed results to CSV in output folder
    detailed_csv_path = os.path.join(output_folder, f'{output_title}_detailed.csv')
    with open(detailed_csv_path, 'w', newline='', encoding='utf-8') as detailed_csvfile:
        fieldnames = ['seconds', 'timestamp', 'profile'] + [f'ocr_text_region_{name}' for name in regions.keys()]
        writer = csv.DictWriter(detailed_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for timestamp_seconds, data in sorted(detailed_results.items()):
            timestamp = convert_seconds_to_timestamp(timestamp_seconds)
            row = {
                'seconds': timestamp_seconds,
                'timestamp': timestamp,
                'profile': data.get('profile', 'undetermined'),
            }
            for name in regions.keys():
                ocr_text = data.get(name, '')
                row[f'ocr_text_region_{name}'] = ocr_text
            writer.writerow(row)

    print(f"Detailed OCR text mapping saved to {detailed_csv_path}")

    # Create main version without consecutive profile repeats
    main_csv_path = os.path.join(output_folder, f'{output_title}.csv')
    main_csv_path = remove_consecutive_profile_repeats(detailed_csv_path, main_csv_path)
    print(f"Main OCR text mapping (without profile repeats) saved to {main_csv_path}")
    
    return main_csv_path
    pass
#if __name__ == "__main__":
    video_source = "data/0_gitignore/video_2024-10-30_PV-TC.mkv"
    start_time = 0*60
    end_time = 10*60 #None
    
    main_csv_path = extract_profiles_from_video(video_source, start_time, end_time)

    """
def mrun_apply_common_profiles_csv():
def extract_profiles_from_transcript_file(transcript_file_path, common_profiles_path):
    """
    # Read common profiles from file
    try:
        with open(common_profiles_path, 'r', encoding='utf-8') as f:
            common_profiles = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading common profiles from {common_profiles_path}: {e}")
        return

    # Read the profiles CSV and update profiles
    temp_csv_path = profiles_csv_path + '.temp'
    with open(profiles_csv_path, 'r', newline='', encoding='utf-8') as infile, \
         open(temp_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            original_profile = row['profile']
            best_match, _ = find_best_profile_match(original_profile, common_profiles, match_ratio_threshold=0.7)
            row['profile'] = best_match
            writer.writerow(row)

    # Replace the original CSV with the reprocessed one
    os.replace(temp_csv_path, profiles_csv_path)
    
    # Remove consecutive profile repeats
    remove_consecutive_profile_repeats(profiles_csv_path)
    print(f"  Apply common profiles CSV saved to {profiles_csv_path}")
    pass
#if __name__ == "__main__":
    profiles_csv_path = 'data/pv/meetings_tc_2024/2024-10-23_PV-TC_profiles.csv'
    common_profiles_path = 'data/pv/meetings_tc_2024/common_profiles_pv-tc.md'
    apply_common_profiles_csv(profiles_csv_path, common_profiles_path)

    """
def mrun_extract_profiles_from_transcript_file():
def process_folder_for_profiles(folder_path, common_profiles_path, apply_common_profiles_only=False):
    """
    from primary.fileops import read_metadata_field_from_file

    # Get the 'link' field from the metadata
    _, youtube_link = read_metadata_field_from_file(transcript_file_path, 'link')

    if not youtube_link:
        print(f"No 'link' field found in metadata of {transcript_file_path}")
        return

    # Call 'extract_profiles_from_video' with the YouTube link
    main_csv_path = extract_profiles_from_video(
        video_source=youtube_link,
        common_profiles_path=common_profiles_path  # Only pass non-default parameters
    )

    # Construct the new filename by replacing the suffix with '_profiles.csv'
    transcript_dir, transcript_filename = os.path.split(transcript_file_path)
    transcript_base = os.path.splitext(transcript_filename)[0]

    if '_' in transcript_base:
        parts = transcript_base.split('_')
        parts[-1] = 'profiles'
        new_base_name = '_'.join(parts)
    else:
        new_base_name = transcript_base + '_profiles'

    new_filename = new_base_name + '.csv'
    target_path = os.path.join(transcript_dir, new_filename)

    # Move and rename the main CSV file to the target path
    shutil.move(main_csv_path, target_path)

    print(f"Moved and renamed main CSV to {target_path}")
    pass
#if __name__ == "__main__":
    cur_transcript_file_path = 'data/pv/meetings_wpc/2022-03-01_PV-WPC_dgwhspm.md'
    common_profiles_path = 'data/pv/meetings_tc_2024/common_profiles_pv-tc.md'
    extract_profiles_from_transcript_file(cur_transcript_file_path, common_profiles_path)

    """
def mrun_process_folder_for_profiles():     

## primary/webflow_api.py (4,093 tokens)
### WEBFLOW SITES (13 tokens)
def mrun_print_site_info():
### WEBFLOW CMS (4,073 tokens)
def webflow_cms_get_collection_details(collection_id, debug=False, verbose=True):
    """
    from primary.fileops import sub_suffix_in_str, remove_all_suffixes_in_str, get_suffix
    
    if apply_common_profiles_only:
        # Get all markdown files and convert to profile CSV patterns
        md_files = glob.glob(os.path.join(folder_path, '*.md'))
        profile_csvs = []
        
        for md_file in sorted(md_files):
            base_with_profiles = sub_suffix_in_str(os.path.basename(md_file), '_profiles')
            profile_csv = os.path.splitext(base_with_profiles)[0] + '.csv'
            profile_csv_path = os.path.join(folder_path, profile_csv)
            if os.path.exists(profile_csv_path):
                profile_csvs.append(profile_csv_path)
        
        if profile_csvs:
            print(f"\nApplying common profiles to {len(profile_csvs)} existing CSV files:")
            for i, file in enumerate(sorted(profile_csvs), 1):
                print(f"  [{i}/{len(profile_csvs)}] {os.path.basename(file)}")
                apply_common_profiles_csv(file, common_profiles_path)
        else:
            print(f"No profile CSV files found in {folder_path}")
        return

    # Handle new profile extraction
    md_files = glob.glob(os.path.join(folder_path, '*.md'))
    files_to_extract = []
    
    # Define preferred suffix order
    preferred_suffixes = ['_pub', '_pubWIP', '_cemanual', '_cemanualRT', '_cemanualBA', '_cemanualWIP', '_spfix', '_spasgn']
    
    # Group files by their base name (excluding all suffixes)
    base_name_groups = {}
    for md_file in sorted(md_files):
        # Skip files with '_profiles' in the name
        if '_profiles' in md_file:
            continue
            
        # Get base filename without extension and remove all suffixes
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        base_name = remove_all_suffixes_in_str(base_name)
        
        # Add file to its base name group
        if base_name not in base_name_groups:
            base_name_groups[base_name] = []
        base_name_groups[base_name].append(md_file)
    
    files_to_extract = []
    # Select preferred file from each group
    for base_name, group_files in base_name_groups.items():
        selected_file = None
        
        # Try to find a file with preferred suffixes in order
        for suffix in preferred_suffixes:
            for file in group_files:
                file_base = os.path.splitext(os.path.basename(file))[0]
                if get_suffix(file_base) == suffix[1:]:  # Remove leading underscore for comparison
                    selected_file = file
                    break
            if selected_file:
                break
        
        # If no preferred suffix found, take the first file alphabetically
        if not selected_file:
            selected_file = sorted(group_files)[0]
        
        # Check if corresponding _profiles.csv exists
        base_with_profiles = sub_suffix_in_str(os.path.basename(selected_file), 'profiles')
        profile_csv = os.path.splitext(base_with_profiles)[0] + '.csv'
        profile_csv_path = os.path.join(folder_path, profile_csv)
        if not os.path.exists(profile_csv_path):
            files_to_extract.append(selected_file)
    
    if files_to_extract:
        print(f"\nFound {len(files_to_extract)} files needing profile extraction:")
        for file in files_to_extract:
            print(f"  {os.path.basename(file)}")
        
        for i, file_path in enumerate(files_to_extract, 1):
            print(f"\nProcessing file {i}/{len(files_to_extract)}: {os.path.basename(file_path)}")
            extract_profiles_from_transcript_file(file_path, common_profiles_path)
    else:
        print(f"No files found needing profile extraction in {folder_path}")
    pass
if __name__ == "__main__":
    folder_path = 'data/pv/meetings_tc_2023'
    common_profiles_path = 'data/pv/meetings_tc_2024/common_profiles_pv-tc.md'
    process_folder_for_profiles(folder_path, common_profiles_path, apply_common_profiles_only=False)


#url = 'https://youtu.be/BuUAVFFfKD8'  # 2024-10-14 ASCC 24min
#url = 'https://youtu.be/hVf8v_64MVk'  # 2022-03-01 WPC


    # Example usage:
    # Assuming you have a function to extract frames and regions
    # For each frame in the video between start_time and end_time:
    #     for region_name, coords in regions.items():
    #         region_image = extract_region(frame, coords)
    #         params = per_region_params.get(region_name, {})
    #         # Check for detection_threshold
    #         detection_threshold = params.get('detection_threshold')
    #         if detection_threshold is not None:
    #             if not is_white_text_on_black_background(region_image, detection_threshold):
    #                 # Skip OCR for this region
    #                 ocr_results[region_name] = ''
    #                 continue
    #         # Perform OCR
    #         mode = params.get('mode', 'binary')
    #         binary_threshold = params.get('binary_threshold')
    #         text = perform_ocr_on_region(region_image, mode=mode, binary_threshold=binary_threshold)
    #         ocr_results[region_name] = text

#===== END OF FILE primary/video.py =====




#===== START OF FILE secondary/webflow.py =====
#Library of functions and execution code to do Webflow tasks

import os
from dotenv import load_dotenv
import markdown
from webflow.client import Webflow
import requests

from primary.fileops import *

#---API KEYS AND SECRETS---
load_dotenv(override=True)  # Load environment variables from .env file
WEBFLOW_API_KEY_FOF_ALL = os.environ["WEBFLOW_API_KEY_FOF_ALL"]

#---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

#Initialize the Webflow API client
client = Webflow(access_token=WEBFLOW_API_KEY_FOF_ALL)

SITE_ID_FOF = "66f32336260d050c6e0fffa0"
    pass
#if __name__ == "__main__":
    cur_site_id = SITE_ID_FOF
    site_info = client.sites.get(site_id=cur_site_id)
    print(f"Site Info for site_id: {cur_site_id}")
    print(f"ID: {site_info.id}")
    print(f"Workspace ID: {site_info.workspace_id}")
    print(f"Created On: {site_info.created_on}")
    print(f"Display Name: {site_info.display_name}")
    print(f"Short Name: {site_info.short_name}")
    print(f"Last Published: {site_info.last_published}")
    print(f"Last Updated: {site_info.last_updated}")
    print(f"Preview URL: {site_info.preview_url}")
    print(f"Time Zone: {site_info.time_zone}")
    print(f"Custom Domains: {site_info.custom_domains}")

DEUTSCH_INTERVIEWS_VRBS_ID = "6711b684a9e995b7c0f06e17"
FDA_C19_TOWNHALLS_ID = "6780532037b7b191793c3544"

    """
def mrun_get_collection_details():
def webflow_cms_import_heading(collection_id, file_path, heading):
    """
    try:
        # Construct the URL
        url = f"https://api.webflow.com/v2/collections/{collection_id}"
        
        # Set up headers
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        
        if debug: 
            print("Raw API response:")
            print(f"Status Code: {response.status_code}")
            print("Headers:")
            print(response.headers)
            print("Content:")
            print(response.text)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        collection_details = {
            "id": data.get("id"),
            "name": data.get("displayName"),
            "slug": data.get("slug"),
            "singularName": data.get("singularName"),
            "fields": data.get("fields", []),
            "createdOn": data.get("createdOn"),
            "lastUpdated": data.get("lastUpdated")
        }

        if verbose:
            print(f"Collection Details for {collection_details['name']}:")
            for key, value in collection_details.items():
                if key != "fields":
                    print(f"{key}: {value}")
                else:
                    filtered_fields = [f for f in value if f.get('slug') not in ['name', 'slug']]
                    print(f"Number of fields: {len(filtered_fields)}")
                    print("Fields:")
                    # Print header row
                    print(f"{'Field Name':<25} {'Type':<15} {'Status':<15} {'Slug'}")
                    print("-" * 80)  # Separator line
                    for field in filtered_fields:
                        field_type = field.get('type', 'Unknown')
                        field_name = field.get('displayName', 'Unnamed')
                        field_slug = field.get('slug', 'no-slug')
                        field_required = "Required" if field.get('isRequired') else "Optional"
                        print(f"\033[33m{field_name:<25}\033[0m {field_type:<15} {field_required:<15} {field_slug}")
                    print("-" * 80)  # Separator line

        return collection_details
    except requests.exceptions.RequestException as e:
        print(f"Error fetching collection details: {str(e)}")
        return None

    pass
#if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    collection_details = webflow_cms_get_collection_details(cur_collection_id, verbose=True)

    """
def webflow_cms_list_items(collection_id, include_archived=True, verbose=False):
    """
    # Get the markdown content for the specified heading
    markdown_text = get_heading(file_path, heading)

    if markdown_text is None:
        print(f"Heading '{heading}' not found in file '{file_path}'")
        return None

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text)

    # Create a title for the item based on the heading
    item_title = os.path.splitext(os.path.basename(file_path))[0] + '_' + heading.strip('#').strip()
    item_slug = item_title.lower().replace(' ', '-')

    new_item = {
        'fields': {
            'name': item_title,  # Required name field
            'slug': item_slug,   # Required slug field
            'transcript-vrb': html_content  # This is your custom rich text field
        }
    }

    # Create the item in the Webflow collection
    created_item = client.collections.create_item(collection_id=collection_id, data=new_item)
    print(f"Created new item with ID: {created_item['_id']}")

    return created_item['_id']

    """
def mrun_webflow_cms_list_items():
def webflow_cms_import_transcript_and_qa(collection_id, transcript_file_path, qa_suffix='_qa-qonly', verbose=False):
    """
    try:
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        url = f'https://api.webflow.com/v2/collections/{collection_id}/items'
        if include_archived:
            url += '?archived=true'
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            items = response.json()['items']
            if verbose:
                for item in items:
                    archived_status = " (ARCHIVED)" if item.get('archived', False) else ""
                    print(f"ID: {item['id']}, Name: {item['fieldData'].get('name', 'N/A')}, "
                          f"Slug: {item['fieldData'].get('slug', 'N/A')}{archived_status}")
                print(f"\nTotal items: {len(items)}")
            return items
        else:
            if verbose:
                print(colored(f"Error listing items. Status code: {response.status_code}", "red"))
                print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        if verbose:
            print(colored(f"Error listing items: {str(e)}", "red"))
        return None
    pass
if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    items = webflow_cms_list_items(cur_collection_id, verbose=True)

    """
def mrun_webflow_cms_import_transcript_and_qa():
def webflow_cms_create_item(collection_id, field_data, collection_validation=True, verbose=False):
    """
    # Get URLs and transcript text - extract just the URL string if it's a tuple
    pdf_url = read_metadata_field_from_file(transcript_file_path, 'link pdf')
    pdf_url = pdf_url[1] if isinstance(pdf_url, tuple) else pdf_url
    
    youtube_url = read_metadata_field_from_file(transcript_file_path, 'link youtube')
    youtube_url = youtube_url[1] if isinstance(youtube_url, tuple) else youtube_url
    
    #transcript_text = get_heading(transcript_file_path, '### transcript')
    transcript_text = 'This is dummy transcript text'
    
    if transcript_text is None:
        print(f"Transcript not found in file '{transcript_file_path}'")
        return None

    # Create a title and slug from the filename
    item_title = os.path.splitext(os.path.basename(transcript_file_path))[0]
    item_slug = item_title.lower().replace(' ', '-')

    # Restructure the data format to match v2 API requirements
    new_item = {
        'fieldData': {
            'name': item_title,
            'slug': item_slug,
            'md-mod-txt': transcript_text,
            'pdf-url': pdf_url if pdf_url else '',
            'youtube-url-3': youtube_url if youtube_url else ''
        }
    }

    if verbose:
        print("\nField values (truncated to 100 chars):")
        for field, value in new_item['fieldData'].items():
            truncated_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"{field}: {truncated_value}")

    try:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        # The v2 API expects a wrapper object with 'items' array
        request_body = {
            'items': [new_item]
        }
        
        response = requests.post(
            f'https://api.webflow.com/v2/collections/{collection_id}/items',
            headers=headers,
            json=request_body
        )
        
        if response.status_code == 200:
            created_item = response.json()
            print(f"Created new item with ID: {created_item['id']}")
            return created_item['id']
        else:
            print(f"Error creating item. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error creating item: {str(e)}")
        return None
    pass
#if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    transcript_file_path = 'data/floodlamp/reg/fda-townhalls/f5_fixnames/done_auto/2020-12-09_Virtual Town Hall 36_fixnames.md'
    webflow_cms_import_transcript_and_qa(cur_collection_id, transcript_file_path, verbose=True)
    """
def mtest_webflow_cms_create_item():
def webflow_cms_update_item(collection_id, item_id, field_data, collection_validation=True, verbose=False):
    """
    # Get collection details and validate fields only if collection_validation is True
    if collection_validation:
        collection_details = webflow_cms_get_collection_details(collection_id, verbose=False)
        if not collection_details:
            print("Failed to fetch collection details for validation")
            return None

        # Extract required fields from collection schema
        required_fields = {
            field.get('slug'): field.get('type') 
            for field in collection_details['fields'] 
            if field.get('isRequired')
        }
        
        # Validate required fields
        missing_fields = [field for field in required_fields.keys() if field not in field_data]
        if missing_fields:
            print(f"Error: Missing required fields: {', '.join(missing_fields)}")
            return None

    if verbose:
        print("\nField values (truncated to 100 chars):")
        for field, value in field_data.items():
            truncated_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"{field}: {truncated_value}")

    # Prepare request data
    new_item = {
        'fieldData': field_data
    }
    
    request_body = {
        'items': [new_item]
    }

    try:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        response = requests.post(
            f'https://api.webflow.com/v2/collections/{collection_id}/items',
            headers=headers,
            json=request_body
        )
        
        if response.status_code in [200, 202]:
            created_item = response.json()
            if verbose:
                print(colored(f"Successfully created item name: {created_item['items'][0]['fieldData']['name']}  ID: {created_item['items'][0]['id']}", "green"))
            return created_item['items'][0]['id']
        else:
            print(colored(f"Error creating item. Status code: {response.status_code}", "red"))
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(colored(f"Error creating item: {str(e)}", "red"))
        return None
    pass
#if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    field_data = {
        'name': 'Test Item',
        'slug': 'test-item',
        'md-mod-txt': 'This is a test item',
        'pdf-url': 'https://example.com/test.pdf',
        'youtube-url-3': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    }
    webflow_cms_create_item(cur_collection_id, field_data, collection_validation=False, verbose=True)
    """

## primary/dbgen.py (2,700 tokens)
### EXCHANGES SQLITE DB (2,694 tokens)
def create_exchanges_db(db_path):
    """
    if collection_validation:
        collection_details = webflow_cms_get_collection_details(collection_id, verbose=False)
        if not collection_details:
            print("Failed to fetch collection details for validation")
            return False

    try:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        request_body = {
            "fieldData": field_data
        }
        
        response = requests.patch(
            f'https://api.webflow.com/v2/collections/{collection_id}/items/{item_id}',
            headers=headers,
            json=request_body
        )
        
        if response.status_code in [200, 202]:
            if verbose:
                print(f"Successfully updated item with ID: {item_id}")
            return True
        else:
            if verbose:
                print(f"Error updating item. Status code: {response.status_code}")
                print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        if verbose:
            print(f"Error updating item: {str(e)}")
        return False


#===== END OF FILE secondary/webflow.py =====




#===== START OF FILE primary/dbgen.py =====
#Library of functions and execution code to generate databases

import os
import json
import sqlite3
import csv
import re


    """
def mtest_create_exchanges_db():
def index_exchanges_in_db(root_folder, exclude_subfolders=None):
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
    db_path = 'exchanges.db'
    create_exchanges_db(db_path)

    """
def mtest_index_exchanges_in_db():
def view_all_exchanges(db_path):
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
    root_folder = 'exchanges/deutsch_qrag'  # Replace with your root folder
    exclude_subfolders = None  # ['not-reviewed']
    db_path = index_exchanges_in_db(root_folder, exclude_subfolders)
    print(f"SQLite database created at: {db_path}")

    """
def mtest_view_all_exchanges():
def copy_exchanges_db_with_pii_add_column(exchanges_db_path):
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
    db_path = 'exchanges/deutsch_qrag/exchanges.db'
    view_all_exchanges(db_path)

    """
def copy_exchanges_db_with_user_pii(exchanges_db_path, users_csv_path):
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

    """
def add_users_table_to_db(cursor, users_csv_path):
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

#get users csv file by downloading from Webflow
    """
def add_username_column_to_exchanges(cursor):
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

    """
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
def add_hmac_user_id_to_users_csv(users_csv_path):
        """)
        print(f"Updated {cursor.rowcount} rows in the exchanges table.")

        # Debug: Check contents of exchanges table after update
        cursor.execute("SELECT hmac_user_id, user_name FROM exchanges LIMIT 5")
        print("Sample data from exchanges table after update:")
        for row in cursor.fetchall():
            print(row)

    except sqlite3.Error as e:
        print(f"SQLite error while adding or updating user_name column: {e}")

    """
def run_mtests_exchanges():