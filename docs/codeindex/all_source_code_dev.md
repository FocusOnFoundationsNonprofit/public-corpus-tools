all_source_code (86,016 tokens)

## primary/fileops.py (19,406 tokens)
#Library of functions and execution code to do support tasks on files
import os
import glob
import csv
import re
import inspect
from datetime import datetime
import pytz
import time
import shutil
import json
import inspect
from termcolor import colored
import warnings

#Naming Conventions - see Coding Log - 2024 gdoc for WIP version
#https://docs.google.com/document/d/1y2zuy5L15b_9KCleT1Fcw31q6yyWz-F7czJLVC0h678/edit?usp=sharing

### INITIAL (434 tokens)
def custom_formatwarning(msg, category, filename, lineno, line=None):
    """
    DO NOT CALL - only used to define the custom format
    """
    return f"{category.__name__}: {msg}\n"
#Set the warnings format to use the custom format
warnings.formatwarning = custom_formatwarning
#USAGE: warnings.warn(f"Insert warning message here") 
def verbose_print(verbose, *messages):
    """
    Helper function to pass on bool verbose and make verbose printing cleaner
    
    :param verbose: boolean for whether to print the messages.
    :param messages: tuple of variable-length argument list.
    :return: None
    """
    if not isinstance(verbose, bool):
        raise TypeError("The first parameter 'verbose' must be of type bool.")
    if not messages:
        raise ValueError("At least one message must be provided.")
    if verbose:
        print(*messages)
def check_file_exists(file_path, operation_name):
    """
    Checks file existence and raises a ValueError if not found, which stops execution.

    :param file_path: string of file path which can be absolute or relative.
    :param operation_name: string of the message that the ValueError will print, typically the function name - optional message.
    :return: bool, True if file exists, False otherwise.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"VALUE ERROR in {operation_name}: input file does not exist for {file_path}")
    return True
def warn_file_overwrite(file_path):
    """
    Checks if a file already exists and issues a warning if it does.

    :param file_path: string representing the path of the file to be checked.
    :return: bool, True if file exists, False otherwise.
    """
    # Get the name of the calling function
    func_name = inspect.currentframe().f_back.f_code.co_name
    if os.path.isfile(file_path):
        warnings.warn(f"The function: {func_name} is overwriting a file that already exists, file: '{file_path}'")
        return True
    return False

### SUFFIX (1,989 tokens)
def get_suffix(file_str, delimiter='_'):
    """
    Extracts the suffix from a given file string based on a specified delimiter.

    :param file_str: string of the file name from which to extract the suffix.
    :param delimiter: string representing the delimiter used to separate the suffix from the rest of the file string. Default is "_".
    :return: string of the extracted suffix or None if no valid suffix is found.
    """
    # Count the occurrences of the file extension delimiter (.) only in the end portion of the string before a '/'
    file_base = os.path.basename(file_str)
    period_count = file_base.count('.')
    # Throw a ValueError if there's more than one period
    if period_count > 1:
        raise ValueError("in get_suffix: More than one period found in the input file string.")

    # Find the last occurrence of the delimiter
    delimiter_index = file_base.rfind(delimiter)
    # Find the last occurrence of the file extension delimiter (.)
    extension_index = file_base.rfind('.')

    # Check if the delimiter is found and before the extension, or if there is no extension
    if delimiter_index != -1 and (extension_index == -1 or delimiter_index < extension_index):
        # Check if the part of the file string preceding the delimiter is a date in the format 'YYYY-MM-DD'
        preceding_str = file_base[:delimiter_index]
        #print(f"DEBUG preceeding_str: {preceding_str}")
        if re.match(r'\d{4}-\d{2}-\d{2}$', preceding_str):
            return None  # Return None if the preceding part is a date

        # Extract and return the suffix including the delimiter
        suffix_end_index = extension_index if extension_index != -1 else len(file_base)
        suffix = file_base[delimiter_index:suffix_end_index]
        # Throw a ValueError if the extracted suffix contains invalid characters
        if not all(char.isalnum() or char == '-' for char in suffix.strip(delimiter)):
            # Return None if the extracted suffix contains a space
            if ' ' in suffix:
                return None
            else:
                raise ValueError("in get_suffix: The extracted suffix contains invalid characters.")

        return suffix
    else:
        return None
def add_suffix_in_str(file_str, suffix_add):
    """
    Adds a suffix to a given file string.

    :param file_str: string of the file name to which the suffix will be added.
    :param suffix_add: string of the suffix to be added to the file string.
    :return: string of the file name with the added suffix.
    """
    # Find the last occurrence of the file extension delimiter (.)
    extension_index = file_str.rfind('.')
    
    # If there is no extension, append the suffix to the end of the string
    if extension_index == -1:
        return file_str + suffix_add
    
    # Insert the suffix and delimiter before the extension
    return file_str[:extension_index] + suffix_add + file_str[extension_index:]
def sub_suffix_in_str(file_str, suffix_sub, delimiter='_'):
    """
    Replaces the existing suffix in a file string with a new suffix.

    :param file_str: string of the file name from which to replace the suffix.
    :param suffix_sub: string of the new suffix to replace the existing one.
    :param delimiter: string representing the delimiter used to separate the suffix from the rest of the file string. Default is "_".
    :return: string of the file name with the replaced suffix or the original file string if no valid suffix is found.
    """
    # Use the get_suffix function to determine if there is a valid suffix
    existing_suffix = get_suffix(file_str, delimiter)
    
    # Find the last occurrence of the file extension delimiter (.)
    extension_index = file_str.rfind('.')
    
    # If there is an existing valid suffix, replace it with the new suffix
    if existing_suffix is not None:
        suffix_start_index = file_str.rfind(existing_suffix)
        return file_str[:suffix_start_index] + suffix_sub + file_str[extension_index:]
    else:
        # If no existing suffix, add the new suffix before the extension
        if extension_index != -1:
            return file_str[:extension_index] + suffix_sub + file_str[extension_index:]
        else:
            # If no extension, just append the new suffix
            return file_str + suffix_sub
def remove_all_suffixes_in_str(file_str, delimiter='_'): # DS, cat 1, unitests 7 - no mock
    """
    Removes all suffixes from a given file string based on a specified delimiter while retaining the original file extension.

    :param file_str: string of the file name from which to remove all suffixes.
    :param delimiter: string representing the delimiter used to separate the suffixes from the rest of the file string. Default is "_".
    :return: string of the file name with all suffixes removed but with the original extension preserved.
    """
    # Find the last occurrence of the file extension delimiter (.)
    extension_index = file_str.rfind('.')
    # Extract the extension if it exists
    extension = file_str[extension_index:] if extension_index != -1 else ''
    
    # Remove the extension from the file string to avoid removing it as a suffix
    file_str_without_extension = file_str[:extension_index] if extension_index != -1 else file_str
    
    # Continuously strip suffixes until no more can be stripped
    while True:
        # Use get_suffix to get the current suffix
        current_suffix = get_suffix(file_str_without_extension, delimiter)
        # If there is a suffix, remove it
        if current_suffix:
            # Find the index of the suffix to be removed
            suffix_index = file_str_without_extension.rfind(current_suffix)
            # Update file_str_without_extension by removing the current suffix
            file_str_without_extension = file_str_without_extension[:suffix_index].rstrip(delimiter)
        else:
            # If no more suffixes, break out of the loop
            break

    # Reattach the original extension to the file string
    return file_str_without_extension + extension
def copy_file_and_append_suffix(file_path, suffix_new):
    """
    Copies the file with a new suffix added before the file extension.

    :param file_path: string of the path to the original file.
    :param suffix_new: string of the suffix to be appended to the original filename before the file extension.
    :return: string of the path to the newly created file with the new suffix.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")

    # Split the file path into directory, base name, and extension
    file_dir, file_base = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_base)

    # Create the new file path with the suffix added before the file extension
    new_file_base = f"{file_name}{suffix_new}{file_ext}"
    new_file_path = os.path.join(file_dir, new_file_base)

    # Copy the original file to the new file path
    shutil.copy(file_path, new_file_path)

    return new_file_path
def sub_suffix_in_file(file_path, suffix_new):
    """
    Substitutes the suffix in the file name of the given file path with a new suffix.
    If new_suffix is empty '' then it will remove the last suffix of the file.

    :param file_path: string, the path to the original file.
    :param suffix_new: string, the new suffix to replace the existing one in the file name.
    :return: string, the path to the newly created file with the substituted suffix.
    """
    # Check if the original file exists
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")

    # Split the file path into directory, base name, and extension
    file_dir, file_base = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_base)

    # Substitute the suffix in the file name using the sub_suffix_in_str function
    new_file_base = sub_suffix_in_str(file_name + file_ext, suffix_new)
    new_file_path = os.path.join(file_dir, new_file_base)

    # Rename the original file to the new file path
    os.rename(file_path, new_file_path)

    return new_file_path
def count_suffixes_in_folder(folder_path):
    """
    Analyzes all the files in the specified folder and prints the number of files for each unique suffix, alphabetized.

    :param folder_path: string of the folder path to search for files and analyze suffixes.
    :return: None. The function prints the suffixes and their counts.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"The directory does not exist: {folder_path}")

    suffix_counts = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            suffix = get_suffix(file_name)
            if suffix:
                suffix_counts[suffix] = suffix_counts.get(suffix, 0) + 1

    # Sort the suffixes alphabetically and print the counts
    for suffix in sorted(suffix_counts):
        print(f"SUFFIX COUNT for {suffix}: {suffix_counts[suffix]}")

### FOLDER (884 tokens)
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
    if not os.path.isdir(folder_path):
        raise ValueError(f"VALUE ERROR in get_files_in_folder: folder does not exist.")
    if suffixpat_include is not None and suffixpat_exclude is not None:
        raise ValueError("Both suffixpat_include and suffixpat_exclude are provided.")
    
    all_file_paths = []
    if include_subfolders:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                all_file_paths.append(os.path.join(root, file))
    else:
        all_file_paths = glob.glob(os.path.join(folder_path, "*"))

    filtered_file_paths = []
    for file_path in all_file_paths:
        if os.path.isfile(file_path):
            # Suffix pattern handling
            if suffixpat_include:
                if '.' in suffixpat_include:
                    if not file_path.endswith(suffixpat_include):
                        continue
                else:
                    file_suffix = get_suffix(file_path)
                    if file_suffix != suffixpat_include:
                        continue
            if suffixpat_exclude:
                if '.' in suffixpat_exclude:
                    if file_path.endswith(suffixpat_exclude):
                        continue
                else:
                    file_suffix = get_suffix(file_path)
                    if file_suffix == suffixpat_exclude:
                        continue
            filtered_file_paths.append(file_path)
    
    filtered_file_paths.sort()
    return filtered_file_paths
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
    verbose_print(verbose, f"\nRUNNING apply_to_folder with {worker_function}", f"FOLDER: {folder_path}")

    # Call get_files_in_folder to retrieve the list of files - it handles errors
    file_paths = get_files_in_folder(folder_path, suffixpat_include=suffixpat_include, suffixpat_exclude=suffixpat_exclude, include_subfolders=include_subfolders)
    file_paths.sort()
    verbose_print(verbose, f"NUMBER OF FILES RUN with apply_to_folder: {len(file_paths)}")
    
    results = {}  # Dictionary to store file names and function return values
    for file_path in file_paths:
        try:
            result = worker_function(file_path, *args, verbose=verbose, **kwargs)  # Try passing verbose
        except TypeError:
            result = worker_function(file_path, *args, **kwargs)  # Fallback if verbose is not accepted
        results[file_path] = result

    return results

### READ WRITE (2,332 tokens)
def read_complete_text(file_path):
    """
    Reads the entire text from a file.

    :param file_path: string of the file path which can be absolute or relative.
    :return: string of the complete text read from the file.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")
    
    with open(file_path, 'r') as file:
        complete_text = file.read()
    return complete_text
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
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")
    with open(file_path, 'r') as file:
        complete_text = file.read()

    # Check for Format 1: ## metadata and ## content
    metadata_start = complete_text.find('## metadata')
    content_start = complete_text.find('## content')
    
    if metadata_start != -1 and content_start != -1:
        metadata = complete_text[metadata_start:content_start].strip()
        content = complete_text[content_start:].strip()
    else:
        # Check for Format 2: METADATA and CONTENT
        metadata_start = complete_text.find('METADATA')
        content_start = complete_text.find('CONTENT')
        
        if metadata_start != -1 and content_start != -1:
            metadata = complete_text[metadata_start + len('METADATA'):content_start].strip()
            content = complete_text[content_start:].strip()
        else:
            raise ValueError(f"File does not contain both metadata and content sections in the required format.\n{file_path}")

    return metadata.rstrip('\n'), content
def read_file_flex(file_path):
    """
    Reads the text from a file and splits it into the metadata and content sections if present.
    If no metadata is found, returns (None, complete_text).

    :param file_path: string of the file path which can be absolute or relative.
    :return: tuple, the metadata and content as two separate strings. If no metadata, returns (None, complete_text).
    """
    complete_text = read_complete_text(file_path)

    try:
        metadata, content = read_metadata_and_content(file_path)
        return metadata, content
    except ValueError:
        # If read_metadata_and_content raises a ValueError, it means no metadata was found
        return None, complete_text.strip()
''' Overwrite Logic Table:
Overwrite   Prompt
Argument    Response    Output Files	    Case Description
no          NA	        _orig + _orig_new	Keep both
no-sub	    NA	        _orig + _new	    Keep both and substitute suffix in new file
replace	    NA	        _orig_new	        Replace orig file
replace-sub	NA	        _new	            Replace orig file with new and substitute suffix in new file
yes	        NA	        _orig	            Overwrite without prompt
prompt      y/yes       _orig	            Prompt=Y to overwrite
prompt      n/no        _orig + _orig_new	Prompt= N to keep both
prompt	    s/sub	    _orig + _new	    Prompt=S to keep both and substitute suffix in new file
prompt	    x/anyother  re-prompt
x/anyother  ValueError
'''
def handle_overwrite_prompt(file_path, file_path_opfunc, verbose=True):
    """
    Handles user prompt for overwriting a file.

    :param file_path: string of the original file path.
    :param file_path_opfunc: string of the new file path.
    :param verbose: boolean for whether to print verbose messages. Default is True.
    :return: string of the path to the file that was kept.
    """
    # Check if both files exist before proceeding
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")
    if not os.path.isfile(file_path_opfunc):
        raise ValueError(f"The file path does not exist or is invalid for {file_path_opfunc}.")
    
    
    while True:
        user_input = input(f"Do you want to overwrite? [Y/yes, N/no, S/sub (substitute suffix)]: ").strip().lower()
        if user_input.startswith("y"):
            verbose_print(verbose, "File operation with overwrite=prompt+yes - overwrite original file.")
            os.remove(file_path)
            os.rename(file_path_opfunc, file_path)
            return file_path
        elif user_input.startswith("n"):
            verbose_print(verbose, f"File operation with overwrite=prompt+no - keep original file and new file.")
            return file_path_opfunc
        elif user_input.startswith("s"):
            verbose_print(verbose, f"File operation with overwrite=prompt+sub - keep original file and new file with substituted suffix.")
            file_path_sub = sub_suffix_in_str(file_path, get_suffix(file_path_opfunc, "_"), delimiter='_')
            os.rename(file_path_opfunc, file_path_sub)
            return file_path_sub
        else:
            print("Invalid input. Please enter 'Y' for yes, 'N' for no, or 'S' to substitute suffix.")
def manage_file_overwrite(original_path, suffix_new, overwrite, verbose=False):
    """
    Handle file overwriting based on the specified mode.
    
    :param original_path: string, the path to the original file.
    :param suffix_new: string, the suffix to be appended to the original filename for the new file.
    :param overwrite: string, the overwrite mode ('no', 'no-sub', 'replace', 'replace-sub', 'yes', 'prompt').
    :param verbose: boolean, whether to print verbose messages.
    :return: string, the final path of the file after applying overwrite logic.
    """
    new_path = add_suffix_in_str(original_path, suffix_new)
    
    if overwrite == "no":
        verbose_print(verbose, f"manage_file_overwrite in mode: '{overwrite}' - Keeping both original and new files.")
        return new_path
    elif overwrite == "no-sub":
        verbose_print(verbose, f"manage_file_overwrite in mode: '{overwrite}' - Keeping both files and substituting suffix in new file.")
        final_path = sub_suffix_in_str(original_path, suffix_new)
        os.rename(new_path, final_path)
        return final_path
    elif overwrite == "replace":
        verbose_print(verbose, f"manage_file_overwrite in mode: '{overwrite}' - Replacing original file with new file.")
        if os.path.exists(original_path):
            os.remove(original_path)
        os.rename(new_path, original_path)
        return original_path
    elif overwrite == "replace-sub":
        verbose_print(verbose, f"manage_file_overwrite in mode: '{overwrite}' - Replacing original file with new file and substituting suffix.")
        if os.path.exists(original_path):
            os.remove(original_path)
        final_path = sub_suffix_in_str(original_path, suffix_new)
        os.rename(new_path, final_path)
        return final_path
    elif overwrite == "yes":
        verbose_print(verbose, f"manage_file_overwrite in mode: '{overwrite}' - Overwriting original file.")
        if os.path.exists(original_path):
            os.remove(original_path)
        os.rename(new_path, original_path)
        return original_path
    elif overwrite == "prompt":
        verbose_print(verbose, f"manage_file_overwrite in mode: '{overwrite}' - Prompting user.")
        return handle_overwrite_prompt(original_path, new_path, verbose)
    else:
        raise ValueError(f"Invalid overwrite mode: {overwrite}")
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
    # Add suffix to create new file path
    new_file_path = add_suffix_in_str(file_path, suffix_new)
    if verbose:
        if os.path.isfile(new_file_path):
            print(f"BEFORE OVERWRITE write_complete_text new_file_path does exist.")
            warn_file_overwrite(new_file_path)
        else:
            print(f"BEFORE OVERWRITE write_complete_text new_file_path does NOT exist (note this file may be an intermediate file that is deleted or renamed by manage_file_overwrite).")
            
    # Write the complete text to the new file
    with open(new_file_path, "w") as file:
        file.write(complete_text)

    # Manage file overwrite
    final_file_path = manage_file_overwrite(file_path, suffix_new, overwrite, verbose)

    return final_file_path
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
    if metadata is not None:
        # If metadata is present (even if it's an empty string), include it with two blank lines between metadata and content
        complete_text = metadata.rstrip('\n') + '\n\n\n' + content.rstrip('\n') + '\n'
    else:
        # If metadata is None, just write the content
        complete_text = content.rstrip('\n') + '\n'

    return write_complete_text(file_path, complete_text, suffix_new, overwrite, verbose)
### JSON (828 tokens)
def pretty_print_json_structure(json_file_path, level_limit=None, save_to_file=False):
    """
    Prints the structure of a JSON file and optionally saves it to a file with a '.pretty' extension.

    :param json_file_path: string of the path to the json file.
    :param level_limit: integer of the maximum level of nesting to print. None means no limit.
    :param save_to_file: boolean indicating whether to save the output to a file. defaults to true.
    :return: None.
    """
    # Define colors for different levels of JSON structure with high contrast
    colors = ['green', 'blue', 'red', 'magenta', 'yellow', 'white', 'grey']
    output_lines = []

    if not os.path.exists(json_file_path):
        warnings.warn(f"File {json_file_path} does not exist.")
        return

    def print_json_structure(data, indent=0, parent_key='', level=0):
        # Stop printing if the current level exceeds the level limit
        if level_limit is not None and level > level_limit:
            return

        # Select color based on the current level, cycling through the colors list
        color = colors[level % len(colors)]

        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    # Print list information with the selected color
                    line = ' ' * indent + f"{key} (list of {len(data[key])} items)"
                    print(colored(line, color))
                    output_lines.append(line)
                    if data[key]:
                        print_json_structure(data[key][0], indent + 4, key, level + 1)
                else:
                    # Print dictionary keys with the selected color
                    line = ' ' * indent + str(key)
                    print(colored(line, color))
                    output_lines.append(line)
                    print_json_structure(data[key], indent + 4, key, level + 1)
        elif isinstance(data, list) and parent_key != '':
            if data:
                print_json_structure(data[0], indent, parent_key, level)

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        print_json_structure(data)

    if save_to_file:
        output_file_path = json_file_path + '.pretty'
        with open(output_file_path, 'w') as output_file:
            for line in output_lines:
                output_file.write(line + '\n')
        print(f"Saved pretty printed JSON structure to {output_file_path}")
def write_json_file_from_object(json_object, file_path, overwrite="no"):
    """ 
    Writes a JSON object to a file at the specified path.

    :param json_object: dictionary or list to be written as JSON.
    :param file_path: string of the path where the JSON file will be written.
    :param overwrite: string of either "yes" or "no" to determine if existing files should be overwritten. default is "no".
    :return: None.
    """
    if overwrite not in ["yes", "no"]:
        raise ValueError("The 'overwrite' parameter must be 'yes' or 'no'.")

    if overwrite == "no" and os.path.exists(file_path):
        raise FileExistsError(f"The file {file_path} already exists and will not be overwritten.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as json_file:
        json.dump(json_object, json_file, indent=4)
def read_json_object_from_file(file_path):  # consider moving to fileops
    """ 
    Reads a JSON object from a file at the specified path.

    :param file_path: string of the path to the JSON file to be read.
    :return: dictionary or list representing the JSON object read from the file.
    """
    with open(file_path, 'r') as json_file:
        json_object = json.load(json_file)
    return json_object

### MISC FILE (2,974 tokens)
def rename_file(file_path, new_filebase):
    """
    Renames the file base portion for the file given at the argument file path.

    :param file_path: string, the path to the file to be renamed.
    :param new_filebase: string, the new base name for the file without the extension.
    :return: string, the new file path after renaming, or an error if the operation fails.
    """
    # Check if the original file exists and is valid
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")

    # Split the file path into directory, base name, and extension
    file_dir, file_base = os.path.split(file_path)
    file_ext = os.path.splitext(file_base)[1]

    # Create the new file path with the new file base
    new_file_path = os.path.join(file_dir, new_filebase + file_ext)

    # Rename the original file to the new file path
    try:
        os.rename(file_path, new_file_path)
        return new_file_path  # Return the new file path if the file was successfully renamed
    except OSError as e:
        return e  # Return the exception if an error occurred
def rename_file_extension(file_path, new_extension):
    """
    Renames the file extension for the file given at the argument file path.

    :param file_path: string, the path to the file to be renamed.
    :param new_extension: string, the new extension for the file (including the dot).
    :return: string, the new file path after renaming, or an error if the operation fails.
    """
    # Check if the original file exists and is valid
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")

    # Split the file path into directory, base name, and extension
    file_dir, file_base = os.path.split(file_path)
    file_name = os.path.splitext(file_base)[0]

    # Create the new file path with the new extension
    new_file_path = os.path.join(file_dir, file_name + new_extension)

    # Rename the original file to the new file path
    try:
        os.rename(file_path, new_file_path)
        return new_file_path  # Return the new file path if the file was successfully renamed
    except OSError as e:
        return e  # Return the exception if an error occurred
def delete_file(file_path):
    """
    Deletes a file at the specified file path.

    :param file_path: string, the path to the file to be deleted.
    :return: None. The function does not return any value.
    """
    try:
        os.remove(file_path)
        return True  # Return True if the file was successfully deleted
    except OSError as e:
        return e  # Return the exception if an error occurred
def delete_files_with_suffix(folder, suffixpat_include, verbose=False):  # omit unittests
    """
    Deletes all files in a given folder that end with a specified suffix.

    :param folder_path: string, the path to the folder where files are to be deleted.
    :param suffixpat_include: string, the suffix pattern of the files to be deleted.
    :param verbose: boolean, if True, the function will print verbose messages. Default is False.
    :return: None. The function does not return any value.
    """
    # Use apply_to_folder to delete files
    return apply_to_folder(delete_file, folder, suffixpat_include=suffixpat_include, include_subfolders=False, verbose=verbose)
def move_file(file_path, destination_folder): # cat 3a, unittest 3 - mocks
    """
    Moves a file to the specified destination folder.

    :param file_path: string, the path to the file to be moved.
    :param destination_folder: string, the path to the destination folder.
    :return: string, the new file path after moving, or an error if the operation fails.
    """
    # Check if the original file exists
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")

    # Check if the destination folder exists, if not, create it
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    # Create the new file path with the destination folder
    file_name = os.path.basename(file_path)
    new_file_path = os.path.join(destination_folder, file_name)

    # Move the original file to the new file path
    try:
        shutil.move(file_path, new_file_path)
        return new_file_path  # Return the new file path if the file was successfully moved
    except OSError as e:
        return e  # Return the exception if an error occurred
def move_files_with_suffix(source_folder, destination_folder, suffixpat_include, verbose=False): # omit unittest
    """
    Moves all files in a given folder that end with a specified suffix to the destination folder.

    :param source_folder: string, the path to the source folder where files are to be moved from.
    :param destination_folder: string, the path to the destination folder where files are to be moved to.
    :param suffixpat_include: string, the suffix pattern of the files to be moved.
    :param verbose: boolean, if True, the function will print verbose messages. Default is False.
    :return: list, the new file paths after moving, or an error if the operation fails.
    """
    # Use apply_to_folder to move files
    return apply_to_folder(move_file, source_folder, destination_folder, suffixpat_include=suffixpat_include, include_subfolders=False, verbose=verbose)
def tune_title(title):
    """
    Removes any special characters from the given title.

    :param title: string, the title from which special characters are to be removed.
    :return: string, the updated title with special characters removed.
    """
    # Remove any special characters from title_filename
    return re.sub(r'[^\w\s\-\(\)\.]', '', title)
def create_full_path(title_or_path, new_suffix_ext, default_folder=None):
    """
    Creates a full file path from a given title or path, a new suffix extension, and an optional default folder.

    :param title_or_path: string, the title or path of the file.
    :param new_suffix_ext: string, the new suffix extension to be added to the file.
    :param default_folder: string, the default folder to be used if no folder is specified in title_or_path. Default is None.
    :return: string, the newly created full file path.
    """
    # Extract file_stem, file_ext, and folder_path
    file_stem, file_ext = os.path.splitext(os.path.basename(title_or_path))
    folder_path = os.path.dirname(title_or_path)
    # Check if the file title or path argument includes a path
    if folder_path == '':
        if default_folder is not None:
            folder_path = default_folder
        else:
            raise ValueError("in create_full_path: no folder in title_or_path and default_folder is None.")
            
    # Remove special characters and apply naming conventions
    file_stem = tune_title(file_stem)

    # Construct the new file name with the new suffix and extension
    cur_suffix = get_suffix(file_stem)
    if cur_suffix is not None and cur_suffix + file_ext == new_suffix_ext:
        new_file_base = file_stem + file_ext
    else:
        new_file_base = file_stem + new_suffix_ext

    # Create the full path
    new_file_path = os.path.join(folder_path, new_file_base)

    return new_file_path
def find_file_in_folders(file_path, folder_paths):
    """
    Searches for a file within a list of folder paths and returns the first match.

    :param file_path: string of the file name to search for.
    :param folder_paths: list of strings of folder paths where the file will be searched.
    :return: string of the full path to the file if found, otherwise None.
    """
    if not os.path.isfile(file_path):
        for folder in folder_paths:
            potential_path = os.path.join(folder, os.path.basename(file_path))
            if os.path.isfile(potential_path):
                return potential_path
        return None
    else:
        warnings.warn(f"file_paths exists at this path - find_file_in_folders erroneously called")
        return file_path
def zip_files_in_folders(folder_paths, suffixpat_include, zip_file_path, include_subfolders=True):
    """
    Zips files in the specified folders that match the given suffix into a single zip file.

    :param folder_paths: list of strings, the paths to the folders where files will be zipped.
    :param suffixpat_include: string, the suffix pattern that included files must have.
    :param zip_file_path: string, the path where the single zip file will be created.
    :param include_subfolders: boolean, indicates whether to include files from subfolders.
    :return: None
    """
    import zipfile
    import os

    # Ensure the directory path for the zip file exists
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

    # Create a single zip file to store all files
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for folder_path in folder_paths:
            if os.path.isdir(folder_path):
                if include_subfolders:
                    # Include files from subfolders
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_name, file_extension = os.path.splitext(file)
                            if file_name.endswith(suffixpat_include):
                                file_path = os.path.join(root, file)
                                # Preserve the folder structure relative to the folder path
                                arcname = os.path.relpath(file_path, start=os.path.dirname(folder_path))
                                zipf.write(file_path, arcname)
                else:
                    # Only include files from the top-level directory
                    for file in os.listdir(folder_path):
                        if file.endswith(suffixpat_include) and os.path.isfile(os.path.join(folder_path, file)):
                            file_path = os.path.join(folder_path, file)
                            zipf.write(file_path, file)
            else:
                print(f"Folder does not exist: {folder_path}")

    print(f"Created zip at {zip_file_path} containing files from folders: {folder_paths}")
def compare_files_text(file1_path, file2_path):
    """
    Compares the content of two files.

    :param file1_path: string, the path to the first file to be compared.
    :param file2_path: string, the path to the second file to be compared.
    :return: boolean, True if the content of the files is exactly the same, False otherwise.
    """
    text1 = read_complete_text(file1_path)
    text2 = read_complete_text(file2_path)
    if text1 == text2:
        print("TRUE for compare_file_text - the content of the files is exactly the same.")
        return True
    else:
        print("FALSE for compare_file_text - the content of the files is different.")
        return False
def get_text_between_delimiters(full_text, delimiter_start, delimiter_end=None):
    """
    Extracts a substring from the given text between specified start and end delimiters.

    :param full_text: string of the text from which to extract the substring.
    :param delimiter_start: string of the delimiter indicating the start of the substring.
    :param delimiter_end: string of the delimiter indicating the end of the substring. If None, the end of the text is used. Default is None.
    :return: string of the extracted substring (inclusive of delimiter_start), or None if the start delimiter is not found.
    """
    start_index = full_text.find(delimiter_start)
    if start_index == -1:
        warnings.warn(f"in get_text_between_delimiters - no text found with delimiter_start: {delimiter_start} using the function: get_text_between_delimiters")
        return None
    end_index = len(full_text) if delimiter_end is None else full_text.find(delimiter_end, start_index + len(delimiter_start))
    if end_index == -1:
        end_index = len(full_text)

    extracted_text = full_text[start_index:end_index].rstrip('\n').rstrip(' \t')
    return extracted_text + '\n'
    # assumes that both delimiters are unique in the content string
    # return string inclusive of the delimiter_start but exclusive of the delimiter_end
    # return string has any blank lines stripped and ending with a single newline character
    # return None if delimiter_start not found
def check_if_duplicate_filename(filename, folder, exclude_suffix=True):
    """
    Checks if a filename already exists in a given folder, optionally excluding suffixes.

    :param filename: str, the filename to check for duplicates.
    :param folder: str, the path to the folder to search in.
    :param exclude_suffix: bool, whether to exclude suffixes when comparing filenames.
    :return: bool, True if a duplicate is found, False otherwise.
    """
    # Get all file names in the folder
    existing_files = os.listdir(folder)

    if exclude_suffix:
        # Strip off the suffix and extension from the input filename
        input_name = os.path.splitext(filename)[0]
        input_suffix = get_suffix(input_name)
        filename_without_suffix = input_name[:-(len(input_suffix))] if input_suffix else input_name
        
        # Check if the filename (without suffix and extension) exists
        for existing_file in existing_files:
            existing_name = os.path.splitext(existing_file)[0]
            existing_suffix = get_suffix(existing_name)
            existing_without_suffix = existing_name[:-(len(existing_suffix))] if existing_suffix else existing_name
            
            if filename_without_suffix.lower() == existing_without_suffix.lower():
                return True
        
        return False
    else:
        # Do an exact comparison including the suffix and extension
        return filename.lower() in [f.lower() for f in existing_files]

### TIME AND TIMESTAMP (3,202 tokens)
def convert_seconds_to_timestamp(seconds):
    """
    Converts a given number of seconds into a timestamp in the format hh:mm:ss or mm:ss.

    :param seconds: integer or float representing the number of seconds to be converted.
    :return: string representing the timestamp in the format hh:mm:ss or mm:ss.
    """
    if not isinstance(seconds, (int, float)):
        raise TypeError("Input must be an integer or float representing seconds.")
    if seconds < 0:
        raise ValueError("Input must be a non-negative number of seconds.")

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)  # This will always round down

    # If hours exist
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    # If minutes exist
    elif minutes > 0:
        return f"{minutes}:{seconds:02}"
    else:
        return f"0:{seconds:02}"
def convert_timestamp_to_seconds(timestamp):
    """
    Converts a timestamp in the format hh:mm:ss or mm:ss into seconds.

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :return: integer representing the total number of seconds.
    """
    if not isinstance(timestamp, str):
        raise TypeError("Timestamp must be a string in the format hh:mm:ss or mm:ss")

    time_components = timestamp.split(':')

    if not all(component.isdigit() for component in time_components):
        raise ValueError("Invalid timestamp: Non-numeric characters found")

    if len(time_components) == 3:
        hours, minutes, seconds = map(int, time_components)
    elif len(time_components) == 2:
        hours = 0
        minutes, seconds = map(int, time_components)
    else:
        raise ValueError("Invalid timestamp format. Expected hh:mm:ss or mm:ss")

    if not (0 <= hours <= 99):
        raise ValueError("Invalid timestamp: Hours must be in the range 0-99")

    if not (0 <= minutes <= 59):
        raise ValueError("Invalid timestamp: Minutes must be in the range 0-59")

    if not (0 <= seconds <= 59):
        raise ValueError("Invalid timestamp: Seconds must be in the range 0-59")

    total_seconds = seconds + minutes * 60 + hours * 3600
    return total_seconds
def change_timestamp(timestamp, delta_seconds):
    """
    Changes a given timestamp by a specified number of seconds. Uncomment line in tune_timestamp

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :param delta_seconds: integer representing the number of seconds to change the timestamp by.
    :return: string representing the new timestamp after the change.
    """
    if timestamp is None:
        raise ValueError("No timestamp provided. Cannot change timestamp.")
    modified_seconds = convert_timestamp_to_seconds(timestamp) + delta_seconds
    if modified_seconds < 0: 
        raise ValueError("Resulting time cannot be less than zero.")
    return convert_seconds_to_timestamp(modified_seconds)
def tune_timestamp(timestamp):
    """
    Converts a given timestamp to a standard format with respect to digits and leading zeros.

    :param timestamp: string representing the timestamp in the format hh:mm:ss or mm:ss.
    :return: string representing the tuned timestamp or None if the input timestamp is None.
    """
    # convert a timestamp to our standard with respect to digits and leading zeros
    if timestamp is None: # not sure if it was intentional to not raise ValueError but leave it
        return None
    # timestamp = change_timestamp(timestamp, 0)  # CAUTION - only include to shift the timestamps
    secs = convert_timestamp_to_seconds(timestamp)
    tuned_timestamp = convert_seconds_to_timestamp(secs)
    #print(f"Original timestamp: '{timestamp}'  Tuned timestamp: '{tuned_timestamp}'") 
    return tuned_timestamp
def get_timestamp(line, print_line=False, max_words=8):
    """
    Extracts a timestamp from a given line of text.

    :param line: string representing the line of text to search for a timestamp.
    :param print_line: boolean indicating whether to print the line where the timestamp was found. Default is False.
    :param max_words: integer representing the maximum number of words allowed before and after the timestamp. Default is 5.
    :return: tuple containing the extracted timestamp as a string and its index in the line, or (None, None) if no valid timestamp is found.
    """
    # Maximum number of words allowed before and after the timestamp, increase for assign speaker_names
    line = line.rstrip('\n') # Strip newline characters if present at the end

    # Regex to match timestamps in various formats including those in square brackets
    # followed by a link in parentheses. The restriction on what follows the timestamp and link has been removed.
    timestamp_regex = r"\b(?:\d{1,2}:)?\d{1,2}:\d{2}\b"
    link_regex = r"\[\s*([^\]]*)\]\(\s*([^)]+)\s*\)"
    #combined_regex = timestamp_regex + r"(?:" + link_regex + r")?"
    combined_regex = r"(" + timestamp_regex + r")" + r"(?:" + link_regex + r")?"

    match = re.search(combined_regex, line)
    if match:
        timestamp = match.group().rstrip()
        # Check if there are more than max words before the timestamp
        words_before_timestamp = line[:match.start()].split()
        if len(words_before_timestamp) > max_words:
            return None, None
        # Check if the string preceding the timestamp is 'length:' followed by any white space
        if ''.join(words_before_timestamp).lower() == 'length:':
            return None, None

        # Use the start of the timestamp as the index
        index = match.start()
        # Check if the character before the index is a starting square bracket
        if index > 0 and line[index - 1] == '[':
            index -= 1
        string_after_index = line[match.end():].split()

        # Check if there are more than max words after the timestamp
        # Exclude the check if the timestamp starts the line
        if len(string_after_index) > max_words and index != 0:
            return None, None

        # Extract just the timestamp without any brackets or links
        pure_timestamp_match = re.search(timestamp_regex, timestamp)
        if pure_timestamp_match:
            #timestamp = pure_timestamp_match.group()
            timestamp = match.group(1).rstrip()  # Group 1 is the timestamp

        # Check for timestamp overflow using the convert_timestamp_to_seconds function
        try:
            convert_timestamp_to_seconds(timestamp)
        except ValueError as ve:
            raise ValueError(f"Invalid timestamp: {timestamp}. Minutes or seconds exceed 59!") from ve

        if print_line:
            print(f"Timestamp found in line: {line} with timestamp = {timestamp} and index = {index}")

        return timestamp, index
    else:
        return None, None
def get_current_datetime_humanfriendly(timezone='America/Los_Angeles', include_timezone=True):
    """
    Returns the current date and time as a string for a given timezone, optionally including the timezone abbreviation and UTC offset.

    :param timezone: string representing the timezone to use for the current time.
    :param include_timezone: boolean indicating whether to include the timezone abbreviation and UTC offset in the returned string.
    :return: string representing the current date and time in the specified timezone, optionally followed by the timezone abbreviation and UTC offset.
        """
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    datetime_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    if include_timezone:
        #timezone_abbr = current_time.strftime('%Z')  # remove using the abbr such as PDT PST to avoid complication 5-4-24 RT
        utc_offset = tz.utcoffset(current_time.replace(tzinfo=None)).total_seconds() / 3600
        datetime_str += f" UTC{int(utc_offset):+03d}:00 {timezone}"
    return datetime_str
#TODO needs unittests
def get_current_datetime_filefriendly(location='America/Los_Angeles', include_utc=False):
    """
    Returns the current date and time as a filename-friendly string for a given timezone, optionally including only the UTC offset.

    :param location: string representing the timezone to use for the current time.
    :param include_utc: boolean indicating whether to include the UTC offset in the returned string.
    :return: string representing the current date and time in the specified timezone, formatted for filenames, optionally followed by the UTC offset.
        """
    datetime_str = get_current_datetime_humanfriendly(location, include_timezone=True)
    # Remove colons and replace spaces with underscores
    filename_friendly_datetime = datetime_str.replace(':', '').replace(' ', '_')
    if include_utc:
        # Extract UTC offset and format it
        utc_offset = filename_friendly_datetime.split('_UTC')[1].split('_')[0]
        utc_offset = utc_offset.replace('+', '').replace(':', '')
        # Include only the UTC offset in the filename
        filename_friendly_datetime = filename_friendly_datetime.split('_UTC')[0] + '_UTC' + utc_offset
    else:
        # Remove UTC part if not included
        filename_friendly_datetime = filename_friendly_datetime.split('_UTC')[0]
    return filename_friendly_datetime
#TODO Consider adding more flexibility to date and time formats
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
    # Define delimiters for splitting the input string
    first_delimiter_index = re.search(r'[ _]', datetime_flex).start()
    date_part = datetime_flex[:first_delimiter_index]
    remainder = datetime_flex[first_delimiter_index + 1:]

    next_delimiter_index = re.search(r'[ _]', remainder)
    if next_delimiter_index:
        next_delimiter_index = next_delimiter_index.start()
        time_part = remainder[:next_delimiter_index]
        remainder = remainder[next_delimiter_index + 1:]
    else:
        time_part = remainder
        remainder = ''

    utc_offset_part = ''
    timezone_part = ''
    utc_index = remainder.find('UTC')
    if utc_index != -1:
        utc_end_index = re.search(r'[ _]', remainder[utc_index:])
        if utc_end_index:
            utc_end_index = utc_end_index.start() + utc_index
            utc_offset_part = remainder[utc_index:utc_end_index]
            timezone_part = remainder[utc_end_index + 1:]
        else:
            utc_offset_part = remainder[utc_index:]
            timezone_part = ''
    else:
        timezone_part = remainder

    verbose_print(verbose, f"Date part: {date_part}")
    verbose_print(verbose, f"Time part: {time_part}")
    verbose_print(verbose, f"UTC offset part: '{utc_offset_part}'")
    verbose_print(verbose, f"Timezone part: '{timezone_part}'")
    # Validate date part format
    try:
        datetime.strptime(date_part, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Date format not recognized: {date_part}. Expected format: YYYY-MM-DD")

    # Validate and format the time part
    if len(time_part) == 6 and time_part.isdigit():
        time_part = time_part[:2] + ':' + time_part[2:4] + ':' + time_part[4:]
        verbose_print(verbose, f"Formatted time part: {time_part}")
    elif len(time_part) == 8 and re.match(r'\d{2}:\d{2}:\d{2}', time_part):
        verbose_print(verbose, f"Time part already formatted: {time_part}")
    else:
        raise ValueError(f"Time format not recognized: {time_part}. Expected formats: HHMMSS (6 digits) or HH:MM:SS")

    # Use the provided UTC offset if available, otherwise use extracted timezone part, then if neither of those exist then use the default timezone
    if utc_offset_part.strip():
        utc_offset_match = re.search(r'([-+]?\d{2}):?(\d{2})', utc_offset_part)
        if utc_offset_match:
            hours = int(utc_offset_match.group(1))
            minutes = int(utc_offset_match.group(2))
            utc_offset_minutes = hours * 60 + minutes
            tz = pytz.FixedOffset(utc_offset_minutes)  # Create timezone from UTC offset in minutes
            verbose_print(verbose, f"Using extracted UTC offset: {utc_offset_part}")
        else:
            raise ValueError(f"Invalid UTC offset format: {utc_offset_part}")
    elif timezone_part:
        verbose_print(verbose, f"Using extracted timezone part: {timezone_part}")
        tz = pytz.timezone(timezone_part)
    else:
        verbose_print(verbose, f"No valid UTC offset or timezone part extracted, using default timezone: {timezone}")
        tz = pytz.timezone(timezone)

    # Combine date and time parts and parse them
    datetime_str = f"{date_part} {time_part}"
    try:
        naive_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        localized_time = tz.localize(naive_time)
        epoch_time = (localized_time - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
        return epoch_time
    except ValueError:
        raise ValueError(f"Time format not recognized: {datetime_str}")
def get_elapsed_seconds(start_time_epoch_seconds):
    """
    Calculates the time elapsed since the start_time and returns it in seconds.

    :param start_time: float, the start time in seconds since the epoch (as returned by time.time())
    :param return_format: string ('minutes' or 'timestamp') for the return value format - 'timestamp' for H:MM:SS or minutes with one decimal place
    :return: integer of the number of seconds
    """
    current_time = time.time()
    return int(round(current_time - start_time_epoch_seconds))

### TIMESTAMP LINKS (990 tokens)
def remove_timestamp_links_from_content(content):
    """
    Removes markdown timestamp links from the content and returns the modified content.

    :param content: string of the content from which to remove markdown timestamp links.
    :return: string of the content with markdown timestamp links removed.
    """
    content_lines = content.splitlines()
    processed_lines = [re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line) for line in content_lines]
    return '\n'.join(processed_lines)+"\n"  # explicitly add extra newline to avoid stripping one
#TODO Update to auto detect whether the file path has metadata and content by. First trying to read the file as metadata and content. And so I'm going to need to adjust that function to probably to return something that will indicate to branch.
def remove_timestamp_links(file_path):
    """
    Removes markdown timestamp links and overwrites the file.

    :param file_path: string of the path to the original file.
    :return: none.
    """
    metadata, content = read_file_flex(file_path)
    new_content = remove_timestamp_links_from_content(content)
    
    if metadata is None:
        write_complete_text(file_path, new_content, overwrite='yes')
    else:
        write_metadata_and_content(file_path, metadata, new_content, suffix_new='_temp', overwrite='yes')
def generate_timestamp_link(base_link, timestamp):
    """
    Helper function to generate a timestamp link for a given base link and timestamp.
    It uses a dictionary to map domains to their respective timestamp formats.
    For Vimeo, the timestamp is converted to milliseconds.
    
    :param base_link: string of the base URL to which the timestamp will be appended.
    :param timestamp: string of the timestamp to be converted and appended to the base URL.
    :return: string of the complete URL with the timestamp appended in the appropriate format.
    """
    # Dictionary mapping domains to their timestamp formats
    domain_timestamp_formats = {
        "youtube.com": "&t={}",
        "youtu.be": "&t={}",
        "spotify.com": "&t={}",
        "vimeo.com": "?ts={}"
    }

    # Determine the domain format based on the base link
    for domain, format_string in domain_timestamp_formats.items():
        if domain in base_link:
            domain_timestamp_format = format_string
            break
    else:
        domain_timestamp_format = "&t={}"  # Default format if domain not found

    # Convert the timestamp to the appropriate format
    if "?ts={}" in domain_timestamp_format:
        # Vimeo uses milliseconds
        timestamp_seconds = convert_timestamp_to_seconds(timestamp) * 1000
    else:
        # Other domains use seconds
        timestamp_seconds = convert_timestamp_to_seconds(timestamp)

    # Create the new timestamp link
    timestamp_link = f"[{timestamp}]({base_link}{domain_timestamp_format.format(timestamp_seconds)})"
    return timestamp_link
def add_timestamp_links_to_content(content, base_link):
    """
    Adds timestamp links to the content using the provided base link.

    :param content: string of the content where timestamp links will be added.
    :param base_link: string of the base URL to which the timestamp will be appended.
    :return: string of the content with timestamp links added.
    """
    # Processes each line of the content to add timestamp links using the base link
    content_lines = content.splitlines()
    processed_lines = []
    for line in content_lines:
        timestamp, index = get_timestamp(line)
        if timestamp:
            tuned_timestamp = tune_timestamp(timestamp)
            if tuned_timestamp and index is not None:
                timestamp_link = generate_timestamp_link(base_link, tuned_timestamp)
                line_with_link = line[:index] + timestamp_link + line[index + len(timestamp):]
            else:
                line_with_link = line
        else:
            line_with_link = line
        processed_lines.append(line_with_link)
    return '\n'.join(processed_lines)+"\n"  # explicitly add extra newline to avoid stripping one
def add_timestamp_links(file_path):
    """
    Adds markdown timestamp links and overwrites the file.

    :param file_path: string, the path to the file where timestamp links will be added.
    :return: none
    """
    metadata, content = read_metadata_and_content(file_path)
    _, base_link = read_metadata_field_from_file(file_path, "link")
    
    # First, remove any existing timestamp links from the content
    content_without_links = remove_timestamp_links_from_content(content)
    # Then, add new timestamp links to the content
    new_content = add_timestamp_links_to_content(content_without_links, base_link)

    write_metadata_and_content(file_path, metadata, new_content, suffix_new='_temp', overwrite='yes')

### FIND AND REPLACE (1,026 tokens)
def count_num_instances(file_path, find_str):
    """
    Counts the number of instances of a specific string in the text of the file.
    Is case-sensitive.

    :param file_path: string, the path to the file where the search will be performed.
    :param find_str: string, the string to find in the file content.
    :return: int, the number of instances found, or zero if no instances are found.
        """
    complete_text = read_complete_text(file_path)
    count = complete_text.count(find_str)
    print(f"Number instances: {count} of {find_str} found in {file_path}")
    return count
def find_and_replace_pairs(file_path, find_replace_pairs, use_regex=False):
    """
    Finds and replaces multiple specified strings or regex patterns in the file and overwrites the original file.

    :param file_path: string, the path to the file where the find and replace operations will be performed.
    :param find_replace_pairs: list of tuples, each containing a string or regex pattern to be found and a string to replace it with.
    :param use_regex: boolean for whether to use regex patterns for finding. Default is False (use exact string matching).
    :return: int, the total number of replacements made.
    """
    metadata, content = read_file_flex(file_path)

    total_replacements = 0
    for find_str, replace_str in find_replace_pairs:
        if use_regex:
            regex = re.compile(find_str, re.DOTALL)
            content, count = regex.subn(replace_str, content)
        else:
            content, count = re.subn(re.escape(find_str), replace_str, content, flags=re.DOTALL)
        total_replacements += count

    if metadata is None:
        write_complete_text(file_path, content, overwrite='yes')
    else:
        write_metadata_and_content(file_path, metadata, content, overwrite='yes')

    return total_replacements
#TODO reconsider the flexibility of the space before the comma so that we can use pairs with leading or trailing spaces, maybe have a warning confirmation message if the csv has a pair with a leading space
def parse_csv_for_find_replace(csv_file):
    """
    Parses a CSV file to extract find and replace pairs.
    Returns a list of the find_
    """
    pairs = []
    with open(csv_file, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)
        if not (first_row and ','.join(first_row).strip().startswith('find')):
            warnings.warn("CSV does not start with 'find, replace' header. Processing the first row as data.")
            pairs.append((first_row[0].strip(), first_row[1].strip()))
        for row in csvreader:
            if row and not row[0].strip().startswith('#'):
                try:
                    find_str, replace_str = row[0].strip(), row[1].strip()
                    pairs.append((find_str, replace_str))
                except IndexError as e:
                    print(f"Error processing row: {row} - {str(e)}")
    return pairs
#TODO needs unittest
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
    # Parse the CSV to get find and replace pairs
    find_replace_pairs = parse_csv_for_find_replace(find_replace_csv)
    
    # Apply find and replace operations to all files in the folder
    results = apply_to_folder(find_and_replace_pairs, folder_path, find_replace_pairs, suffixpat_include=suffixpat_include, verbose=verbose)

    # Print the total number of replacements in all files
    total_replacements = sum(results.values())
    print(f"{total_replacements} REPLACEMENTS IN {len(results)} files run.")

    # If verbose is True, print the number of replacements for each file
    if verbose:
        for file_path, num_replacements in results.items():
            print(f"{num_replacements} replacements in file: {file_path}  {num_replacements} replacements")

### HEADINGS (1,943 tokens)
def get_heading_level(heading):
    """
    Determines the level of a markdown heading.

    :param heading: string, the markdown heading including '#' characters.
    :return: int, the level of the heading.
    """
    return len(heading) - len(heading.lstrip('#'))
def get_heading_pattern(heading):
    """
    Creates a regex pattern to match a heading and its content, including subheadings.

    :param heading: string, the markdown heading including '#' characters.
    :return: compiled regex pattern or None if heading is empty
    """
    if not heading:
        return None

    heading_level = get_heading_level(heading)
    
    # Escape special characters in the heading
    escaped_heading = re.escape(heading)
    
    # Define the end delimiter as any markdown heading of equal or higher order
    delimiter_end_pattern = r'(?=^#{1,' + str(heading_level) + r'}\s|\Z)'
    
    # Construct the full pattern
    full_pattern = f"({escaped_heading}.*?){delimiter_end_pattern}"
    
    return re.compile(full_pattern, re.MULTILINE | re.DOTALL)
def find_heading_text(full_text, heading):
    """
    Finds the heading text, including its subheadings, inclusive of the heading itself.

    :param text: string, the text to search in.
    :param heading: string, the markdown heading to find.
    :return: tuple (start_index, end_index) or None if not found.
    """
    pattern = get_heading_pattern(heading)
    if pattern is None:
        return None
    match = pattern.search(full_text)
    if match:
        return match.start(), match.end()
    return None
def get_heading(file_path, heading):
    """
    Extracts the markdown heading and its associated text from a file, including any subheadings of equal or lower order.
    Uses the complete text and does not parse the metadata and content sections.

    :param file_path: string, the path to the file to be read.
    :param heading: string, the markdown heading to be extracted, including the '#' characters and the following space.
    :return: string, the markdown heading and its associated text, including any subheadings of equal or lower order.
    """
    complete_text = read_complete_text(file_path)
    result = find_heading_text(complete_text, heading)
    if result:
        start, end = result
        return complete_text[start:end]
    return None
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
    metadata, content = read_metadata_and_content(file_path)
    
    new_text_with_heading = f"{heading}\n{new_text}"
    if not new_text_with_heading.endswith('\n'):
        new_text_with_heading += '\n'
    
    result = find_heading_text(content, heading)
    
    if result:
        start, end = result
        new_content = content[:start] + new_text_with_heading + content[end:]
    else:
        # Add new heading at the top of the content section
        content_lines = content.split('\n')
        if content.strip():  # Check if content is not empty
            if len(content_lines) > 1:
                # Find the position of the first non-blank line after the first line
                insert_position = 1
                while insert_position < len(content_lines) and content_lines[insert_position].strip() == '':
                    insert_position += 1
                # Strip a single newline from the end of new_text_with_heading if present
                new_text_to_insert = new_text_with_heading[:-1] if new_text_with_heading.endswith('\n') else new_text_with_heading
                # Insert the new heading and text
                content_lines.insert(insert_position, new_text_to_insert)
                new_content = '\n'.join(content_lines)
            else:
                # If content has only one line, append the new heading and text
                new_content = f"{content.rstrip()}\n\n{new_text_with_heading}"
        else:
            # If content is empty, just use the new heading and text
            new_content = new_text_with_heading
    
    # Write the updated content back to the file
    write_metadata_and_content(file_path, metadata, new_content, suffix_new='_temp', overwrite='yes')
def delete_heading(file_path, heading):
    """
    Deletes the specified markdown heading and its following text, including subheadings, and overwrites the file.
    If the heading does not exist, a warning is issued and no action is taken.

    :param file_path: string of the path to the file from which the heading will be deleted.
    :param heading: string of the markdown heading to be deleted, including the '#' characters and the following space.
    """
    metadata, content = read_metadata_and_content(file_path)
    
    result = find_heading_text(content, heading)
    
    if result:
        start, end = result
        new_content = content[:start] + content[end:]
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)
        
        write_metadata_and_content(file_path, metadata, new_content, suffix_new='_temp', overwrite='yes')
    else:
        warnings.warn("in delete_heading: trying to delete heading that does not exist - no action")
def append_heading_to_file(source_file_path, target_file_path, heading, include_filename=True):
    """
    Appends the text under a specified heading from a source file to a target file, optionally including the source filename as a heading.

    :param source_file_path: string of the path to the source file.
    :param target_file_path: string of the path to the target file where the text will be appended.
    :param heading: string of the markdown heading to be appended.
    :param include_filename: boolean indicating whether to include the source filename as a heading. Defaults to True.
    :return: string of the appended text or None if the heading is not found in the source file.
    """
    new_text = get_heading(source_file_path, heading)
    if new_text is not None:
        if include_filename:
            # Extract the file name from the source file path
            filename = os.path.basename(source_file_path)
            # Determine the markdown heading level for the filename (one less than the heading level)
            heading_level = '#' * (heading.count('#') - 1 if heading.count('#') > 1 else 1)
            # Add the filename as a heading above the new_text
            new_text = f"{heading_level} {filename}\n{new_text}"
        
        # Check if the target file path has a folder component; if not, use the folder from the source file path
        target_folder = os.path.dirname(target_file_path)
        if not target_folder:
            source_folder = os.path.dirname(source_file_path)
            target_file_path = os.path.join(source_folder, os.path.basename(target_file_path))
 
        if os.path.exists(target_file_path):
            text = read_complete_text(target_file_path)
            text += '\n' + new_text

        write_complete_text(target_file_path, text, suffix_new='_temp', overwrite='yes')
        return new_text
    else:
        return None
def create_new_file_from_heading(file_path, heading, suffix_new='_headingonly', remove_heading=False):
    """
    Extracts text under a specified heading from a file and writes it to a new file with a specified suffix.

    :param file_path: string of the path to the file.
    :param heading: string of the markdown heading to be processed.
    :param suffix_new: string of the suffix to be appended to the new file. Defaults to "_headingonly".
    :param remove_heading: boolean indicating whether to remove the heading from the extracted text. Defaults to False.
    :return: string of the path to the newly created file.
    """
    heading_text = get_heading(file_path, heading)
    
    if heading_text is None:
        heading_text = ""  # Set to empty string if heading not found or file is empty
    else:
        if remove_heading:
            # Remove the markdown heading line and any blank lines that follow it
            lines = heading_text.split('\n')
            non_empty_index = next((i for i, line in enumerate(lines) if line.strip() and not line.startswith('#')), len(lines))
            heading_text = '\n'.join(lines[non_empty_index:])
        else:
            # Strip the markdown heading from the beginning of the complete text
            heading_text = heading_text.lstrip(heading).lstrip('\n')
    
    return write_complete_text(file_path, heading_text, suffix_new)

### METADATA (2,673 tokens)
def set_metadata_field(metadata, field, value):
    """
    Sets or updates a metadata field with a given value.

    :param metadata: string, the metadata from which a metadata field is to be set or updated.
    :param field: string, the metadata field to be set or updated without the : and space.
    :param value: string, the value to be set for the metadata field.
    :return: string, the updated metadata with the set or updated metadata field.
    """
    # Split the metadata text into lines
    lines = metadata.split('\n')
    field_line = None
    field_exists = False
    insert_index = -1  # Default insert index to the end of the metadata

    # Check if the field already exists and find the insert index after '## metadata'
    metadata_start_found = False
    for i, line in enumerate(lines):
        if '## metadata' in line:
            metadata_start_found = True
            metadata_index = i
        elif metadata_start_found and line.strip() == '':
            insert_index = i  # Set insert index to the first blank line after '## metadata'
            break
        if line.startswith(f"{field}:"):
            field_exists = True
            field_line = i
            break

    # If the field exists, update it
    if field_exists:
        lines[field_line] = f"{field}: {value}"
    else:
        # If the field does not exist, add it at the insert index
        if insert_index == -1:  # If no blank line was found, append it after the metadata heading
            lines.insert(metadata_index + 1, f"{field}: {value}")
        else:
            lines.insert(insert_index, f"{field}: {value}")

    # Reassemble the metadata text
    updated_metadata = '\n'.join(lines)

    return updated_metadata
def remove_metadata_field(metadata, field):
    """
    Removes a specified metadata field from the metadata.

    :param metadata: string, the metadata from which a metadata field is to be removed.
    :param field: string, the metadata field to be removed.
    :return: string, the updated metadata with the removed metadata field.
    """
    # Removes a specified metadata field from the metadata
    lines = metadata.split('\n')
    updated_lines = [line for line in lines if not line.startswith(f"{field}:")]
    updated_metadata = '\n'.join(updated_lines)
    # DONE fill in code utilizing code from @add_metadata_field to delete the provided field
    return updated_metadata
def create_initial_metadata():
    """
    Creates an initial metadata for a file.

    :return: string, the initial metadata for a file.
    """
    metadata = "## metadata\nlast updated: \n"  # newlines will
    return metadata
def set_last_updated(metadata, new_last_updated_value, use_today=True):
    """
    Updates the 'last updated' metadata field in the metadata with a new value.

    :param metadata: string, the metadata from which the 'last updated' metadata field is to be updated.
    :param new_last_updated_value: string, the new value for the 'last updated' metadata field.
    :param use_today: boolean, if True, today's date is prepended to the new_last_updated_value. Default is True.
    :return: string, the updated metadata with the new 'last updated' value.
    """
    if use_today:
        date_today = datetime.now().strftime("%m-%d-%Y") # Assign today's date in format MM-DD-YYY
        new_last_updated_value = f"{date_today} {new_last_updated_value}"
    return set_metadata_field(metadata, 'last updated', new_last_updated_value)
def read_metadata_field_from_file(file_path, field):
    """
    Reads a specific metadata field from a file.

    :param file_path: string, the path to the file to be read.
    :param field: string, the metadata field to be read from the file.
    :return: tuple, the line number of the field and the value of the field.
    """
    metadata, _ = read_metadata_and_content(file_path)
    metadata_start = metadata.find('## metadata')
    metadata_end = metadata.find('##', metadata_start + len('## metadata'))
    if metadata_end == -1:  # If there's no second '##', use the end of the string
        metadata_end = len(metadata)
    metadata_selection = metadata[metadata_start:metadata_end].strip()
    field_search = f"{field}: "
    field_start = metadata_selection.find(field_search)
    if field_start != -1:
        field_line = metadata_selection[:field_start].count('\n') + 2  # +2 because we start counting from 1 and there's the '## metadata' line
        field_start += len(field_search)
        field_end = metadata_selection.find('\n', field_start)
        if field_end == -1:  # If it's the last field in the metadata
            field_end = len(metadata_selection)
        field_value = metadata_selection[field_start:field_end].strip()
        return field_line, field_value
    return None
def set_metadata_fields_from_csv(folder_path, csv_file_path, suffix_extension):
    """
    Sets metadata fields for all files in a folder based on a CSV file.

    :param folder_path: string of the path to the folder containing the files.
    :param csv_file_path: string of the path to the CSV file with metadata fields and values.
    :param suffix_extension: string of the file extension to be appended to file bases.
    :return: None, but prints the number of files processed successfully and the total in the CSV excluding empty rows.
    """
    # Read the CSV file and extract the metadata fields and values
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        metadata_fields = next(csv_reader)  # First row contains metadata field names
        metadata_values = [row for row in csv_reader if row]  # Remaining rows contain metadata values, excluding empty rows

    total_files_in_csv = len(metadata_values)  # Count only non-empty rows
    successfully_processed_files = 0

    # Iterate over each row in the CSV to update files
    for row_index, row in enumerate(metadata_values, start=1):  # Start counting rows from 1
        if len(row) < len(metadata_fields):  # Check if the row has enough columns
            print(f"Row {row_index} in CSV does not have enough columns. Expected {len(metadata_fields)}, got {len(row)}.")
            continue

        file_base = row[0] + suffix_extension
        file_path = os.path.join(folder_path, file_base)
        # Map fields to values
        metadata_dict = dict(zip(metadata_fields[1:], row[1:]))

        try:
            # Read the header and content from the file
            metadata, content = read_metadata_and_content(file_path)

            # Update the metadata fields from the CSV
            for field, value in metadata_dict.items():
                metadata = set_metadata_field(metadata, field, value)

            write_metadata_and_content(file_path, metadata, content, suffix_new='_temp', overwrite='yes')

            successfully_processed_files += 1
        except Exception as e:
            print(f"Failed to process file {file_base}: {e}")

    print(f"Total files in CSV excluding empty rows: {total_files_in_csv}")
    print(f"Successfully processed files: {successfully_processed_files}")
#TODO update the filename variables to follow our naming conventions
#TODO consider updating to not require the generic field to end with a colon
def create_csv_from_fields(folder_path, fields):
    """
    Generates a CSV file of input fields from all markdown files in a folder.
    Fields can be 2 formats, 1) generic, usually metadata (ending with a ':') or 2) markdown headings (starting with a '#').
    Generic fields extract single-line values, while heading fields capture all content under the heading.

    :param folder_path: string, the path to the folder containing the markdown files.
    :param fields: list, the fields to be extracted from the markdown files.
    :return: string of the path to the created csv file.
    """
    # Generates a CSV file from all files in the specified folder
    folder_name = os.path.basename(os.path.normpath(folder_path))
    csv_filename = os.path.join(folder_path, f'{folder_name}.csv')

    # Check if the CSV file already exists and prompt for action
    if os.path.exists(csv_filename):
        user_input = input(f"The file {csv_filename} already exists. Overwrite? (y/n): ").strip().lower()
        if user_input == 'n':
            base, ext = os.path.splitext(csv_filename)
            csv_filename = f"{base}(1){ext}"

    with open(csv_filename, 'w', newline='') as csvfile:
        # Adjust field names by removing ":" and "#" and any leading/trailing spaces
        adjusted_fields = ['file_name', 'title'] + [field.strip().replace(':', '').replace('#', '') for field in fields]
        csv_writer = csv.DictWriter(csvfile, fieldnames=adjusted_fields)
        csv_writer.writeheader()

        # Iterate over each file in the folder
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.md'):  # Assuming markdown files
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    content = file.read()

                # Initialize a dictionary to store extracted data
                data = {'file_name': filename, 'title': os.path.splitext(filename)[0]}
                for field in fields:
                    adjusted_field = field.strip().replace(':', '').replace('#', '')
                    if field.endswith(':'):
                        # Field is a metadata line
                        match = re.search(rf'^{field}\s+(.*)', content, re.MULTILINE)
                        if match:
                            data[adjusted_field] = match.group(1).strip()
                    elif field.startswith('#'):
                        # Field is a markdown heading
                        heading_text = get_heading(file_path, field)
                        if heading_text:
                            # Remove the heading line itself
                            field_content = re.sub(rf'^{re.escape(field)}.*\n?', '', heading_text, flags=re.MULTILINE)
                            # Remove leading and trailing whitespace
                            field_content = field_content.strip()
                            # Remove multiple blank lines
                            field_content = re.sub(r'\n\s*\n', '\n', field_content)
                            data[adjusted_field] = field_content

                # Write the extracted data to the CSV
                csv_writer.writerow(data)

    print(f"CSV file created at {csv_filename}")
    return csv_filename
def create_csv_matrix_from_triples(triples_text, target_file_path):
    """
    Converts multiline text of triples into a csv matrix file where each entry is the number for that row and column.

    :param triples_text: string of multiline text containing rows of data separated by newlines, each row containing two strings and a number separated by commas.
    :param target_file_path: string of the path to the target csv file.
    :return: string of the path to the created csv file.
    """
    import csv
    from collections import defaultdict

    # Parse the triples text into a list of tuples
    triples = []
    for line in triples_text.strip().split('\n'):
        if line:
            items = line.split(', ')
            if len(items) != 3:
                raise ValueError(f"Line does not contain exactly three items: {line}")
            triples.append(items)

    # Extract unique row titles and column headers, and sort them
    row_titles = sorted(set(row[0] for row in triples), key=lambda s: s.lower())
    column_headers = sorted(set(row[1] for row in triples))

    # Create a default dictionary to hold the numbers, with a default of 0
    matrix = defaultdict(lambda: defaultdict(int))
    for row_title, col_header, number in triples:
        matrix[row_title][col_header] = int(number)

    # Write to CSV
    with open(target_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['row title'] + column_headers)
        row_count = 0
        for row_title in row_titles:
            row_data = [matrix[row_title][col_header] for col_header in column_headers]
            csv_writer.writerow([row_title] + row_data)
            row_count += 1

    print(f"CSV file with {row_count} rows created at {target_file_path}")
    return target_file_path





## primary/transcribe.py (17,181 tokens)
#Library of functions and execution code to transcribe audio files
import os
import sys
import re
import threading
import time
from datetime import datetime, timedelta
import requests
import yt_dlp as youtube_dl
from num2words import num2words
import json
import math
import mutagen  # Import mutagen to handle audio metadata
from wordfreq import top_n_list
#Get the top 3000 English words
common_english_vocab = set(top_n_list('en', 3000))

from config import DEEPGRAM_API_KEY

import warnings  # Set the warnings to use a custom format
from primary.fileops import custom_formatwarning
warnings.formatwarning = custom_formatwarning
#USAGE: warnings.warn(f"Insert warning message here")

#Get the directory name of the current file (transcribe.py) and the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir) # Add the parent directory to sys.path

### YOUTUBE (3,351 tokens)
def download_mp3_from_youtube(url, output_title='downloaded_audio'):
    """ 
    Downloads an audio file from a YouTube URL and saves it as an mp3 file. Uses yt_dlp package.

    :param url: string of the YouTube URL from which to download the audio.
    :param output_title: string of the title to save the downloaded mp3 file as. defaults to 'downloaded_audio'.
    :return: string of the path to the saved mp3 file.
    """
    output_file_path = output_title + '.mp3'
    if os.path.exists(output_file_path):
        user_input = input("Audio file already exists. Enter 'y' or 'yes' to download again and overwrite, or any other key to skip: ").lower()
        if user_input not in ['y', 'yes']:
            print("Skipping download.")
            return output_file_path

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_title,  # note it's not output_path, by default save file as "downloaded_audio.mp3"
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_file_path
def get_youtube_title_length(url):
    """ 
    Retrieves the title and duration of a youtube video in a formatted timestamp. Uses yt_dlp package.

    :param url: string of the youtube url to retrieve information from.
    :return: tuple containing the video title and its duration as a string in a formatted timestamp.
    """
    from primary.fileops import tune_timestamp
    ydl_opts = {
        'quiet': True,
        'skip_download': True,  # We just want the info
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'Unknown Title')
        video_duration = info_dict.get('duration', 0)
        # Convert duration from seconds to a time format (H:MM:SS)
        video_length = tune_timestamp(str(timedelta(seconds=video_duration)))
        return video_title, video_length
def download_link_list_to_mp3s(links, audio_inbox_path="data/audio_inbox"):  # NO CALLERS (3-3 RT)
    """
    Downloads a list of youtube links as mp3 files to a specified directory and stores the link-title pairs. Uses yt_dlp package.
    Calls download_mp3_from_youtube

    :param links: list of youtube links to be downloaded.
    :param audio_inbox_path: string of the directory path where the audio files will be saved.
    :return: dictionary mapping each youtube link to its corresponding title.
    """
    link_title_pairs = {}
    for link in links:
        title, length = get_youtube_title_length(link)  # Get title and length
        title = title.rsplit('.', 1)[0]  # Remove file extension from title
        link_title_pairs[link] = title  # Store link-title pair
        download_mp3_from_youtube(link, os.path.join(audio_inbox_path, title))  # Download as MP3
    return link_title_pairs
def download_youtube_subtitles_url(subtitle_url): # DS, cat 1, omit unittests since called by next function
    """
    Downloads and extracts subtitle text from a given YouTube subtitle URL.
    Helper function to that is called from get_youtube_subtitles
    
    :param subtitle_url: string of the url from which subtitles are to be downloaded.
    :return: string of the extracted subtitle text, spaces between segments and stripped of new lines.
    """
    response = requests.get(subtitle_url)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    subtitle_data = response.json()  # Parse JSON data

    # Extract transcript text from the subtitle data
    subtitle_text = ""
    for event in subtitle_data['events']:
        if 'segs' in event:
            for seg in event['segs']:
                if 'utf8' in seg:
                    subtitle_text += seg['utf8'] + " "

    return subtitle_text.replace('\n', ' ').strip()
def get_youtube_subtitles(url):
    """
    Retrieves English subtitles for a given YouTube video URL if available. Uses yt_dlp package.
    
    :param url: string of the youtube video url.
    :return: subtitles as a string if found, otherwise None.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en']  # Specify the language of subtitles you want to download
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        
        # Attempt to get the transcript (subtitles)
        subtitles = info_dict.get('subtitles', {})
        auto_captions = info_dict.get('automatic_captions', {})
        
        # Choose subtitles or automatic captions to return
        transcript_info = subtitles if subtitles else auto_captions
        
        # If there are subtitles or auto captions, download them
        if transcript_info.get('en'):
            subtitles_url = transcript_info['en'][0]['url']  # Get the URL for the first English subtitle track
            return download_youtube_subtitles_url(subtitles_url)
        else:
            print("No English subtitles found.")
            return None
def get_youtube_all(url):
    """
    Retrieves all available information from a YouTube video URL, including title, length, chapters, description, and transcript. Uses yt_dlp package.
    
    :param url: string of the youtube video url.
    :return: dictionary with video details or None if the URL is invalid.
    """
    if not is_valid_youtube_url(url):
        print(f"Invalid YouTube URL: {url}")
        return None
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en']
    }
    
    transcript_text = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        
        # Extract title, channel, date, and length
        video_title = info_dict.get('title', 'Unknown Title')
        video_channel = info_dict.get('uploader', 'Unknown Channel')
        video_date = info_dict.get('upload_date', 'Unknown Date')
        video_duration = info_dict.get('duration', 0)
        video_length = str(timedelta(seconds=video_duration))
        
        # Extract chapters
        chapters = info_dict.get('chapters', [])
        #print("DEBUG - Chapters:", chapters if chapters else "Chapters is None")
        if chapters:
            formatted_chapters = [{'start_time': str(timedelta(seconds=chap['start_time'])),
                                   'title': chap['title']} for chap in chapters]
        else:
            formatted_chapters = ''
        
        # Extract description
        description = info_dict.get('description', '')
        
        # Extract subtitles
        subtitles = info_dict.get('subtitles', {})
        auto_captions = info_dict.get('automatic_captions', {})
        
        # Choose subtitles or automatic captions to return and assign the source
        if subtitles:
            transcript_info = subtitles
            transcript_source = 'subtitles'
        else:
            transcript_info = auto_captions
            transcript_source = 'auto-captions'
        
        # If there are subtitles or auto captions, download them
        if transcript_info.get('en'):
            subtitles_url = transcript_info['en'][0]['url']  # Get the URL for the first English subtitle track
            transcript_text = download_youtube_subtitles_url(subtitles_url)
            transcript_text = ' '.join(transcript_text.split())  # compress multiple spaces into one
        else:
            print("No English subtitles found.")
        
        print(f"For YouTube video title: {video_title}")
        extracted_features = []
        if formatted_chapters:
            extracted_features.append('chapters')
        if description:
            extracted_features.append('description')
        if transcript_source:
            extracted_features.append(f'transcript from {transcript_source}')
        
        print(f"  extracted the following features: {', '.join(extracted_features)}")
        return {
            'title': video_title,
            'channel': video_channel,
            'date': video_date,
            'length': video_length,
            'chapters': formatted_chapters,
            'description': description,
            'transcript': transcript_text or "No transcript found",
            'transcript source': transcript_source
        }
def is_valid_youtube_url(url):
    """ 
    Determine if a string of url is a valid YouTube URL by attempting to fetch video info using the yt_dlp package.

    :param url: string of url to be validated.
    :return: boolean where true if the url is valid, false otherwise.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            # Try to fetch the video info. If this succeeds, the URL is valid.
            ydl.extract_info(url, download=False)
            return True
        except youtube_dl.utils.DownloadError:
            # If youtube_dl raises a DownloadError, the URL is not valid.
            return False
        except youtube_dl.utils.ExtractorError:
            # If youtube_dl raises an ExtractorError, the URL is not valid.
            return False
        except Exception as e:
            # If any other exception occurs, print the exception and assume the URL is not valid.
            print(f"ERROR in is_valid_youtube_url occurred: {e}")
            return False
def create_youtube_md(url, title_or_path=None):  # unittests 3 APICALL + 1 APIMOCK
    """
    Generates a markdown file containing metadata, chapters, description, and transcript from a YouTube video.

    :param url: string of the url to be processed.
    :param title_or_path: string of the title or path for the markdown file, defaults to None.
    :return: string of the path to the created markdown file.
    """
    from primary.fileops import create_full_path, set_metadata_field
    from primary.fileops import write_metadata_and_content, add_timestamp_links
    
    if not is_valid_youtube_url(url):
        raise ValueError(f"VALUE ERROR - invalid YouTube URL: {url}")

    if title_or_path is None:
        title_or_path, _ = get_youtube_title_length(url)
    
    default_folder = "data/audio_inbox"
    suffix_ext = "_yt.md"
    yt_md_file_path = create_full_path(title_or_path, suffix_ext, default_folder)

    yt_info_dict = get_youtube_all(url)
    yt_content = "## content\n\n"
    if yt_info_dict['chapters']:
        yt_content += "### chapters (youtube)\n\n" + '\n'.join([f"{chap['start_time']} - {chap['title']}" for chap in yt_info_dict['chapters']])
        yt_content += "\n\n"
    yt_content += "### description (youtube)\n\n" + yt_info_dict['description'] + "\n\n"
    yt_content += "### transcript (youtube)\n\n" + yt_info_dict['transcript']

    yt_metadata = "## metadata\n"  # below fields are inserted above
    date_today = datetime.now().strftime("%m-%d-%Y")  # Assign today's date in format MM-DD-YYYY
    yt_metadata = set_metadata_field(yt_metadata, 'last updated', date_today + ' Created')  # Updates last updated
    yt_metadata = set_metadata_field(yt_metadata, 'link', url)
    yt_metadata = set_metadata_field(yt_metadata, 'youtube title', yt_info_dict['title'])
    yt_metadata = set_metadata_field(yt_metadata, 'youtube transcript source', yt_info_dict['transcript source'])
    yt_metadata = set_metadata_field(yt_metadata, 'length', yt_info_dict['length'])
    
    write_metadata_and_content(yt_md_file_path, yt_metadata, yt_content, overwrite='yes')
    add_timestamp_links(yt_md_file_path)
    return yt_md_file_path
def create_youtube_md_from_file_link(md_file_path):
    """
    Creates a YouTube markdown file from a given file path by extracting the YouTube link from the file's metadata.
    
    :param md_file_path: string of the path to the markdown file containing the YouTube link in its metadata.
    :return: string of the path to the created YouTube markdown file.
    """
    from primary.fileops import sub_suffix_in_str, read_metadata_and_content, read_metadata_field_from_file
    suffix_new = '_yt'

    metadata, _ = read_metadata_and_content(md_file_path)
    if metadata is None:
        raise ValueError("VALUE ERROR - metadata is None")

    metadata_result = read_metadata_field_from_file(md_file_path, "link")  # returns a tuple (line num, field val)
    if metadata_result is None or metadata_result[1] is None:
        raise ValueError(f"VALUE ERROR - 'link' metadata field is missing or None in the file: {md_file_path}")
    _, link = metadata_result
    yt_file_path = sub_suffix_in_str(md_file_path, suffix_sub=suffix_new)
    #print(f"DEBUG: before create call {yt_file_path}")
    yt_file_path = create_youtube_md(link, yt_file_path)  # creates and returns the same file_path so the assignment is not needed but do it in case there is a bug and a different file_path is returned
    #print(f"DEBUG: after create call {yt_file_path}")
    return yt_file_path
def extract_feature_from_youtube_md(yt_md_file_path, feature):
    """
    Extracts a specified feature from a YouTube markdown file and returns it as a string.

    :param yt_md_file_path: string of the path to the markdown file from which the feature is to be extracted.
    :param feature: string of the feature to be extracted (e.g., 'chapters', 'description', 'transcript').
    :return: string of the extracted text under the specified feature
    """
    try:
        with open(yt_md_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        feature_section_found = False
        extracted_feature = ""
        feature_heading_pattern = re.compile(r'^#+\s*' + re.escape(feature), re.IGNORECASE)  # Pattern to match any level of markdown heading for the feature

        for line in lines:
            if feature_heading_pattern.match(line) or feature_section_found:
                if line.strip().startswith('#') and feature_section_found:
                    break
                feature_section_found = True
                if not feature_heading_pattern.match(line):  # Do not include the heading line in the extracted feature
                    extracted_feature += line
        if not feature_section_found or extracted_feature == "":
            warnings.warn(f"Feature '{feature}' not found in YouTube markdown file.")
            return None
        else:
            return extracted_feature.strip() + '\n\n'
    except Exception as e:
        raise ValueError(f"Error extracting {feature} from {yt_md_file_path}: {e}")
    
### DEEPGRAM AND JSON (6,232 tokens)
from deepgram import DeepgramClient, PrerecordedOptions

def test_deepgram_client():  # omit unittests
    """
    Tests the Deepgram client initialization with the provided API key and prints a success or failure message.
    Raises ValueError if test fails.
    """
    try:
        test_deepgram_client = DeepgramClient(DEEPGRAM_API_KEY)
        if test_deepgram_client:
            print("Successfully created Deepgram Client and accessed the DeepGram API key.")
        else:
            print("Failed to create the Deepgram Client and/or access the DeepGram API key.")
    except Exception as e:
        raise ValueError(f"VALUE ERROR in test of Deepgram client: {e}")
def get_media_length(file_path_or_url):
    """
    Retrieves the length (duration) of a media file or a YouTube video.
    For a local file, it returns the duration in seconds.
    For a YouTube video, it returns the duration in our tuned timestamp format.

    :param file_path_or_url: Path to a local media file or a URL to a YouTube video.
    :return: length (duration) of the media in seconds (for local files) or in our tuned timestamp format (for YouTube videos).
    """
    from primary.fileops import tune_timestamp

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with open(os.devnull, 'w') as fnull:
            sys.stderr = fnull
            try:
                if is_valid_youtube_url(file_path_or_url):
                    _, video_length = get_youtube_title_length(file_path_or_url)
                    return tune_timestamp(video_length)
                elif os.path.isfile(file_path_or_url):
                    # Use mutagen to get the length of the audio file
                    audio = mutagen.File(file_path_or_url)
                    if audio is not None and hasattr(audio.info, 'length'):
                        return tune_timestamp(str(timedelta(seconds=int(audio.info.length))))
                    else:
                        raise ValueError("Could not determine the length of the audio file.")
                else:
                    raise ValueError("Invalid YouTube URL or file path.")
            except Exception as e:
                raise ValueError(f"An error occurred while retrieving media length: {e}")
            finally:
                sys.stderr = sys.__stderr__
def add_link_to_json(json_file_path, link):
    """ 
    Add a hyperlink to the JSON file under the 'metadata' section.

    :param json_file_path: string, the path to the JSON file to be modified.
    :param link: string, the hyperlink to be added to the JSON file.
    :return: tuple, the path to the modified JSON file and None if successful, or None and an exception if an error occurs.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Check if 'metadata' exists in the JSON
        if 'metadata' in data:
            # Add the 'link' field at the top of the 'metadata'
            data['metadata'] = {'link': link, **data['metadata']}
        else:
            # If 'metadata' does not exist, create it
            data['metadata'] = {'link': link}

        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return json_file_path, None
    except Exception as e:
        print(f"Error processing file {json_file_path}: {e}")
        return None, e
def get_link_from_json(json_file_path):
    """ 
    Retrieve the hyperlink from the 'metadata' section of a JSON file.

    :param json_file_path: string, the path to the JSON file from which the hyperlink is to be retrieved.
    :return: string or None, the hyperlink if found in the JSON file's 'metadata' section, otherwise None.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        link = data.get('metadata', {}).get('link', None)
    except Exception as e:
        print(f"Error extracting link from {json_file_path}: {e}")
        link = None
    return link

#TODO rename to add transcribe_deepgram_sync and propagate including to unittests
def transcribe_deepgram(audio_file_path, model):
    """ 
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription, accpets deepgram api call model or our suffix version (see below).
    :return: a dictionary containing the transcription results.
    """
    from primary.fileops import get_current_datetime_humanfriendly, convert_to_epoch_seconds, get_elapsed_seconds, convert_seconds_to_timestamp, convert_timestamp_to_seconds
    MIMETYPES = ['mp3', 'mp4', 'mp2', 'aac', 'wav', 'flac', 'pcm', 'm4a', 'ogg', 'opus', 'webm']  # Supported file types
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    # Check if the file type is supported
    if not any(audio_file_path.endswith(ext) for ext in MIMETYPES):
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    if model == 'nova-2-general':
        suffix = "_nova2gen"
    elif model == 'nova-2-meeting':
        suffix = "_nova2meet"
    elif model == 'enhanced-meeting':
        suffix = "_enhmeet"
    elif model == 'whisper-medium':
        suffix = "_dgwhspm"
    elif model == 'whisper-large':
        suffix = "_dgwhspl"

    else:
        raise ValueError("Invalid or absent DeepGram model ('nova-2-general' 'nova-2-meeting' 'enhanced-meeting' 'whisper-medium' 'whisper-large').")

    json_file_path = None  # Initialize json_file_path to ensure it has a value
    try:
        print(f"Deepgram transcribing model: {model}  file : {audio_file_path}")
        
        with open(audio_file_path, "rb") as file:
            buffer_data = file.read()

        # Extract the file extension and prepare the correct MIME type
        file_extension = audio_file_path.rsplit('.', 1)[1]
        mimetype = f'audio/{file_extension}'

        payload: FileSource = {
            "buffer": buffer_data,
            "mimetype": mimetype,
        }

        # STEP 2: Configure Deepgram options for audio analysis
        options = {
            "punctuate": True, "diarize": True, "model": model, "intents": True, "sentiment": True,
            "summarize": True, "measurements": True, "smart_format": True, "topics": True
        }

        audio_length = get_media_length(audio_file_path)
        start_time = get_current_datetime_humanfriendly()
        print(f"Start Syncronous Deepgram Transcription at {start_time} for audio length of {audio_length}")
        # STEP 3: Call the transcribe_file method with the text payload and options
        # Use a timeout to prevent the write operation from timing out
        try:
            # Use the Deepgram client to transcribe the audio file
            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options, timeout=30*60)
            print("Response received successfully.")
            print('\n'.join(str(response).splitlines()[:5]))  # Print only the first five lines of the response JSON
        except Exception as e:
            print(f"An error occurred: {e}")
        
        elapsed_time = get_elapsed_seconds(convert_to_epoch_seconds(start_time))
        transcribe_time_ratio = int(round(elapsed_time / convert_timestamp_to_seconds(audio_length)*100))
        print(f"Elapsed time is {convert_seconds_to_timestamp(elapsed_time)} which is {transcribe_time_ratio}% of the audio length")
        
        # STEP 4: Save the response as a JSON file
        response_json = response.to_json(indent=4)
        json_file_path = audio_file_path.rsplit('.', 1)[0] + suffix + '.json'
        with open(json_file_path, "w") as json_file:
            json_file.write(response_json)
        print(f"Transcription saved to {json_file_path}")
        #audio_duration = get_youtube_title_length(url)
        # TODO fill in code to print elapsed
    except Exception as e:
        print(f"Error during transcription: {e}")
    return json_file_path

def transcribe_deepgram_sdk_prerecorded(audio_file_path, model):
    """
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model, utilizing the SDK.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :return: path to the JSON file containing the transcription results.
    """
    from primary.fileops import get_current_datetime_humanfriendly, convert_to_epoch_seconds, get_elapsed_seconds, convert_seconds_to_timestamp, convert_timestamp_to_seconds

    MIMETYPES = ['mp3', 'mp4', 'mp2', 'aac', 'wav', 'flac', 'pcm', 'm4a', 'ogg', 'opus', 'webm']
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    if not any(audio_file_path.endswith(ext) for ext in MIMETYPES):
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    model_suffix_map = {
        'nova-2-general': "_nova2gen",
        'nova-2-meeting': "_nova2meet",
        'enhanced-meeting': "_enhmeet",
        'whisper-medium': "_dgwhspm",
        'whisper-large': "_dgwhspl"
    }

    if model not in model_suffix_map:
        raise ValueError("Invalid or absent DeepGram model.")

    suffix = model_suffix_map[model]
    json_file_path = None

    try:
        print(f"Deepgram transcribing model: {model}  file : {audio_file_path}")

        with open(audio_file_path, "rb") as audio:
            source = {'buffer': audio, 'mimetype': f'audio/{audio_file_path.rsplit(".", 1)[1]}'}

        options = PrerecordedOptions(
            model=model,
            punctuate=True,
            diarize=True,
            intents=True,
            sentiment=True,
            summarize=True,
            measurements=True,
            smart_format=True,
            topics=True
        )

        audio_length = get_media_length(audio_file_path)
        start_time = get_current_datetime_humanfriendly()
        print(f"Start Synchronous Deepgram Transcription at {start_time} for audio length of {audio_length}")

        response = deepgram.transcription.sync_prerecorded(source, options)
        print("Response received successfully.")
        print('\n'.join(str(response).splitlines()[:5]))

        elapsed_time = get_elapsed_seconds(convert_to_epoch_seconds(start_time))
        transcribe_time_ratio = int(round(elapsed_time / convert_timestamp_to_seconds(audio_length)*100))
        print(f"Elapsed time is {convert_seconds_to_timestamp(elapsed_time)} which is {transcribe_time_ratio}% of the audio length")

        json_file_path = audio_file_path.rsplit('.', 1)[0] + suffix + '.json'
        with open(json_file_path, "w") as json_file:
            json.dump(response, json_file, indent=4)
        print(f"Transcription saved to {json_file_path}")

    except Exception as e:
        print(f"Error during transcription: {e}")

    return json_file_path


#TODO create APICALL and APIMOCK unittests
#TODO update with options and other stuff from sync version AND FIX THE MODEL PROBLEM!!
#TODO add model to return tuple
def transcribe_deepgram_callback(audio_file_path, model, callback_url):
    """
    Transcribes the given audio file using the specified Deepgram model asynchronously with a callback URL.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :param callback_url: URL to which Deepgram will send the transcription results.
    :return: Request ID from Deepgram indicating that the file has been accepted for processing.
    """
    from primary.fileops import get_current_datetime_humanfriendly

    # Supported MIME types mapping
    MIMETYPES = {
        'mp3': 'audio/mpeg',
        'mp4': 'audio/mp4',
        'wav': 'audio/wav',
        'flac': 'audio/flac',
        # add other supported formats as necessary
    }

    file_extension = audio_file_path.rsplit('.', 1)[1]
    if file_extension not in MIMETYPES:
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    mimetype = MIMETYPES[file_extension]

    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': mimetype
    }

    # Set up the query parameters with the callback URL
    params = {
        'callback': callback_url,
        # 'punctuate': True, # it works if this line is commented out
        # 'diarize': True,  # it works if this line is commented out
        'model': model
    }

    with open(audio_file_path, 'rb') as file:
        audio_data = file.read()

    audio_length = get_media_length(audio_file_path)
    start_time = get_current_datetime_humanfriendly()
    print(f"Start Callback Deepgram Transcription at {start_time} for audio length of {audio_length}")
        
    response = post(
        url='https://api.deepgram.com/v1/listen',
        headers=headers,
        params=params,
        data=audio_data
    )

    # Adjusted to accept both 200 and 202 status codes as successful
    if response.status_code in (200, 202):        
        callback_response = response.json()
        request_id = callback_response.get('request_id', 'NO REQUEST_ID FIELD FOUND IN JSON')
        if request_id == 'NO REQUEST_ID FIELD FOUND IN JSON':
            print(f"Deepgram Callback FAIL - {request_id}")
        else:
            print(f"Deepgram Callback SUCCESS - request_id: {request_id}")
        base_audio_file_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        return (request_id, base_audio_file_name, model)

    else:
        raise Exception(f"Failed to submit audio: {response.text}, Status Code: {response.status_code}")




        # json_data = response.json()
        # with open('tests/test_manual_files/1min youttube/155500a5-83f5-4b56-a4bb-372aa25a29b2.json', 'r') as file:
        #     json_data = json.load(file)

        # request_id = json_data.get('request_id', 'NO REQUEST_ID FIELD FOUND IN JSON')
        # created_timestamp = json_data.get('created', 'NO CREATED FIELD FOUND IN JSON')

        # s3_bucket = 'fofpublic'
        # s3_path = 'deepgram-transcriptions'
        # cur_s3_object_name = f"{request_id}.json"
        # json_data = get_s3_json(s3_bucket, cur_s3_object_name, s3_path)
        # print(f"First characters of received JSON:\n\n{json.dumps(json_data)[:500]}")

        # created_timestamp = json_data.get('metadata', {}).get('created', 'NO CREATED FIELD FOUND IN JSON').replace(':', '').split('.')[0]
        
        # new_s3_object_name = f"{base_audio_file_name}_{created_timestamp}.json"
        # #rename_s3_object(s3_bucket, old_s3_object_name, new_s3_object_name, s3_path=s3_path)
        # return new_s3_object_name
def transcribe_deepgram_callback2(audio_file_path, model, callback_url):
    """
    Transcribes the given audio file using the specified Deepgram model asynchronously with a callback URL.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :param callback_url: URL to which Deepgram will send the transcription results.
    :return: Request ID from Deepgram indicating that the file has been accepted for processing.
    """
    from primary.fileops import get_current_datetime_humanfriendly
    import os

    # Supported MIME types mapping
    MIMETYPES = {
        'mp3': 'audio/mpeg',
        'mp4': 'audio/mp4',
        'wav': 'audio/wav',
        'flac': 'audio/flac',
    }

    file_extension = audio_file_path.rsplit('.', 1)[1]
    if file_extension not in MIMETYPES:
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    mimetype = MIMETYPES[file_extension]

    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': mimetype
    }

    # Set up the query parameters with the callback URL
    params = {
        'callback': callback_url,
        #'punctuate': True,
        #'diarize': True,
        'model': model,
    }

    with open(audio_file_path, 'rb') as file:
        audio_data = file.read()

    audio_length = get_media_length(audio_file_path)
    start_time = get_current_datetime_humanfriendly()
    print(f"Start Callback Deepgram Transcription at {start_time} for audio length of {audio_length}")

    try:
        response = post(
            url='https://api.deepgram.com/v1/listen',
            headers=headers,
            params=params,
            data=audio_data,
        )
    except exceptions.SSLError as ssl_err:
        print(f"SSL error: {ssl_err}")
        raise
    except exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
        raise

    if response.status_code in (200, 202):
        callback_response = response.json()
        request_id = callback_response.get('request_id', 'NO REQUEST_ID FIELD FOUND IN JSON')
        if request_id == 'NO REQUEST_ID FIELD FOUND IN JSON':
            print(f"Deepgram Callback FAIL - {request_id}")
        else:
            print(f"Deepgram Callback SUCCESS - request_id: {request_id}")
        base_audio_file_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        return (request_id, base_audio_file_name, model)
    else:
        raise Exception(f"Failed to submit audio: {response.text}, Status Code: {response.status_code}")
#TODO come back and review this to troubleshoot deepgram whisper transcription
def transcribe_deepgram_OLD_fixhang(file_path, timeout_duration=1*60*60):
    json_file_path = None
    progress_thread = None
    stop_event = threading.Event()
    try:
        if file_path.endswith(MIMETYPE):
            print(f"Starting Deepgram transcription at {get_current_time_str()}")

            # Print the size of the file in MB
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"File size: {file_size_mb:.2f} MB")

            # Start the progress thread with the stop event
            progress_thread = threading.Thread(target=print_progress, args=(timeout_duration, stop_event))
            progress_thread.start()

            with open(file_path, "rb") as f:
                source = {"buffer": f, "mimetype": 'audio/' + MIMETYPE}

                # Start the transcription process
                print(f"Deepgram transcribing file: {file_path}")
                print("Progress: ", end="")

                res = dg.transcription.sync_prerecorded(source, dg_options)

                # Signal the progress thread to stop
                stop_event.set()

                json_file_path = file_path[:-4] + dg_suffix + '.json'
                with open(json_file_path, "w") as transcript:
                    json.dump(res, transcript, indent=4)
                print(f"\nDeepgram transcribe successful on file: {file_path}")
        else:
            print(f"File {file_path} does not end with {MIMETYPE}")
    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        # Signal the progress thread to stop and ensure it is stopped
        if progress_thread is not None:
            stop_event.set()
            progress_thread.join(timeout=0)
    return json_file_path
def get_summary_start_seconds(data, index):
    """ 
    Retrieves the start time in seconds of a word from the transcription data at the given index.

    :param data: dictionary of the transcription data.
    :param index: integer of the index of the word to find the start time for.
    :return: integer of the start time in seconds of the specified word, rounded down to the nearest whole number.
    """
    words_list = data.get('results', {}).get('channels', [])[0].get('alternatives', [])[0].get('words', [])
    if index < len(words_list):
        return math.floor(words_list[index].get('start', 0))
    return 0
def format_feature_segment(feature, segment, data):
    """
    Formats a segment of a feature with a timestamp and additional info.

    :param feature: string, the feature being extracted.
    :param segment: dict, the segment of the feature to be formatted.
    :param data: dict, the JSON data from the Deepgram file.
    :return: string, the formatted segment.
    """
    from primary.fileops import convert_seconds_to_timestamp

    singular_feature_json = feature[:-1]  # Remove the last character to make it singular as found in the JSON
    singular_feature_print = singular_feature_json.capitalize()  # Capitalize the singular form for printing
    segment_text = segment.get('text', '')
    segment_start_index = int(segment.get('start_word', 0))
    segment_start_secs = get_summary_start_seconds(data, segment_start_index)
    segment_timestamp = convert_seconds_to_timestamp(segment_start_secs)
    segment_midline = ""

    if feature.lower() == "summaries":
        singular_feature_json = 'summary'
        singular_feature_print = singular_feature_json.capitalize()
        segment_text = segment.get(singular_feature_json, '')
    elif feature.lower() == "sentiments":
        sentiment = segment.get('sentiment')
        sentiment_score = segment.get('sentiment_score')
        segment_midline = f"{sentiment} - sentiment_score = {sentiment_score:.2f}"
    elif feature.lower() == "topics":
        # Assuming there's only one topic per segment, hence index [0]
        topic_info = segment.get('topics', [{}])[0]
        topic_name = topic_info.get('topic')
        confidence_score = topic_info.get('confidence_score')
        segment_midline = f"{topic_name} - confidence_score = {confidence_score:.2f}"
    elif feature.lower() == "intents":
        # Assuming there's only one intent per segment, hence index [0]
        intent_info = segment.get('intents', [{}])[0]
        intent_name = intent_info.get('intent')
        confidence_score = intent_info.get('confidence_score')
        segment_midline = f"{intent_name} - confidence_score = {confidence_score:.2f}"

    formatted_segment = f"{singular_feature_print}  {segment_timestamp}\n"
    if segment_midline:
        formatted_segment += f"{segment_midline}\n"
    formatted_segment += f"{segment_text}\n\n"

    return formatted_segment
def extract_feature_from_deepgram_json(json_file_path, feature):
    """
    Extract a specific feature section from a Deepgram JSON file and return it as a string.

    :param json_file_path: string of the path to the JSON file from which the feature is to be extracted.
    :param feature: string of the feature of the section to be extracted.
    :return: string of the extracted text under the specified feature, preceded by the feature itself (no pound signs) and a blank line.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        extracted_text = ''
        if feature == "summaries":
            summaries = data.get('results', {}).get('channels', [])[0].get('alternatives', [])[0].get(feature, [])
            #print(f"DEBUG summaries {summaries}")
            for summary in summaries:
                extracted_text += format_feature_segment(feature, summary, data)
        elif feature in ["sentiments", "topics", "intents"]:
            segments = data.get('results', {}).get(feature, {}).get('segments', [])
            #print(f"DEBUG {feature} {segments}")
            for segment in segments:
                extracted_text += format_feature_segment(feature, segment, data)
        else:
            warnings.warn(f"in extract_feature_from_deepgram_json - Feature '{feature}' not found in Deepgram JSON")
            return None

        if extracted_text:
            return f"{extracted_text.strip()}\n\n"
        else:
            warnings.warn(f"in extract_feature_from_deepgram_json - Feature '{feature}' was found in Deepgram JSON but extracted text is None or empty string (should not get this warning!)")
            return None
    except Exception as e:
        raise ValueError(f"Error extracting {feature} from {json_file_path}: {e}")
def validate_transcript_json(json_file_path):
    """
    Validates the structure of a JSON file to ensure it contains specific keys and types.

    :param json_file_path: string of the path to the JSON file to be validated.
    :return: boolean, True if the JSON structure is as expected, False otherwise.
    """
    if not os.path.exists(json_file_path):
        raise ValueError(f"The file path does not exist for {json_file_path}.")
    
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Access the nested structure with checks for KeyError and TypeError
        results = data.get("results")
        if results is None:
            raise KeyError("results key not found")

        channels = results.get("channels")
        if not isinstance(channels, list) or not channels:
            raise TypeError("channels is not a non-empty list")

        alternatives = channels[0].get("alternatives")
        if not isinstance(alternatives, list) or not alternatives:
            raise TypeError("alternatives is not a non-empty list")

        words_data = alternatives[0].get("words")
        if not isinstance(words_data, list) or len(words_data) <= 1:
            raise ValueError("The list of words is empty or has only one word.")

        paragraphs_data = alternatives[0].get("paragraphs")
        if paragraphs_data is None:
            raise KeyError("paragraphs key not found")

        transcript = paragraphs_data.get("transcript", "").strip()
        if not transcript:
            raise ValueError("The transcript in paragraphs is empty.")

        paragraphs_list = paragraphs_data.get("paragraphs")
        if not isinstance(paragraphs_list, list) or not paragraphs_list:
            raise ValueError("There are no paragraphs in paragraphs.")

    except (KeyError, TypeError, ValueError) as e:
        print(f"Error occurred with file {json_file_path}: {str(e)}")
        return False

    return True
def set_various_transcript_headings(file_path, feature, source):
    """
    Sets the transcript heading in a file based on the extracted feature from a specified source.

    :param file_path: string of the path to the file where the heading is to be set.
    :param feature: string of the feature to extract and use as the heading.
    :param source: string of the source from which to extract the feature ('deepgram' or 'youtube').
    :return: None.
    """
    from primary.fileops import set_heading, add_suffix_in_str, remove_all_suffixes_in_str, find_file_in_folders  # seems to be needed for unittest, see Claude thread

    folder_paths = ["data/f_c9_done_json_yt_host"]     
    if source == "deepgram":
        dg_json_file_path = file_path.replace('.md', '.json')
        if not os.path.isfile(dg_json_file_path):
            dg_json_file_path = find_file_in_folders(dg_json_file_path, folder_paths)
            if dg_json_file_path is None:
                raise ValueError(f"No companion deepgram json file found for {file_path}")
        extracted_feature_text = extract_feature_from_deepgram_json(dg_json_file_path, feature)
    elif source == "youtube":
        yt_md_file_path = add_suffix_in_str(remove_all_suffixes_in_str(file_path), "_yt")
        if not os.path.isfile(yt_md_file_path):
            yt_md_file_path = find_file_in_folders(yt_md_file_path, folder_paths)
            if yt_md_file_path is None:
                raise ValueError(f"No companion youtube md file found for {file_path}")
        extracted_feature_text = extract_feature_from_youtube_md(yt_md_file_path, feature)
    else:
        raise ValueError("source invalid")
    if extracted_feature_text is None:
        return

    set_heading(file_path, extracted_feature_text, "### " + feature)

### NUMERAL CONVERT (3,614 tokens)
def extract_context(line, match, context_radius):
    """ 
    Extracts a context window around a regex match within a string of text.

    :param line: string of text containing the match.
    :param match: regex match object containing the start and end positions of the match within the line.
    :param context_radius: integer specifying the number of words around the match to include in the context window.
    :return: string of text representing the context window around the match.
    """
 
    if match is None:
        raise ValueError("Match not found")

    # Define the number of words around the match to include in the context
    words = line.split()
    match_word_index = None

    # Find the index of the word that contains the match
    for index, word in enumerate(words):
        if match.start() >= line.find(word) and match.end() <= line.find(word) + len(word):
            match_word_index = index
            break

    if match_word_index is None:
        raise ValueError("Match not found within the words of the line")

    # Calculate the start and end indices for the context window
    context_start = max(match_word_index - context_radius, 0)
    context_end = min(match_word_index + context_radius + 1, len(words))

    # Extract the context window from the line
    context_window = ' '.join(words[context_start:context_end])
    return context_window
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
    match = re.search(re.escape(match_str), line)
    if match:
        exception_msg = f"Excluding conversion for {exception_type} at line {line_number+1+num_metadata_lines}: ...{extract_context(line, match, 5)}..."
        if exception_msg not in printed_exceptions:
            print(exception_msg)
            printed_exceptions.append(exception_msg)
    # DEBUG CODE to check if certain words are in english_vocab
    # debug_words = ["Like", "And", "Orca", "Shirley", "FTGSTKLOMNB"]
    # for word in debug_words:
    #     print(f"Is '{word}' in common_english_vocab? {'yes' if word.lower() in common_english_vocab else 'no'}")
def get_previous_word(substring, start_index):
    """ 
    Finds the word in a string that precedes the given start index.

    :param substring: the string from which to extract the previous word.
    :param start_index: the index in the string to start searching backward from.
    :return: the word found before the start index, or an empty string if no word is found.
    """
    # Find the last non-space character before the start_index
    word_end = start_index
    while word_end > 0 and substring[word_end-1].isspace():
        word_end -= 1
    # Find the start of the word
    word_start = word_end
    while word_start > 0 and not substring[word_start-1].isspace():
        word_start -= 1
    # Return the word found, if any
    return substring[word_start:word_end] if word_start != word_end else ""
def previous_word_exception(word, common_english_vocab, additional_exception_words):
    """ 
    Determines if a word is an exception based on its presence in additional exceptions or English vocabulary.

    :param word: the word to check for exception status.
    :param common_english_vocab: a set of common English words to compare against.
    :param additional_exception_words: a set of words that are always considered exceptions.
    :return: True if the word is an exception, False otherwise.
    """
    if word.lower() in additional_exception_words:
        #print(f"DEBUG: '{word}' before the number is in the additional exception list.")
        return True
    if word.istitle() and word.lower() not in common_english_vocab:
        #print(f"DEBUG: Capitalized '{word}' before the number is not in common English vocabulary.")
        return True
    return False
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
    num_subs_total = 0
    current_index = 0
    additional_exception_words = ["step"]
    while current_index < len(line):
        if line[current_index].isdigit():
            # Check if the digit is adjacent to any characters that are not digits or allowed punctuation
            if (current_index > 0 and not line[current_index-1] in '0123456789.,?! \n') or \
               (current_index < len(line) - 1 and not line[current_index+1] in '0123456789.,?! \n'):
                # Search forward until a space or a new line is found
                while current_index < len(line) and not line[current_index] in ' \n':
                    current_index += 1
                continue
            # Skip conversion if the digit is part of a decimal number (e.g., "1.0")
            if current_index < len(line) - 1 and not line[current_index+1].isdigit() and \
               current_index + 2 < len(line) and line[current_index+2].isdigit():
                current_index += 3  # Skip past the decimal point and the following digit(s)
                while current_index < len(line) and (line[current_index].isdigit() or line[current_index].isspace() or line[current_index] in '.,!?'):
                    current_index += 1
                continue
            # Check if the character directly before the number is a period, then skip conversion
            if current_index > 0 and line[current_index-1] == '.':
                    current_index += 2  # Skip past the period and the decimal point
                    while current_index < len(line) and line[current_index].isdigit():
                        current_index += 1
                    continue
            # Skip conversion if the number starts the line or is preceded only by whitespace and followed by a period and a space
            if (current_index == 0 or (current_index > 0 and line[:current_index].isspace())) and \
               (current_index + 1 < len(line) and line[current_index+1] == '.' and \
                (current_index + 2 < len(line) and line[current_index+2] == ' ')):
                current_index += 3  # Skip past the period and the space
                continue
            end_index = current_index + 1
            while end_index < len(line) and line[end_index].isdigit():
                end_index += 1
            number_str = line[current_index:end_index]
            if number_str == num_str:
                previous_word = get_previous_word(line, current_index)
                if not previous_word_exception(previous_word, common_english_vocab, additional_exception_words):
                    new_line, num_subs = re.subn(r'\b' + re.escape(num_str) + r'\b', num2words(num), line[current_index:], 1)
                    num_subs_total += num_subs
                    line = line[:current_index] + new_line
                    current_index = end_index
                else:
                    print_num_exception(line[current_index:end_index], line_number, num_metadata_lines, printed_exceptions, "proper name", line)
            current_index = end_index
        else:
            current_index += 1
    return line, num_subs_total
    # old comment - need to fix $3zero - found in FloodLAMP_Demo13_Plate_v1.md 'It cost about $30, but super helpful.'
def convert_num_line_capitalization(line, num, num_str):
    """ 
    Capitalize the numeral word at the beginning of a sentence or after punctuation.

    :param line: the line of text in which to perform capitalization.
    :param num: the numerical value to convert to words.
    :param num_str: the string representation of the number to find in the line.
    :return: a tuple containing the modified line and the total number of substitutions made.
    """
    num_subs_total = 0
    for punctuation in ['.', '?', '!']:
        # Include comma in the lookahead assertion
        pattern = r'(^|[' + re.escape(punctuation) + r']\s)' + re.escape(num_str) + r'(?=[\s,]|$)'
        new_line, num_subs = re.subn(pattern, lambda match: match.group(1) + num2words(num).capitalize(), line)
        num_subs_total += num_subs
        if num_subs > 0:
            line = new_line
    return line, num_subs_total
def skip_speaker_line_with_timestamp(line):
    """ 
    Determine if a line contains a single timestamp with max_words before the timestamp less that get_timestamp default val (8) and is therefore a speaker line to skip.

    :param line: The line of text to be checked for a timestamp.
    :return: boolean where True if a timestamp is found, otherwise False.
    """
    from primary.fileops import get_timestamp
    timestamp_result = get_timestamp(line)
    return timestamp_result and any(value is not None for value in timestamp_result)
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
    num_subs_total = 0
    for i, line in enumerate(lines):
        if skip_speaker_line_with_timestamp(line):
            continue  # Skip lines with timestamps
        line, num_subs = convert_num_line_capitalization(line, num, num_str)
        num_subs_total += num_subs
        if num_subs > 0 and verbose:
            print(f"  convert in line {i+1+num_metadata_lines} the number: {num}")
        line, num_subs = convert_num_line_lowercase(line, num, num_str, i, num_metadata_lines, printed_exceptions, common_english_vocab)
        num_subs_total += num_subs
        lines[i] = line  # Update the line in lines
    return lines, num_subs_total
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
    lines = content.split('\n')  # Break the content into lines
    num_subs_total = 0  # Initialize counter for the number of conversions
    printed_exceptions = []  # Initialize a list to keep track of printed exceptions
    for num in list(range(num_limit)) + additional_numbers:  # Loop over all numbers from 0 to 9 and additional numbers
        num_str = str(num)  # Convert the number to a string
        lines, num_subs = convert_num_lines(lines, num, num_str, num_metadata_lines, print_output, printed_exceptions)
        num_subs_total += num_subs
        #print(f"Convert number {num} with conversions: {num_subs}")
    return '\n'.join(lines), num_subs_total
def convert_ordinals_in_content(content, punct_capitalization):
    """ 
    Converts ordinal numbers in a string of text to their word equivalents and capitalizes words following specified punctuation.

    :param content: string of text containing ordinal numbers and punctuation.
    :param punct_capitalization: list of punctuation characters after which the following word should be capitalized.
    :return: string of text with ordinal numbers converted and words capitalized as specified.
    """

    ordinal_map = {
        '1st': 'first', '2nd': 'second', '3rd': 'third', '4th': 'fourth',
        '5th': 'fifth', '6th': 'sixth', '7th': 'seventh', '8th': 'eighth',
        '9th': 'ninth'
    }
    converted_content = content
    for ordinal, word in ordinal_map.items():
        converted_content = re.sub(r'\b' + re.escape(ordinal) + r'\b', word, converted_content)
    # Capitalize where necessary
    for punctuation in punct_capitalization:
        pattern = r'(^|[' + re.escape(punctuation) + r']\s)(\w)'
        converted_content = re.sub(pattern, lambda match: match.group(1) + match.group(2).upper(), converted_content)
    return converted_content
    # DONE fill in code to change "1st" to "first", "2nd" to "second", etc. up to "9th"
    # DONE fill in code to capilatize when needed as is done in @convert_nums_to_words
def convert_nums_to_words(file_path, verbose=False):
    """
    Converts numerals in the content of a file to their corresponding words, appends a specified suffix to the filename, and creates a new file with the converted content.

    :param file_path: string of the path to the original file.
    :param verbose: boolean for printing verbose messages. Defaults to False.
    :return: string of the path to the newly created file with the converted content.
    """
    from primary.fileops import read_file_flex, write_metadata_and_content, verbose_print

    num_limit = 10  # number up to which will be converted plus any additional numbers
    additional_numbers = [1000000, 1000000000, 1000000000000]
    metadata, content = read_file_flex(file_path)
    
    # Handle case where metadata is None (no metadata in file)
    num_metadata_lines = 0 if metadata is None else len(metadata.splitlines())
    
    content = convert_ordinals_in_content(content, ['.', '?', '!'])
    converted_content, num_subs_total = convert_numbers_in_content(content, num_limit, additional_numbers, num_metadata_lines, verbose)

    verbose_print(verbose, "Review and fix manually: addresses")
    verbose_print(verbose, f"END convert_nums_to_words - Conversion Count: {num_subs_total}\n")
    write_metadata_and_content(file_path, metadata, converted_content, overwrite='yes')
    return file_path  # Return the path of the modified file

### SPEAKER NAMES (2,285 tokens)
def read_speaker_names_from_json(json_file_path):
    """ 
    Reads speaker names from a JSON file's metadata, which have been inserted by us and are not in the raw deepgram json files.

    :param json_file_path: string of the path to the JSON file.
    :return: list of speaker names if they exist, otherwise an empty list.
    """ 
    if not os.path.exists(json_file_path):
        raise ValueError(f"The file path does not exist for {json_file_path}.")
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Return the speaker_names if they exist in the metadata
    return data.get('metadata', {}).get('speaker_names', [])
def write_speaker_names_to_json(json_file_path, speaker_names, verbose=False):
    """ 
    Writes speaker names to a JSON file's metadata. Overwrites file.

    :param json_file_path: string of the path to the JSON file.
    :param speaker_names: list of strings containing speaker names.
    :return: None.
    """ 
    from primary.fileops import verbose_print

    if not os.path.exists(json_file_path):
        raise ValueError(f"The file path does not exist for {json_file_path}.")
    # Read the existing JSON file's content
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Initialize a flag to check if speaker_names have been updated
    speaker_names_updated = False

    # Check if 'metadata' exists and if 'speaker_names' is present
    if 'metadata' in data and 'speaker_names' in data['metadata']:
        # If the new speaker_names are different from the existing ones, update them
        if data['metadata']['speaker_names'] != speaker_names:
            data['metadata']['speaker_names'] = speaker_names
            speaker_names_updated = True
    else:
        # If 'metadata' does not exist or 'speaker_names' is not present, create 'metadata' with speaker_names
        data.setdefault('metadata', {}).update({'speaker_names': speaker_names})
        speaker_names_updated = True

    # Write the modified data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    # Print a statement to the console if the speaker_names have been updated
    if speaker_names_updated:
        verbose_print(verbose, f"Speaker names in the JSON have been updated.")
    else:
        verbose_print(verbose, f"Speaker names in the JSON are unchanged.")
def find_unassigned_speakers(md_file_path, verbose=False):
    """ 
    Identifies speakers in the markdown file who do not have assigned names.
    This is determined by if the line has a valid timestamp and then looking for 'Speaker X' before the timestamp.

    :param md_file_path: string of the path to the markdown file.
    :return: list of strings of unassigned speaker names, or None if all speakers are assigned.
    """
    from primary.fileops import verbose_print, get_timestamp
    
    if not os.path.exists(md_file_path):
        raise ValueError(f"The file path does not exist for {md_file_path}.")

    unassigned_speaker_numbers = []
    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            timestamp_index = get_timestamp(line)
            if timestamp_index:
                # Search for unnamed speaker pattern before the timestamp
                match = re.search(r"Speaker\s+(\d+)", line[:timestamp_index[1]])
                if match:
                    speaker_number = int(match.group(1))
                    if speaker_number not in unassigned_speaker_numbers:
                        unassigned_speaker_numbers.append(speaker_number)

    # Sort the list of unassigned speaker numbers
    unassigned_speaker_numbers.sort()

    # Convert the sorted list of numbers to the required string format
    unassigned_speakers = [f"Speaker {number}" for number in unassigned_speaker_numbers]

    num_unassigned = len(unassigned_speakers)
    if num_unassigned > 0:
        verbose_print(verbose, f"From find_unassigned_speakers - Number of speakers not assigned names: {num_unassigned}. Speaker names: {' '.join(unassigned_speakers)}")
        return unassigned_speakers
    else:
        verbose_print(verbose, f"From find_unassigned_speakers - All speakers have been assigned names.")
        return None
    # DONE fill in code to find all speakers without names assigned ('Speaker X') using code similar to @propagate_speaker_names_throughout_md
    # DONE fill in code to print the number of speakers not assigned followed by the specific speaker numbers, as a single print line
    # DONE return a list of the unassigned speaker numbers or NONE
#TODO think this is done but double check - change to propagate the speaker assignment backwards as well as forwards in the Markdown file.
def propagate_speaker_names_throughout_md(md_file_path, input_speaker_names=None):
    """
    Propagates speaker names throughout a markdown file based on provided input names or existing assignments.

    :param md_file_path: string of the path to the markdown file.
    :param input_speaker_names: list of tuples with speaker numbers and names, if available.
    :return: list of tuples with speaker numbers and names after propagation.
    """
    from primary.fileops import get_timestamp

    # Initialize speaker names list based on input
    speaker_names = input_speaker_names.copy() if input_speaker_names else []

    # Read the content of the markdown file
    with open(md_file_path, 'r') as file:
        content = file.readlines()

    updated_content = []
    for i, line in enumerate(content):
        # Extract timestamp index from the line
        _, index = get_timestamp(line, max_words=10)
        if index is not None:
            # Search for speaker name assignment before the timestamp
            match = re.search(r"Speaker\s+(\d+)\s*=\s*(.+)", line[:index])
            if match:
                speaker_num, name = match.groups()
                speaker_num = int(speaker_num)  # Ensure speaker number is an integer
                name = name.strip()
                # Add new speaker name if not already in the list
                if (speaker_num, name) not in speaker_names:
                    speaker_names.append((speaker_num, name))
                # Update the line with the speaker name and timestamp
                line = f"{name}  {line[index:].lstrip()}"
            else:
                # Replace speaker placeholders with names throughout the document
                for spkr_num, spkr_name in speaker_names:
                    line = re.sub(rf"\bSpeaker {spkr_num}\b\s*", f"{spkr_name}  ", line)

        updated_content.append(line)

    # After the forward pass, perform a backward pass to propagate names to earlier mentions
    for i in range(len(updated_content) - 1, -1, -1):
        line = updated_content[i]
        _, index = get_timestamp(line, max_words=10)
        if index is not None:
            for spkr_num, spkr_name in speaker_names:
                line = re.sub(rf"\bSpeaker {spkr_num}\b\s*", f"{spkr_name}  ", line)
            updated_content[i] = line    

    # Write the updated content back to the markdown file
    with open(md_file_path, 'w') as file:
        file.writelines(updated_content)

    # Sort the speaker names by speaker number for consistency
    speaker_names.sort(key=lambda x: x[0])
    return speaker_names
def iterate_input_speaker_names(md_file_path, input_speaker_names=None):
    """
    Iterates over input speaker names and updates the markdown file until the user decides to exit.

    :param md_file_path: string of the path to the markdown file.
    :param input_speaker_names: list of tuples with speaker numbers and names, if available.
    :return: list of tuples with speaker numbers and names after all iterations.
    """
    if not os.path.exists(md_file_path):
        raise ValueError(f"The file path does not exist for {md_file_path}.")

    overall_speaker_names = input_speaker_names.copy() if input_speaker_names else []

    while True:
        current_speaker_names = propagate_speaker_names_throughout_md(md_file_path, overall_speaker_names)
        
        for speaker_name in current_speaker_names:
            if speaker_name not in overall_speaker_names:
                overall_speaker_names.append(speaker_name)
        
        overall_speaker_names.sort(key=lambda x: x[0])
        
        if not overall_speaker_names:
            print("No Speaker Names")
        else:
            print("Current speaker_names:")
            for num, name in overall_speaker_names:
                print(f"Speaker {num}: {name}")
        
        continue_prompt = input("\nASSIGN SPEAKER NAMES NOW - hit enter to continue or E/exit to exit: ").strip().lower()
        if continue_prompt == '':
            continue
        elif continue_prompt in ['e', 'exit']:
            unassigned_speakers = find_unassigned_speakers(md_file_path)
            if unassigned_speakers:
                print("Unassigned speakers:")
                for spkr in unassigned_speakers:
                    print(f"  {spkr}")
            else:
                print("All speakers have been assigned.")
            print("\nAssigned speaker names:")
            for num, name in overall_speaker_names:
                print(f"  Speaker {num}: {name}")
            return overall_speaker_names
        else:
            print("Invalid input. Please either hit enter to continue or type 'E'/'Exit' to exit.")
def assign_speaker_names(md_file_path):
    """
    Assigns speaker names to markdown file by reading from a corresponding JSON file, updating, and writing back to the json if changed.
    Prompts the user iteratively through assigning the names.
    
    :param md_file_path: string of the path to the markdown file.
    :return: None
    """
    json_file_path = md_file_path.replace('.md', '.json')
    try:
        with open(json_file_path, 'r') as file:
            # Check if there is a corresponding JSON file
            speaker_names = read_speaker_names_from_json(json_file_path)
    except FileNotFoundError:
        # If the JSON file does not exist, start with an empty list
        speaker_names = []

    # Iterate over speaker_names and update them
    updated_speaker_names = iterate_input_speaker_names(md_file_path, speaker_names)

    # Check if the updated speaker_names are different from the original ones
    if updated_speaker_names != speaker_names:
        # Write the updated speaker_names back to the JSON file
        write_speaker_names_to_json(json_file_path, updated_speaker_names)

### TRANSCRIBE WRAPPER (1,479 tokens)
def create_transcript_md_from_json(json_file_path, combine_segs=True):
    """
    Creates a markdown transcript from a JSON file containing Deepgram transcription data.
    If combine_segs is True, combines consecutive segments from the same speaker.

    :param json_file_path: string of the path to the json file containing transcription data.
    :param combine_segs: boolean indicating whether to combine consecutive segments from the same speaker.
    :return: string of the path to the created markdown file or None if the json file is not valid.
    """
    from primary.fileops import create_initial_metadata, convert_seconds_to_timestamp, set_metadata_field
    from primary.fileops import write_metadata_and_content, add_timestamp_links
    
    md_file_path = json_file_path[:-5] + ".md"
    link = get_link_from_json(json_file_path)
    lines = []

    if not validate_transcript_json(json_file_path):
        return None

    with open(json_file_path, "r") as file:
        data = json.load(file)
        model_name = data["metadata"]["model_info"][list(data["metadata"]["model_info"].keys())[0]]["name"]
        paragraph_data = data["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]

        # Initialize current paragraph information
        curr_speaker = None
        curr_timestamp = None
        curr_transcript = ""

        for para in paragraph_data:
            speaker_id = str(para['speaker'])  # Keep speaker_id as string
            speaker = f'Speaker {speaker_id}'

            start_timestamp = convert_seconds_to_timestamp(para['start'])

            # Extract sentences from paragraph and join them
            sentences = para.get('sentences', [])
            transcript = ' '.join(sentence.get('text', '') for sentence in sentences)

            if combine_segs and speaker == curr_speaker:
                # If combine_segs is True and the speaker is the same as the previous paragraph, continue accumulating the transcript
                curr_transcript += " " + transcript
            else:
                # If it's a new speaker, write the accumulated transcript to lines, then reset curr_speaker, curr_timestamp, and curr_transcript
                if curr_transcript:
                    # Add speaker, timestamp and transcript to lines
                    lines.extend([curr_speaker + '  ' + curr_timestamp, curr_transcript, ''])
                curr_speaker = speaker
                curr_timestamp = start_timestamp
                curr_transcript = transcript

        # Write the last paragraph to lines
        if curr_transcript:
            lines.extend([curr_speaker + '  ' + curr_timestamp, curr_transcript, ''])

    content = "## content\n\n### transcript\n\n" + "\n".join(lines)
    print(f"DEBUG - content: {content}")
    metadata = create_initial_metadata()
    date_today = datetime.now().strftime("%m-%d-%Y") # Assign today's date in format MM-DD-YYY
    metadata = set_metadata_field(metadata, 'last updated', date_today + ' Created')  
    metadata = set_metadata_field(metadata, 'link', link)
    metadata = set_metadata_field(metadata, 'transcript source', 'deepgram '+model_name)
    
    write_metadata_and_content(md_file_path, metadata, content, overwrite='yes')
    convert_nums_to_words(md_file_path)
    add_timestamp_links(md_file_path)
    return md_file_path
def process_deepgram_transcription(title, link, model, audio_inbox_path="data/audio_inbox"):  # unittests 1 TEMP SKIPPED
    """
    Processes a Deepgram transcription from a YouTube video link by downloading the audio, transcribing it, and creating a markdown transcript.

    :param title: the title of the video used to name the downloaded audio file.
    :param link: the YouTube link to the video to be transcribed.
    :param model: the Deepgram model used for transcription.
    :param audio_inbox_path: the directory path where the audio file will be downloaded.
    :return: the path to the created markdown file or None if transcription fails.
    """
    # Download the audio file
    audio_file_path = download_mp3_from_youtube(link, f"{audio_inbox_path}/{title}")
    
    # Transcribe the downloaded audio file
    json_file_path = transcribe_deepgram(audio_file_path, model)
    if json_file_path is None:
        print("transcription failed or the file type is incorrect.")
        return None
    print(json_file_path)

    # Add the YouTube link to the transcription JSON
    add_link_to_json(json_file_path, link)

    # Create a markdown transcript from the JSON file and process it
    md_file_path = create_transcript_md_from_json(json_file_path)
    
    # Assign speaker names to the markdown transcript
    assign_speaker_names(md_file_path)
    
    return md_file_path
def process_deepgram_transcription_from_audio_file(audio_file_path, link, model):  # unittests 1 TEMP SKIPPED
    """ 
    Transcribes an audio file using the Deepgram service, adds the YouTube link to the transcription, creates a markdown transcript, and assigns speaker names.

    :param audio_file_path: string of the path to the audio file to be transcribed.
    :param link: string of the youtube link to be added to the transcription json.
    :param model: string of the deepgram model to be used for transcription.
    :return: string of the path to the markdown file with the completed transcription or None if transcription fails.
    """
    # Transcribe the downloaded audio file
    json_file_path = transcribe_deepgram(audio_file_path, model)
    if json_file_path is None:
        raise ValueError("Transcription failed or the file type is incorrect.")
    # Add the YouTube link to the transcription JSON
    add_link_to_json(json_file_path, link)

    # Create a markdown transcript from the JSON file and process it
    md_file_path = create_transcript_md_from_json(json_file_path)

    # Assign speaker names to the markdown transcript
    assign_speaker_names(md_file_path)

    return md_file_path
def process_multiple_videos(videos_to_process, model='nova-2-general', bool_youtube=True):  # unittests 1 MOCK
    """
    Processes multiple videos by transcribing them and creating YouTube markdown files if bool_youtube is True.

    :param videos_to_process: list of tuples containing the title and link of each video to be processed.
    :param model: string of the deepgram model to be used for transcription. Defaults to 'enhmeet' (deepgram enhanced-meeting) model.
    :param bool_youtube: boolean indicating whether to create YouTube markdown files. Defaults to True.
    :return: None
    """
    for title, link in videos_to_process:
        try:                                             
            cur_md = process_deepgram_transcription(title, link, model)
            if bool_youtube:
                create_youtube_md_from_file_link(cur_md)
        except ValueError as e:
            print(f"Error processing video {title}: {e}")






## primary/llm.py (20,087 tokens)
import sys
import os
import json
import glob
import shutil
import warnings
import requests
import tiktoken
import anthropic
from openai import OpenAI
from termcolor import colored
from tenacity import retry, wait_random_exponential, stop_after_attempt

from config import OPENAI_API_KEY_CONFIG_LLM,  ANTHROPIC_API_KEY_CONFIG_LLM
from primary.fileops import *

import warnings  # Set the warnings to use a custom format
warnings.formatwarning = custom_formatwarning
#USAGE: warnings.warn(f"Insert warning message here")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir) # Add the parent directory to sys.path

os.environ["OPENAI_API_KEY_CONFIG_LLM"] = OPENAI_API_KEY_CONFIG_LLM  # updated 7-20-24 RT as new Project Key (User Keys have been replace by OpenAI for Project Keys but our old User Keys still work)
os.environ['ANTHROPIC_API_KEY'] = ANTHROPIC_API_KEY_CONFIG_LLM

#OpenAI model name - comment one out
#OPENAI_MODEL = "gpt-4o-mini"
OPENAI_MODEL = "gpt-4o-2024-08-06"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"
#NOT IMPLEMENTED YET   ANT_LLM = "claude-3-5-sonnet-20240620"

TOKEN_COST_DICT = {
    'gpt-4o':{'input_token_cost':5, 'output_token_cost':15},  # costs in $/million tokens
    'gpt-4o-2024-08-06':{'input_token_cost':2.5, 'output_token_cost':10},
    'gpt-4o-mini':{'input_token_cost':.15, 'output_token_cost':.6},
     'claude-3-5-sonnet-20240620':{'input_token_cost':3, 'output_token_cost':15}
    }
BLOCK_DELIMITER = '\n---\n'

### PRINT AND TOKENS (2,694 tokens)
def pretty_print_function(messages, tools, print_prompts=False, print_input=True, verbose=False):
    """
    Prints messages with role-specific colors and separates function details for clarity.

    :param messages: list of dictionaries containing message role and content
    :params tools: list of tools, each containing function details, passed to pretty_print_function_descriptions
    :param print_prompts: boolean of whether to print the system prompt and function parameter descriptions, defaults to False
    :param print_input: boolean of whether to print the user input, defaults to True
    :return: a list of the print strings as [print_str_prompts, print_str_input, print_str_responses]
    """
    role_to_color = {
        "system": "red",
        "function parameter descriptions": "yellow",
        "user": "green",
        "assistant": "grey",
        "function responses": "magenta",  # Color for function details
    }
    print_str_prompts = ""
    print_str_input = ""
    print_str_responses = ""

    verbose_print(verbose, f"messages:\n{messages}")
    verbose_print(verbose, f"tools:\n{tools}")

    for index, message in enumerate(messages):
        verbose_print(verbose, f"Message {index + 1} of {len(messages)} messages")
        if message["role"] == "system" and print_prompts:
            print_str_prompts = f"System Prompt: {message['content']}\n"
            print(colored(print_str_prompts, role_to_color[message["role"]]))
            if tools is not None:
                print_str_prompts += pretty_print_function_descriptions(tools, role_to_color["function parameter descriptions"])
        if message["role"] == "user":
            print_str_input = f"User Input:\n{message['content']}\n"
            print(colored(print_str_input, role_to_color[message["role"]]))
        elif message["role"] == "assistant":
            assistant_msg_str = str(message)

            # Find the index where function details start
            function_start_idx = assistant_msg_str.find("'function': ")

            # Split the string into two parts
            assistant_msg_part = assistant_msg_str[:function_start_idx]
            function_msg_part = assistant_msg_str[function_start_idx:]

            # Print the technical assistant info but generally we don't need this so comment out 3-16-24 RT
            #print(colored(f"assistant: {assistant_msg_part}", role_to_color["assistant"]))

            # Process and print the second part (function details) in magenta
            if function_start_idx != -1:
                # Parsing the function details from the string
                function_name_start_idx = function_msg_part.find("'name': '") + len("'name': '")
                function_name_end_idx = function_msg_part.find("'", function_name_start_idx)
                function_name = function_msg_part[function_name_start_idx:function_name_end_idx]

                arguments_str = function_msg_part.split("'arguments': '{", 1)[-1].rstrip("}'}}]")
                arguments_str = arguments_str.replace("\\n", "\n").replace("\\", "").replace('"', '')
                print_str_responses = "Function Parameters Responses:\n"
                for line in arguments_str.split(","):
                    # below is simply to add a space after the colon for reasons I do not understand!
                    key_value = line.split(':', 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        print_str_responses += f"  {key.strip()}: {value.strip()}\n"
                    else:
                        print_str_responses += f"  {line}\n"
                print(colored(print_str_responses, role_to_color["function responses"]))

    return [print_str_prompts, print_str_input, print_str_responses]
def pretty_print_function_descriptions(tools, print_color):
    """
    Print descriptions of functions and their properties from a list of tools.

    :param tools: a list of tools, each containing function details
    :return: a string of function names and descriptions, including properties
    """
    output_str = ""
    for tool in tools:
        if tool["type"] == "function":
            function_name = f"Function Name: {tool['function']['name']}"
            function_description = f"Function Description: {tool['function']['description']}"
            output_str += function_name + "\n" + function_description + "\n"
            print(colored(output_str, print_color))
            output_str += "Function Parameter Descriptions:\n"
            print(colored("Function Parameter Descriptions:", print_color))
            output_str += '\n'  # add newline so string matches terminal print
            
            # Extract and print each function's properties with descriptions, appending them to the output string.
            properties = tool['function']['parameters']['properties']
            for prop, details in properties.items():
                prop_description = f"  {prop}: {details['description'].strip()}"
                output_str += prop_description + "\n"
                print(colored(prop_description, print_color))
            
    return output_str
def count_tokens(input_string):  # no unittests
    """
    Counts the number of tokens in a given string using the 'cl100k_base' encoding.

    :param input_string: string of text to be tokenized.
    :return: integer representing the number of tokens in the input string.
    """
    encoding = tiktoken.get_encoding('cl100k_base')
    token_count = len(encoding.encode(input_string))
    return token_count
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
    if output_tokens_ratio != 0 and output_tokens_fixed != 0:
        raise ValueError("output_tokens_ratio and output_tokens_fixed cannot both be non zero")
    
    # Default chunking function: read the entire file as a single chunk
    def default_chunking(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return [file.read()]

    # Use the provided chunking function or the default one
    chunks = (chunking_function or default_chunking)(file_path, *chunking_function_args)

    # Setting up variables
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0
    input_token_cost = token_cost_dict[model]['input_token_cost']
    output_token_cost = token_cost_dict[model]['output_token_cost']
    prompt_tokens = count_tokens(prompt)
    
    # Main loop
    for chunk in chunks:
        input_tokens = prompt_tokens
        chunk_input = count_tokens(chunk)
        input_tokens += chunk_input
        if output_tokens_fixed > 0:
            output_tokens = output_tokens_fixed
        else:
            output_tokens = chunk_input * output_tokens_ratio
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens

    total_input_cost = (total_input_tokens / 1000000) * input_token_cost
    total_output_cost = (total_output_tokens / 1000000) * output_token_cost
    total_cost = total_input_cost + total_output_cost

    if verbose:
        print(file_path)
        print(f"File input tokens: {total_input_tokens:,} (Cost: ${input_token_cost:.4f}/1M tokens, Input token cost: ${total_input_cost:.2f})")
        print(f"File output tokens: {total_output_tokens:,} (Cost: ${output_token_cost:.4f}/1M tokens, Output token cost: ${total_output_cost:.2f})")
        print(f"File cost: ${total_cost:.2f}\n\n")

    return total_input_cost, total_output_cost, total_cost, total_input_tokens
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
    total_input_cost = 0
    total_output_cost = 0
    total_cost = 0
    total_input_tokens = 0
    
    file_paths = get_files_in_folder(corpus_path, suffix_include=suffix_include, suffix_exclude=suffix_exclude, include_subfolders=include_subfolders)
    
    for file_path in file_paths:
        file_input_cost, file_output_cost, file_cost, input_tokens = cost_llm_on_file(file_path, prompt, model, token_cost_dict, verbose, chunking_function, chunking_function_args, output_tokens_ratio, output_tokens_fixed)
        total_input_cost += file_input_cost
        total_output_cost += file_output_cost
        total_cost += file_cost
        total_input_tokens += input_tokens
    
    print(f"\nCorpus Summary for {corpus_path}")
    print(f"Corpus input cost: {total_input_cost:.2f}")
    print(f"Corpus output cost: {total_output_cost:.2f}")
    print(f"Corpus total cost: ${total_cost:.2f}")
    print(f"Corpus total files: {len(file_paths)}, total input tokens: {total_input_tokens:,}\n")

    return total_input_cost, total_output_cost, total_cost
def add_token_counts_to_headings(text):
    """
    Adds token counts to markdown headings in the given text.

    :param text: string, the text content to process.
    :return: string, the text with token counts added to headings.
    """
    updated_lines = []
    for line in text.split('\n'):
        if re.match(r'^#{1,6}\s', line):
            heading = line.strip()
            heading_text = find_heading_text(text, heading)
            if heading_text:
                start, end = heading_text
                section_content = text[start:end]
                token_count = count_tokens(section_content)
                formatted_count = f"{token_count:,}"
                updated_line = f"{line} ({formatted_count} tokens)"
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    
    result = '\n'.join(updated_lines)
    total_tokens = count_tokens(result)
    
    # Add total token count to the first line
    first_line, *rest = result.split('\n', 1)
    result = f"{first_line} ({total_tokens:,} tokens)\n" + (rest[0] if rest else "")
    return result


### SPLIT FILES (2,381 tokens)
def get_line_numbers_with_match(file_path, match_str):
    """
    Retrieve line numbers from a file where the line matches a given string exactly after stripping.

    :param file_path: path to the file to be searched
    :param match_str: string of text to match on each line
    :return: list of line numbers where the match_str is found
    """
    # Check if the original file exists and is valid
    if not os.path.isfile(file_path):
        raise ValueError(f"The file path does not exist or is invalid for {file_path}.")
    
    line_numbers = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if line.strip() == match_str:
                line_numbers.append(line_number)
    
    return line_numbers
def get_speaker_segments(file_path, skip_string='SKIPQA'):
    """
    Extract segments from a file that do not contain a specific skip string, or all segments if skip string is None.

    :param file_path: string of the path to the file to be processed
    :param skip_string: string of the substring used to identify segments to skip, or None to include all segments
    :return: list of segments without the skip string, or all segments if skip string is None
    """
    transcript = get_heading(file_path, heading="### transcript")
    transcript = transcript.lstrip('### transcript').rstrip('\n').lstrip('\n*')
    
    segments = transcript.split("\n\n")
    if skip_string is not None:
        segments = [segment.strip() for segment in segments if skip_string not in segment]
    else:
        segments = [segment.strip() for segment in segments]
    
    return segments
def count_segment_tokens(file_path, skip_string='SKIPQA'):
    """
    Count tokens in each segment of a file and provide token statistics.

    :param file_path: string of the path to the file to be processed
    :param skip_string: string of the substring used to identify segments to skip
    :return: tuple containing (list of segments, list of token counts)
    """
    segments = get_speaker_segments(file_path, skip_string)
    segment_tokens = [count_tokens(segment) for segment in segments]
    
    total_tokens = sum(segment_tokens)
    max_tokens = max(segment_tokens)
    
    print(f"Total tokens in the file: {total_tokens:,}  x 4 for characters: {4*total_tokens:,}")
    print(f"Number of segments in the file: {len(segments)}")
    print(f"Maximum tokens in any segment: {max_tokens:,}  x 4 for characters: {4*max_tokens:,}")
    
    return segment_tokens
def plot_segment_tokens(file_path):
    """
    Create a horizontal bar chart plot of token counts for each segment and save it as a PNG file.

    :param file_path: string of the path to the file to be processed
    :return: string of the path to the saved PNG file
    """
    import matplotlib.pyplot as plt
    
    segments = get_speaker_segments(file_path)
    segment_tokens = count_segment_tokens(file_path)
    
    plt.figure(figsize=(15, 10))
    y_pos = range(len(segment_tokens))
    plt.barh(y_pos, segment_tokens)
    
    total_tokens = sum(segment_tokens)
    max_tokens = max(segment_tokens)
    num_segments = len(segment_tokens)
    
    plt.title(f"Token Distribution in Segments\n\n{file_path}\n\n"
              f"Maximum tokens in any segment: {max_tokens}\n"
              f"Number of segments: {num_segments}\n"
              f"Total tokens: {total_tokens}\n\n", loc='left', fontweight='bold', fontsize=14)
    
    plt.ylabel("Segment Index")
    plt.xlabel("Token Count")
    
    # Invert y-axis to have zero at the top
    plt.gca().invert_yaxis()

    # Save the plot as a PNG file
    base_name = os.path.basename(file_path).rsplit('.', 1)[0]
    output_path = os.path.join('logs', 'plots', f'Token_count_{base_name}.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

    # Open the file using VS Code
    import subprocess
    subprocess.run(['code', output_path])

    print(f"Token count of segments plot saved to: {output_path}")
    return output_path
def group_segments_select_speaker(segments, speaker):
    """
    Groups consecutive segments not containing the specified speaker's name and selects segments where the speaker's name is found before the timestamp.
    Calls get_timestamp from fileops.py to determine if the first line in a segment is a speaker line.

    :param segments: list of text segments to be processed
    :param speaker: string of the speaker's name to select segments
    :return: list of text segments where the speaker's name is found before the timestamp
    """
    from primary.fileops import get_timestamp

    final_segments = []
    temp_segments = []
    for segment in segments:
        first_line = segment.split('\n', 1)[0]  # Extract the first line of the segment
        timestamp, index = get_timestamp(first_line)
        # Check if the speaker's name is in the portion of the first line before the timestamp index
        if timestamp is not None and speaker in first_line[:index]:
            temp_segments.append(segment)
            final_segments.append('\n\n'.join(temp_segments))
            temp_segments = []
        else:
            temp_segments.append(segment)
    
    # Check if the last temp_segments should be added
    if temp_segments:
        last_segment_first_line = temp_segments[-1].split('\n', 1)[0]
        timestamp, index = get_timestamp(last_segment_first_line)
        if timestamp is not None and speaker in last_segment_first_line[:index]:
            final_segments.append('\n\n'.join(temp_segments))
    
    return [segment for segment in final_segments if segment.strip()]
def group_segments_token_cap(segments, token_cap=2000):
    """
    Groups consecutive segments without exceeding the token_cap, without splitting segments.
    Includes segments that exceed the token_cap as individual blocks.

    :param segments: list of text segments to be processed
    :param token_cap: integer of maximum number of tokens, using words = .75 tokens
    :return: list of grouped text segments without exceeding the token_cap, including oversized segments as individual blocks
    """
    final_segments = []
    temp_segments = []
    current_token_count = 0
    word_cap = token_cap / 0.75

    for segment in segments:
        words_in_segment = len(segment.split())
        if words_in_segment > word_cap:
            # If there are any segments in temp_segments, add them to final_segments
            if temp_segments:
                final_segments.append('\n\n'.join(temp_segments))
                temp_segments = []
                current_token_count = 0
            # Add the oversized segment as an individual block
            final_segments.append(segment)
        else:
            if current_token_count + (words_in_segment * 0.75) > token_cap:
                # If adding the segment would exceed the token cap, finalize the current group
                final_segments.append('\n\n'.join(temp_segments))
                temp_segments = [segment]
                current_token_count = words_in_segment * 0.75
            else:
                # Otherwise, add the segment to the current group
                temp_segments.append(segment)
                current_token_count += words_in_segment * 0.75

    # Add any remaining segments in temp_segments to final_segments
    if temp_segments:
        final_segments.append('\n\n'.join(temp_segments))

    return [segment for segment in final_segments if segment.strip()]
def split_file_select_speaker(file_path, speaker, skip_string='SKIPQA', suffix_new='_blocks'):
    """
    Add block delimiters to a file, with a block for every segment by the selected speaker and other segments grouped together.

    :param file_path: path to the file to be processed
    :param speaker: the speaker whose sections will be delimited
    :param skip_string: string to identify speaker segments to skip
    :param suffix_new: suffix for the new file with block delimiters
    :return: file_path of new file with separator delimiters ("---") with suffix_new='_blocks' by default
    """
    from primary.fileops import read_metadata_and_content, write_metadata_and_content

    metadata, _ = read_metadata_and_content(file_path)
    segments = get_speaker_segments(file_path, skip_string)
    #print(f"\nDEBUG separate segments: {segments}")
    grouped_segments = group_segments_select_speaker(segments, speaker)
    # if final_segments:
    #     print(f"DEBUG: First element of final_segments: {repr(final_segments[0][:100])}")
    new_content = "## content\n\n" + BLOCK_DELIMITER.join(grouped_segments)  # Using the global variable BLOCK_DELIMITER  
    return write_metadata_and_content(file_path, metadata, new_content, suffix_new, overwrite='no')
def split_file_every_speaker(file_path, skip_string=None, suffix_new='_blocks'):
    """
    Add block delimiters to a file with one block per speaker segment regardless of speaker.

    :param file_path: path to the file to be processed
    :param skip_string: string to identify speaker segments to skip
    :param suffix_new: suffix for the new file with block delimiters
    :return: file_path of new file with separator delimiters ("---") with suffix_new='_blocks' by default
    """
    from primary.fileops import read_metadata_and_content, write_metadata_and_content

    metadata, _ = read_metadata_and_content(file_path)
    segments = get_speaker_segments(file_path, skip_string)
    #print(f"\nDEBUG separate segments: {segments}")
    new_content = "## content\n\n" + BLOCK_DELIMITER.join(segments)  # Using the global variable BLOCK_DELIMITER  
    return write_metadata_and_content(file_path, metadata, new_content, suffix_new, overwrite='no')
def split_file_token_cap(file_path, token_cap, skip_string='SKIPQA', suffix_new='_blocks'):
    """
    Add block delimiters to a file with one block per speaker segment regardless of speaker.

    :param file_path: path to the file to be processed
    :param token_cap: integer of maximum number of tokens, using words = .75 tokens
    :param skip_string: string to identify speaker segments to skip
    :param suffix_new: suffix for the new file with block delimiters
    :return: file_path of new file with separator delimiters ("---") with suffix_new='_blocks' by default
    """
    from primary.fileops import read_metadata_and_content, write_metadata_and_content

    metadata, _ = read_metadata_and_content(file_path)
    segments = get_speaker_segments(file_path, skip_string)
    #print(f"\nDEBUG separate segments: {segments}")
    grouped_segments = group_segments_token_cap(segments, token_cap)
    new_content = "## content\n\n" + BLOCK_DELIMITER.join(grouped_segments)  # Using the global variable BLOCK_DELIMITER  
    return write_metadata_and_content(file_path, metadata, new_content, suffix_new, overwrite='no')


### OPENAI LLM (1,047 tokens)
def test_openai_chat(model=OPENAI_MODEL):# DS, cat 5, unittests 2 APIMOCK
    """
    Sends a predefined message to the OpenAI chat API and prints the response.

    :param model: string of the model name to be used for the chat completion request
    :return: None
    """
    try:
        messages = [{"role": "user", "content": "Tell me a knock knock joke about science."}]
        response = openai_chat_completion_request(messages, model=model)
        if response:
            print("API chat response:", response.text)
    except Exception as e:
        print(f"Failed to access the OpenAI API: {e}")
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def openai_chat_completion_request(messages, tools=None, tool_choice=None, model=OPENAI_MODEL):  # APIMOCK unittests 2
    """
    Send a chat completion request to the OpenAI API with the provided messages and optional tools and tool choice.

    :param messages: a list of message dictionaries to send in the chat completion request
    :param tools: optional list of tools to include in the request
    :param tool_choice: optional tool choice to include in the request
    :param model: the model to use for the chat completion request
    :return: the response object from the OpenAI API request
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY_CONFIG_LLM,  # Use the imported API key instead of this way "openai.api_key,"
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate OpenAI Chat Completion response")
        print(f"Exception: {e}")
        return e
#TODO: refactor so calls openai_chat_completion_request, rename
def simple_openai_chat_completion_request(prompt, model):  # no unittests
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY_CONFIG_LLM,  # Use the imported API key instead of this way "openai.api_key,"
    }

    messages = [{"role": "user", "content": prompt}]

    json_data = {"model": model, "messages": messages}
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        response_json = response.json()
        return str(response_json['choices'][0]['message']['content'])
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return str(e)
#The comment about concatenating a boolean with a string is incorrect.
#The function is not attempting to concatenate verbose (a boolean) with a string.
#The issue mentioned is not present in this code.

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
    messages = [{"role": "system", "content": fcall_prompt}, {"role": "user", "content": content}]
    verbose_print(verbose, f"OPENAI_MODEL = {model}")
    chat_response = openai_chat_completion_request(messages, tools=tools, model=model)

    verbose_print(verbose, f"Response Status Code: {chat_response.status_code}")
    verbose_print(verbose, f"Response Text: {chat_response.text}")

    assistant_message = None  # Initialize to None or a sensible default
    try:
        assistant_message = chat_response.json()["choices"][0]["message"]
        messages.append({"role": "assistant", "content": assistant_message})
        if verbose:
            pretty_print_function(messages, tools)
        # print(f"DEBUG openai_function_call print full messages:\n {messages}")
    except Exception as e:
        print(f"Error parsing response: {e}")
    return assistant_message


### ANTHROPIC LLM (658 tokens)
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
    # Initialize the client
    client = anthropic.Anthropic()

    # Prepare the request parameters
    request_params = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    # Add system message if provided
    if system:
        request_params["system"] = system

    # Add messages if provided, otherwise raise an exception
    if messages:
        request_params["messages"] = messages
    else:
        raise ValueError("No messages were provided for Anthropic chat completion request.")

    try:
        # Make the API call
        message = client.messages.create(**request_params)

        # Return the content of the message
        return message.content[0].text
    except anthropic.APIError as e:
        print(f"Anthropic API error: {str(e)}")
    except anthropic.APIConnectionError as e:
        print(f"Error connecting to Anthropic API: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    
    return None
def simple_anthropic_chat_completion_request(prompt, model=ANTHROPIC_MODEL):
    """
    Make a simple chat completion request to Anthropic's API.

    :param prompt: String containing the user's prompt or message
    :param model: String specifying the Anthropic model to use (default: "claude-3-opus-20240229")
    :return: String containing the generated message content, or an error message if the request fails
    """
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": os.environ['ANTHROPIC_API_KEY'],
        "anthropic-version": "2023-06-01"
    }

    json_data = {
        "model": model,
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_json = response.json()
        return str(response_json['content'][0]['text'])
    except requests.exceptions.RequestException as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return str(e)


### LLM PROCESSING (2,412 tokens)
#TODO clean up 'prompt' terminology so system prompt is properly distinguished
def llm_process_block(block, prompt, provider="openai"):
    """
    Processes a single block of text with a given prompt using the OpenAI chat completion API.

    :param block: string of the text block to be processed.
    :param prompt: string of the prompt to use for the chat completion request.
    :param provider: string indicating the LLM provider (default is "openai").
    :return: string of the processed text block or None if no valid response is received.
    """
    if provider == "openai":
        messages = [{"role": "system", "content": prompt}, {"role": "user", "content": block}]
        print("OPENAI LLM = " + OPENAI_MODEL)
        chat_response = openai_chat_completion_request(messages)

        if chat_response.status_code == 200:
            response_json = chat_response.json()
            #print(f"DEBUG llm_process_block print full response_json:\n {response_json}")
            if 'choices' in response_json and len(response_json['choices']) > 0:
                return response_json['choices'][0]['message']['content']
            else:
                print("No 'choices' in response or 'choices' list is empty.")
                return None
        else:
            print(f"Request failed with status code {chat_response.status_code}: {chat_response.text}")
            return None
    else:
        raise ValueError(f"Provider '{provider}' is not set up yet.")

#TODO Figure out what the right metadata and content function does as suffix new is passed with an empty string. See chat history and test it
#TODO consider adding boolean to keep speaker lines
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
    from primary.fileops import read_metadata_and_content, write_metadata_and_content
    
    if mode not in ['replace', 'append']:
        raise ValueError("mode must be 'replace' or 'append'.")

    metadata, content = read_metadata_and_content(blocks_file_path)
    content = content.lstrip("## content\n\n")
    blocks = content.split(BLOCK_DELIMITER)

    processed_blocks = []
    print(f"BLOCKS TO PROCESS WITH SIMPLE LLM CALL: {len(blocks)}\n")
    print(colored(f"Simple LLM Call Prompt: {prompt}\n", "red"))

    for i, block in enumerate(blocks):
        print(f"\n\nBlock number: {i+1}")
        llm_response = llm_process_block(block, prompt, provider)
        if llm_response:
            if mode == 'replace':
                processed_blocks.append(llm_response)
            elif mode == 'append':
                processed_blocks.append(block + "\n" + llm_response)
            print(colored("User Input:", "green"))
            print(colored(block, "green"))
            print(colored("LLM Response:", "blue"))
            print(colored(llm_response, "blue"))
        else:
            print("No response received for block.")
    print(colored(f"\nSingle LLM call prompt: {prompt}\n", "red"))
    
    new_content = '## content\n\n'
    new_content += '\n\n'.join(processed_blocks) if not retain_delimiters else BLOCK_DELIMITER.join(processed_blocks)
    return write_metadata_and_content(blocks_file_path, metadata, new_content, suffix_new, overwrite='no-sub')

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
    return llm_process_file_blocks(blocks_file_path, prompt, suffix_new, 'replace', provider=provider, retain_delimiters=retain_delimiters)

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
    return llm_process_file_blocks(blocks_file_path, prompt, suffix_new, 'append', provider=provider, retain_delimiters=retain_delimiters)

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
    from primary.fileops import delete_file

    # Call the block separation function without 'retain_delimiters'
    # Make a shallow copy of kwargs without 'retain_delimiters' for the separation function
    separation_kwargs = {key: value for key, value in kwargs.items() if key != 'retain_delimiters'}
    blocks_file_path = split_file_function(file_path, *args, **separation_kwargs)

    # Prepare kwargs for scall_replace or scall_append, including 'retain_delimiters'
    llm_kwargs = kwargs.copy()
    llm_kwargs['retain_delimiters'] = kwargs.get('retain_delimiters', False)

    if mode == "replace":
        llm_file_path = scall_replace(blocks_file_path, prompt, suffix_new=suffix_new, provider=provider, **llm_kwargs)
    elif mode == "append":
        llm_file_path = scall_append(blocks_file_path, prompt, suffix_new=suffix_new, provider=provider, **llm_kwargs)
    else:
        raise ValueError("mode must be 'replace' or 'append'.")
    delete_file(blocks_file_path)
    return llm_file_path


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

### COPYEDITS (1,671 tokens)
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
#TODO need to test - not tested after removing ffop code
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
    from primary.fileops import delete_file
    
    blocks_file_path = split_file_function(file_path, *args, **kwargs)
    copyedit_file_path = scall_replace(blocks_file_path, prompt, retain_delimiters=True, suffix_new='_llmce')
    delete_file(blocks_file_path)
    return copyedit_file_path

### TRANSCRIPT TRANSITIONS (1,666 tokens)
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
    from primary.fileops import read_metadata_and_content, write_metadata_and_content

    metadata, content = read_metadata_and_content(blocks_file_path)
    content = content.lstrip("## content\n\n")
    blocks = content.split(BLOCK_DELIMITER)
    modified_blocks = []

    for i, block in enumerate(blocks):
        # Extract context from the preceding and following blocks
        prev_context = ' '.join(blocks[max(0, i-1)].split()[-num_adjacent_words:]) if i > 0 else ''
        # TODO modify this to use a yet-to-be-created is_speaker_line function (work w and without timestamps) to skip the speaker line if it's there, for now just add 3
        next_context = ' '.join(blocks[min(len(blocks)-1, i+1)].split()[:num_adjacent_words+3]) if i < len(blocks)-1 else ''
        
        # Concatenate the context with the current block, ensuring two new lines between contexts and the block
        augmented_block = f"{prev_context}\n\nTARGET SEGMENT\n{block}\n\n{next_context}".strip()
        modified_blocks.append(augmented_block)

    # Join modified blocks with delimiters
    new_content = "## content\n\n" + BLOCK_DELIMITER.join(modified_blocks)  

    # Overwrite the file with the modified content
    write_metadata_and_content(blocks_file_path, metadata, new_content, overwrite='yes')
    print(f"Modified block file with adjacent words for block file: {blocks_file_path}")
#TODO need to test - not tested after removing ffop code
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
    mod_blocks_file_with_adjacent_words(blocks_file_path, adjacent_words)
    return llm_process_file_blocks(blocks_file_path, prompt, suffix_new, 'replace', retain_delimiters)
#TODO need to test - not tested after removing ffop code
def create_transitions_file(file_path, split_file_function, prompt, *args, **kwargs):
    """
    Creates a file with transitions between blocks processed by a language model based on a given prompt.

    :param file_path: string of the path to the original file
    :param split_file_function: function used to separate the original file into blocks
    :param prompt: string of the prompt to process each block with
    :return: string of the path to the transitions file
    """
    from primary.fileops import delete_file
    adjacent_words = 10

    blocks_file_path = split_file_function(file_path, *args, **kwargs)
    transitions_file_path = scall_replace_adjacent_words(blocks_file_path, prompt, adjacent_words, retain_delimiters=True, suffix_new='_transitions')
    delete_file(blocks_file_path)
    return transitions_file_path

### QA GENERATION (5,479 tokens)
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
#TODO modify to use the FCALL_PROMPT_QA_DIALOGUE_FROMANSWER above
def tools_qa_speaker(speaker):  # no unittests
    """
    Generate a list of tools for question and answer extraction based on the speaker's response.

    :param speaker: string of the speaker's name whose responses are being analyzed
    :return: list of dictionaries containing tool configurations for QA extraction
    """
    return[
{
    "type": "function",
    "function": {
        "name": "get_qa",
        "description": "Extract and modify a question into a generic form and provide the exact verbatim answer from a transcript",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description":f"""
                    The question should capture the essence of the original query posed by the interviewer in a simplified, generic form. It should focus on the core topic or idea, removing extraneous contextual details. The modified question should have semantic alignment with {speaker}'s answer. The question should be rephrased for a third-person audience, ensuring it is generalized and does not include direct references to {speaker}. DO NOT mention the name {speaker} in the question.
                    """ , 
                },
                "timestamp": {
                    "type": "string",
                    "description": f"""
                    The timestamp corresponding to the start of {speaker}'s response in the format H:MM:SS or MM:SS or M:SS (chose whichever is present in the input text). This timestamp is crucial for contextualizing the answer within the transcript and must be accurate to reflect the exact moment the response begins.
                    """, 
                },
            },
            "required": ["question","timestamp"], 
        },
    },
    },
    ]
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
    from primary.fileops import read_metadata_and_content, add_timestamp_links
    from primary.fileops import sub_suffix_in_str, set_last_updated, write_metadata_and_content

    print("***Running fcall_qa on file: " + block_file_path)
    
    metadata, block_content = read_metadata_and_content(block_file_path)
    metadata = set_last_updated(metadata, 'Created QA')

    blocks = block_content.split(BLOCK_DELIMITER)

    print(f"QA BLOCKS TO PROCESS: {len(blocks)}\n")
    print(colored(f"System Prompt: {fcall_prompt}\n", "red"))
    pretty_print_function_descriptions(tools_qa_speaker(speaker), "red")
    
    qa_content = "## content\n\n"
    for i, block in enumerate(blocks):
        print(f"\n\nQA BLOCK NUMBER: {i+1}")
        qa_response = openai_function_call(fcall_prompt, block, tools_qa_speaker(speaker)) # Finish function to return textual output 
        
        # Extract the 'arguments' field from the function call
        arguments_json = qa_response['tool_calls'][0]['function']['arguments']

        # Attempt to parse the JSON
        try:
            arguments = json.loads(arguments_json)
            question = arguments['question']
            timestamp = arguments['timestamp']
            answer = block[block.rfind(')') + 1:].strip()

        except json.decoder.JSONDecodeError as e:
            print("JSONDecodeError:", e)
        # Extract the question and answer

        qa_content += f"QUESTION: {question}\nTIMESTAMP: {timestamp}\nANSWER: {answer}\nEDITS: \nTOPICS: \nSTARS: \n\n"

    qa_file_path = write_metadata_and_content(block_file_path, metadata, qa_content, suffix_new)
    print("QA written to " + qa_file_path)
    add_timestamp_links(qa_file_path)
    print("Timestamp Links added.")
    print(colored(f"System Prompt: {fcall_prompt}\n", "red"))
    pretty_print_function_descriptions(tools_qa_speaker(speaker), "red")
    return qa_file_path
def create_qa_file_select_speaker(file_path, speaker, fcall_prompt):
    """
    Processes a _prepqa file to generate QA question and answer blocks using OpenAI LLM function calling.

    :param file_path: string of the path to the _prepqa transcript file to be processed.
    :param speaker: string of the speaker's name to be used in processing.
    :return: None.
    """    
    blocks_file_path = split_file_select_speaker(file_path, speaker)
    qa_file_path = fcall_qa_speaker(blocks_file_path, speaker, fcall_prompt)
    delete_file(blocks_file_path)
    return qa_file_path

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
    return [{
        "type": "function",
        "function": {
            "name": "extract_qa",
            "description": "Extract and clarify the next question-answer pair from an FDA Town Hall transcript chunk",
            "parameters": {
                "type": "object",
                "properties": {
                    "clarified_question": {
                        "type": "string",
                        "description": "A clear, concise version of the next question given the context of the provided previous question and answer block, even if this next question overlaps with the previous answer. Remove filler words and improving readability of the question. If no explicit question is asked in the entirity of the transcrtipt text provided, analyze the text to determine if important information provided by an Authority Speaker. If so, then generate an appropriate question based on the important information. The entire text of this next question should be on a single line.",
                    },
                    "clarified_answer": {
                        "type": "string",
                        "description": "A clear, concise version of the answer to the next question, removing filler words and improving readability. Must maintain the same meaning as the verbatim answer but may rephrase for clarity. The entire text of this answer should be on a single line.",
                    },
                    "verbatim_question": {
                        "type": "string",
                        "description": "The exact text corresponding to the next question as it appears in the transcript, excluding the speaker line and any newline characters. If no explicit question is asked, use the string 'IMPLIED QUESTION'. The entire text should be on a single line.",
                    },
                    "verbatim_answer": {
                        "type": "string",
                        "description": "The exact answer as it appears in the transcript, including any filler words or hesitations, but excluding the speaker line and any newline characters. The entire text should be on a single line.",
                    },
                    "speaker_question": {
                        "type": "string",
                        "description": "The name or role of the person asking the question, as identified in the transcript by the text in the speaker line that precedes a colon or timestamp. Do not use a different name spelling that may appear in the speaker dialogue. If the question is implied from an Authority Speaker's statement, use 'NONE'.",
                    },
                    "speaker_answer": {
                        "type": "string",
                        "description": "The name and role of the person providing the answer, as identified in the transcript by the text in the speaker line that precedes a colon or timestamp. Do not use a different name spelling that may appear in the speaker dialogue.",
                    },
                    "relative_start_position": {
                        "type": "integer",
                        "description": "The character position in the transcript chunk where the verbatim_question begins, relative to the start of the chunk.",
                    },
                    "relative_end_position": {
                        "type": "integer",
                        "description": "The character position in the transcript chunk where the verbatim_answer ends, relative to the start of the chunk.",
                    },
                    "topics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "A list of 1-3 key topics addressed in the question-answer pair, focusing on technical, procedural, or legal aspects of COVID-19 diagnostics.",
                    },
                    "review_flag": {
                        "type": "boolean",
                        "description": "Set to True if there's any uncertainty about the importance or relevance of the extracted information, or if the content requires additional review. Otherwise, set to False.",
                    }
                },
                "required": ["clarified_question", "clarified_answer", "verbatim_question", "verbatim_answer", "speaker_question", "speaker_answer", "relative_end_position", "topics", "review_flag"]
            }
        }
    }]

def get_next_chunk(transcript, start_position, next_tokens):
    """
    Get the next chunk of transcript to process, based on the algorithm specification.
    
    :param transcript: Complete transcript text.
    :param start_position: Starting character position in the transcript.
    :param next_tokens: Number of tokens to look ahead.
    :return: Tuple of (chunk_text, end_position).
    """
    chars_per_token = 4
    look_ahead_chars = next_tokens * chars_per_token
    
    end_position = min(start_position + look_ahead_chars, len(transcript))
    
    # Go to the end of the line
    while end_position < len(transcript) and transcript[end_position] != '\n':
        end_position += 1
    
    chunk_text = transcript[start_position:end_position]
    return chunk_text, end_position

def get_last_qa_block_start_position(qa_file_path):
    """
    Read the last processed start position from the existing QA file.
    
    :param qa_file_path: String of the path to the QA file.
    :return: Integer of the transcript start position, or 0 if not found.
    """
    try:
        with open(qa_file_path, 'r') as f:
            content = f.read()
            field_identifier = "TRANSCRIPT START POSITION: "
            last_transcript_start_position = content.rfind(field_identifier)
            if last_transcript_start_position != -1:
                end_of_line = content.find("\n", last_transcript_start_position)
                position_str = content[last_transcript_start_position + len(field_identifier):end_of_line].strip()
                return int(position_str.replace(',', ''))
    except FileNotFoundError:
        pass
    return 0

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
    current_position = start_position
    previous_block = None
    total_chars_transcript = len(transcript)

    while current_position < len(transcript):
        chunk, next_position = get_next_chunk(transcript, current_position, next_tokens)
        print(f"chunk transcript positions:        {current_position:,} to {next_position:,} of total: {total_chars_transcript:,} | Percent done: {round(current_position / total_chars_transcript * 100)}%")
        
        prev_block_prompt = "Please identify the first question-answer pair in the following transcript chunk:" if not previous_block else f"""
        Previous Question-Answer Block:
        {previous_block}
        Please identify the next question-answer pair after this one in the following transcript chunk:
        """

        full_prompt = fcall_prompt + "\n" + prev_block_prompt + "\n\n" + chunk
        
        try:
            qa_response = openai_function_call(full_prompt, chunk, tools_qa_incremental())
            arguments = json.loads(qa_response['tool_calls'][0]['function']['arguments'])
            
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
            
            print(f"qa response transcript position: {abs_transcript_start_pos:,} to {abs_transcript_end_pos:,}")
            # Update previous_block for the next iteration
            previous_block = qa_block
            
            yield qa_block, abs_transcript_start_pos
        except Exception as e:
            print(f"Error in qa extraction: {str(e)}")
            yield None, current_position
        
        current_position = abs_transcript_start_pos

def create_qa_file_from_transcript_incremental(file_path, fcall_prompt):
    """
    Manages the incremental extraction of question-answer pairs from a transcript file.
    This function handles the overall process, including reading the transcript, determining the next chunk to process, and appending the extracted QA blocks to a new file.

    :param file_path: String of the path to the transcript file to be processed.
    :param fcall_prompt: String of the prompt to be used for function calling.
    :return: String of the path to the newly created QA file.
    """
    from primary.structured import count_blocks

    metadata, content = read_metadata_and_content(file_path)
    metadata = set_last_updated(metadata, 'Created QA Incremental')
    metadata = set_metadata_field(metadata, "source file", file_path)
    
    print("OPENAI_MODEL = " + OPENAI_MODEL)
    segment_tokens = count_segment_tokens(file_path)
    max_segment_tokens = max(segment_tokens)
    transcript = get_heading(file_path, "### transcript")
    transcript = transcript.lstrip('### transcript').rstrip('\n').lstrip('\n*')
    print(f"Number of characters in transcript: {len(transcript):,}\n")

    initial_content = "## content\n\n### qa\n"
    qa_file_path = write_metadata_and_content(file_path, metadata, initial_content, overwrite='no-sub', suffix_new='_qa-incremental')
    
    current_position = 0
    max_retries = 5

    while current_position < len(transcript):
        existing_blocks = count_blocks(qa_file_path)
        block_number = existing_blocks + 1
        
        for qa_block, abs_transcript_start_pos in fcall_qa_incremental(transcript, max_segment_tokens, fcall_prompt, start_position=current_position):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    if qa_block is None:
                        raise Exception(f"Error occurred on block {block_number}.")
                    
                    print(f"writing block number {block_number}\n")
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


### QA EVAL (1,626 tokens)
def validate_qa_transcript_positions(transcript, qa_dict):
    """
    Validate the extracted QA block against the original transcript based on reported positions.
    
    :param transcript: String of the full transcript text.
    :param qa_dict: Dictionary containing the extracted QA information.
    :return: Tuple of (bool, str) indicating pass/fail and a mismatch description if applicable.
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

def evaluate_qa_extraction(transcript, qa_file_path):
    """
    Evaluate the QA extraction process using LLM-based checks and position validation.
    
    :param transcript: String of the full transcript text.
    :param qa_file_path: String path to the file containing extracted QA blocks.
    :return: List of dictionaries containing evaluation results for each QA block.
    """
    from primary.structured import get_all_fields_dict
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

def generate_evaluation_report(evaluation_results, output_file):
    """
    Generate a readable report from the evaluation results.
    
    :param evaluation_results: List of dictionaries containing evaluation results.
    :param output_file: String path to write the report.
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

def run_automated_evaluation(transcript_file, qa_file):
    """
    Run the automated evaluation process.
    
    :param transcript_file: String path to the original transcript file.
    :param qa_file: String path to the file containing extracted QA blocks.
    """
    transcript = get_heading(transcript_file, "### transcript")
    transcript = transcript.lstrip('### transcript').rstrip('\n').lstrip('\n*')
    
    evaluation_results = evaluate_qa_extraction(transcript, qa_file)
    
    output_file = manage_file_overwrite(qa_file, "_autoeval", overwrite="no")
    generate_evaluation_report(evaluation_results, output_file)
    
    print(f"Evaluation completed. Report written to {output_file}")






## primary/vectordb.py (5,314 tokens)
import os
import json
import zipfile
import shutil
import datetime

from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import Pinecone as LangchainPinecone
from langchain_community.document_loaders import ObsidianLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import PINECONE_API_KEY, OPENAI_API_KEY_CONFIG_LLM

client = OpenAI(api_key=OPENAI_API_KEY_CONFIG_LLM)

VZIP_LOG_FOLDER = 'logs/vectordb_pinecone_log_zips/'
EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI 1536 dimensions and $0.02/1M tokens - batch is 1/2 that, large is $.13)

#These vector db wrapper functions are used manually and are not called by the rag_bots functions. (RT 6-10-2024)
#Pinecone indexes can be seen in the pinecone.io portal > go to Serverless in UL - login sends email to fofgeneral20


### VECTOR DB SUPPORT (3,515 tokens)
def generate_embedding(text, model=EMBEDDING_MODEL):
    """ 
    Generates an embedding vector for the provided text using the specified OpenAI embeddings model.

    :param text: string of text to generate an embedding for.
    :param model: string of the OpenAI embeddings model to use.
    :return: list of floats representing the embedding vector.
    """

    response = client.embeddings.create(input=text,
    model=model)
    embedding = response.data[0].embedding
    return embedding

#TODO review the timestamp lines
def generate_vectors_qa(folder_paths, suffixpat_include, include_subfolders=True):
    """ 
    Generates vectors from markdown files in the specified folder paths.

    :param folder_paths: list of strings of the paths to the folders containing markdown files.
    :param include_subfolders: boolean indicating whether to search for markdown files in subfolders. Default is True.
    :return: vectors as a list of dictionaries, each containing an id, values, and metadata for a block of text.
    """
    from primary.fileops import get_files_in_folder, get_timestamp
    from primary.structured import get_blocks_from_file, get_all_fields_dict

    vectors = []  # Consider renaming this. it's the list of all the dicts with the fields from the blocks
    total_files = 0
    num_vectors = 0
    for folder_path in folder_paths:
        file_paths = get_files_in_folder(folder_path, suffixpat_include=suffixpat_include, include_subfolders=include_subfolders)
        total_files += len(file_paths)
        for path in file_paths:
            blocks = get_blocks_from_file(path)
            block_num = 0
            for block in blocks:
                fields = get_all_fields_dict(block)
                file_name_with_extension = os.path.basename(path)  # Get file name with extension
                fields['SOURCE'] = file_name_with_extension  # Use file name with extension as the SOURCE
                vector_id = (os.path.splitext(file_name_with_extension)[0] + "_" + str(block_num)).replace(" ", "_")
                
                # Main call to generate embeddings
                embedding = generate_embedding(fields['QUESTION'])  
                timestamp, _ = get_timestamp(fields['QUESTION'])  # Extract timestamp from the question
                if timestamp:
                    fields['TIMESTAMP'] = timestamp  # Add timestamp to the metadata fields
                vector = {'id': vector_id, 'values': embedding, 'metadata': fields}  # Create the vector schema
                vectors.append(vector)
                num_vectors += 1
                block_num += 1
            #print('Vectorized file:' + file_name_with_extension)
    print(f"Vectors generated for {total_files} files - number of vectors: {num_vectors}")
    return vectors

def vectors_to_json(vectors, file_path):
    """
    Converts a list of dictionaries into a JSON file.

    :param vectors: list of dictionaries to be converted.
    :param file_path: name of the JSON file to be created.
    :return: None.
    """

    try:
        # Write the JSON data to a file
        with open(file_path, 'w') as json_file:
            json.dump(vectors, json_file, indent=4)
        print(f"Successfully created {file_path}.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def json_to_vectors(file_path):
    """
    Loads vectors from a JSON file.

    :param file_path: Path to the JSON file containing the vectors.
    :return: List of vectors loaded from the JSON file. Returns an empty list if an error occurs.
    """
    try:
        with open(file_path, 'r') as json_file:
            vectors = json.load(json_file)
        print(f"Successfully loaded {file_path}.")
        return vectors
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def validate_vectors(vectors, required_fields=None, verbose=False):
    """ 
    Validates that each vector in the list has the required fields and correct data types.

    :param vectors: list of dictionaries, each representing a vector with an id, values, and metadata.
    :param required_fields: list of required field names (in uppercase). If None, uses a default set.
    :param verbose: boolean, if True, prints additional information during validation.
    :return: None. Raises ValueError if validation fails.
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

def upsert_vectors_pinecone(vectors, vector_index_name, new_index=True):
    """ 
    Upserts vectors into a Pinecone index in batches of 100, creating the index if it does not exist and if new_index is True.

    :param vectors: list of dictionaries, each representing a vector to be upserted.
    :param vector_index_name: string of the name of the Pinecone index.
    :param new_index: boolean indicating whether to create a new index if it does not exist. Default is True.
    :return: None.
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
def delete_pinecone_index(vector_index_name, user_prompt=True):
    """
    Deletes a Pinecone index if it exists, optionally prompting the user for confirmation.

    :param vector_index_name: string of the name of the Pinecone index to be deleted.
    :param user_prompt: boolean indicating whether to prompt the user for confirmation before deletion. Default is True.
    :return: Boolean indicating whether the index was actually deleted.
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

def update_pinecone_index_list_md(file_name='pinecone_index_list.md', log_folder_path=VZIP_LOG_FOLDER):
    """
    Updates a markdown file with a list of Pinecone indices.

    :param file_name: Name of the markdown file to update. Default is 'pinecone_index_list.md'.
    :param log_folder_path: Path to the folder where the file will be saved. Default is VZIP_LOG_FOLDER.
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

def save_splits_to_json(all_chunks, output_base_filename, metadata, log_folder_path=VZIP_LOG_FOLDER):
    """
    Saves the text splits and metadata to a JSON file, organized by source.

    :param all_chunks: List of Document objects containing the text splits.
    :param output_base_filename: Base filename for the output JSON file.
    :param metadata: Dictionary containing metadata to be included in the JSON.
    :return: Path to the saved JSON file.
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

def setup_create_vectordb(folder_paths, vector_index_base, suffixpat_include=None):
    """
    Sets up the initial parameters for creating a vector database.
    
    :param folder_paths: List of folder paths to process
    :param vector_index_base: Base name for the vector index
    :param suffixpat_include: Pattern to filter files (optional)
    :return: Tuple of (vector_index_name, vector_index_name_with_timestamp, datetime, all_file_paths)
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

def check_and_create_pinecone_index(vector_index_name, dimension=1536, metric='cosine'):
    """
    Initializes Pinecone, checks if the specified index exists, creates it if it doesn't,
    and prompts the user for action if the index already exists.
    
    :param vector_index_name: Name of the Pinecone index to check/create
    :param dimension: Dimension of the vectors (default is 1536 for OpenAI embeddings)
    :param metric: Distance metric to use (default is 'cosine')
    :return: Boolean indicating whether to continue with the vector database creation
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


### VECTOR DB CREATION (1,549 tokens)
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
    from primary.fileops import apply_to_folder, create_new_file_from_heading, sub_suffix_in_file, move_files_with_suffix, remove_timestamp_links, find_and_replace_pairs
    
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY_CONFIG_LLM

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

def create_qrag_vectordb(folder_paths, vector_index_base, suffixpat_include=None):
    # Set OpenAI and Pinecone API keys
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY_CONFIG_LLM
    
    # Setup vector database creation
    vector_index_name, vector_index_name_with_timestamp, datetime, all_file_paths = setup_create_vectordb(folder_paths, vector_index_base, suffixpat_include)

    # Generate vectors
    vectors = generate_vectors_qa(folder_paths, suffixpat_include)

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






## primary/rag.py (3,758 tokens)
import os
from datetime import datetime
from pinecone import Pinecone

from primary.vectordb import generate_embedding
from primary.llm import simple_openai_chat_completion_request
from primary.rag_prompts_routes import *
from config import PINECONE_API_KEY, OPENAI_API_KEY_CONFIG_LLM, ANTHROPIC_API_KEY_CONFIG_LLM

#TODO consider where and how we are getting the openai api keys
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY_CONFIG_LLM
os.environ['ANTHROPIC_API_KEY'] = ANTHROPIC_API_KEY_CONFIG_LLM

DEFAULT_LLM_MODEL = 'gpt-4o'
pc = Pinecone(api_key=PINECONE_API_KEY)  # 'pc' is the standard convention so we'll keep it despite it being unclear


### RETRIEVAL (283 tokens)
def pinecone_retriever(query, vector_index_name, num_chunks=5):
    """ 
    Retrieves relevant question chunks from a Pinecone index based on the input question.

    :param question: string of the input question to search for.
    :param vector_index_name: string of the name of the Pinecone index to query.
    :return: tuple containing fetched question chunks and a dictionary of retrieved IDs with their scores.
    """
    vectorized_query = generate_embedding(query)
    index = pc.Index(vector_index_name)
    retrieved_qchunks = index.query(
        namespace="",
        vector=vectorized_query,
        top_k=num_chunks,  # determines number of vectors retuned by pinecone
        include_values=False)
    
    # Extract the IDs from the retrieved question chunks
    retrieved_ids_scores = {vector['id']: vector['score'] for vector in retrieved_qchunks['matches']}
    # print(f"DEBUG retrieved_ids: {retrieved_ids})
    # Fetch the question chunks using the IDs
    ids = list(retrieved_ids_scores.keys())
    fetched_chunks = index.fetch(ids=ids, namespace="")

    # DEBUG save to file
    # with open('fetched_chunks.txt', 'w') as f:
    #     f.write(str(fetched_qchunks))

    return fetched_chunks, retrieved_ids_scores


### VRAG (694 tokens)
def print_vrag_display_text(json_object, show_prompt=False):
    """
    Prints a formatted display text for VRAG (Vector Retrieval Augmented Generation) results.

    :param json_object: dictionary containing VRAG results with 'content' key.
    :param show_prompt: boolean to determine whether to show the full LLM prompt.
    :return: None.
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
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(user_question, vector_index_name)
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
 
### QRAG (2,604 tokens)
def select_chunks_qrag_1or2(fetched_qa_chunks, retrieved_ids_scores):
    """ 
    Sorts and returns the most relevant chunks based on similarity score and 'STARS' rating.
    Filters down to 1 or 2 chunks from the 5 fetched.

    :param fetched_qchunks: dictionary of fetched question chunks from Pinecone.
    :param retrieved_ids_scores: dictionary of retrieved IDs with their similarity scores.
    :return: tuple containing the highest similarity chunk and the highest 'STARS' rated chunk (if different).
    """
    # Find the id of the chunk with the highest similarity score
    highest_sim_id = max(retrieved_ids_scores, key=retrieved_ids_scores.get)
    
    # Find the id of the chunk with the highest 'STARS' rating
    highest_stars_id = max(fetched_qa_chunks['vectors'], key=lambda x: fetched_qa_chunks['vectors'][x]['metadata'].get('STARS', 0))
    
    # Extract chunks
    highest_sim_chunk = fetched_qa_chunks['vectors'][highest_sim_id]
    highest_stars_chunk = fetched_qa_chunks['vectors'][highest_stars_id] if highest_sim_id != highest_stars_id else None

    # Return the chunks directly
    return (highest_sim_chunk, highest_stars_chunk)

def parse_chunk_all(chunk, simscores=None):
    """ 
    Formats information from a chunk and its optional similarity scores into a structured dictionary,
    including all fields present in the chunk's metadata. Handles various data types including lists.

    :param chunk: dictionary containing metadata and content of a document chunk.
    :param simscores: optional dictionary of similarity scores keyed by chunk id.
    :return: dictionary containing formatted chunk information.
    """
    def safe_convert(value):
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

def parse_chunk_qa_dd(chunk, simscores, prefix=''):
    """ 
    Wrapper function that formats information from a chunk and its similarity scores into a structured dictionary,
    maintaining the same functionality as the original parse_chunk_qa_dd function while using parse_chunk_all internally.
    Handles complex data types like lists and empty strings.

    :param chunk: dictionary containing metadata and content of a document chunk.
    :param simscores: dictionary of similarity scores keyed by chunk id.
    :param prefix: string of prefix to add to dictionary keys. default is empty string.
    :return: dictionary containing formatted chunk information with prefixed keys.
    """
    # Call the general parsing function
    general_result = parse_chunk_all(chunk, simscores)

    def safe_int(value, default=0):
        try:
            return int(value) if value != '' else default
        except (ValueError, TypeError):
            return default

    def safe_float(value, default=0.0):
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

def qrag_routing_call(user_question, vector_index_name, routes_dict, routes_bounds=[0.3, 0.9], 
llm_model=DEFAULT_LLM_MODEL, user_id='default', qrag_version="1.0"):
    """ 
    Routes a user question through a question retrieval augmented generation (QRAG) process.

    :param user_question: string of the user's input question.
    :param routes_dict: dictionary containing routing prompts and templates.
    :param vector_index_name: string of the name of the pinecone index to use for retrieval.
    :param routes_bounds: list of two floats representing the lower and upper similarity bounds for routing.
    :param user_id: string of the user identifier. defaults to 'default'.
    :param llm_model: string of the language model to use. defaults to DEFAULT_LLM_MODEL.
    :param bot_version: string of the bot version. defaults to "1.0".
    :return: dictionary containing metadata and content of the QRAG process and response.

    Usage:
    response = qrag_routing_call("What is the capital of France?", routes_dict, "my_index")
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

def qrag_llm_call(json_object):
    """ 
    Generates an AI answer for a given JSON object containing question and context information.

    :param json_object: dictionary containing the question, context, and metadata for generating an AI answer.
    :return: dictionary with the updated JSON object including the AI-generated answer.
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

def print_qrag_display_text(json_object):
    """ 
    Prints a formatted display text for QRAG (Question Retrieval Augmented Generation) results.

    :param json_object: dictionary containing QRAG results with 'content' key.
    :return: None.
    """
    user_question = json_object['content']['user_question']
    route_preamble = json_object['content']['route_preamble']
    quoted_qa = json_object['content']['quoted_qa']
    ai_answer = json_object['content']['ai_answer']
    display_text = 'USER QUESTION: ' + user_question + '\n\n' + 'ROUTE PREAMBLE: ' + route_preamble + '\n\n' + quoted_qa + 'AI ANSWER: ' + ai_answer
    print(display_text)

def qrag_2step(user_question, routes_dict, vector_index_name):
    """ 
    Performs a two-step question-answering process using QRAG (Question Retrieval Augmented Generation).

    :param user_question: string of the user's input question.
    :return: None
    """
    # Create JSON object with routing information
    routing_json_obj = qrag_routing_call(user_question, routes_dict, vector_index_name)

    # Print the display text for the QRAG process
    print_qrag_display_text(routing_json_obj)

    # Generate and print the AI answer
    ai_answer = qrag_llm_call(routing_json_obj)['content']['ai_answer']
    print(ai_answer)





## primary/conversion.py (871 tokens)

import os
import re
import logging
import pypandoc

from llama_parse import LlamaParse  # pip install llama-index llama-parse
from llama_index.core import SummaryIndex
from llama_index.readers.google import GoogleDocsReader  # pip install llama-index llama-index-readers-google
#from IPython.display import Markdown, display

from config import LLAMA_CLOUD_API_KEY


### LLAMAINDEX (491 tokens)
def convert_llamaparse_pdf_to_md(file_path):
    suffix_append = "_llamaparse"
    documents = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown",verbose=True).load_data(file_path)
    print(documents[0].text[0:1000])
    md_file_path = file_path.rsplit('.', 1)[0] + suffix_append + '.md'  # Replace the file extension with .md
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(documents[0].text)
    print("Completed LlamaParse pdf to md conversion and appended suffix: " + suffix_append + " on input file_path: " + file_path)
    return md_file_path

#TODO WIP - not working because needs different gcloud auth than service account
def convert_llamaindex_gdocs_to_md(gdoc_id_list):
    """
    Converts Google Docs to Markdown using Llama Index.

    :param gdoc_id_list: list of Google Docs document IDs.
    :return: Markdown representation of the Google Docs.
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


### PANDOC (294 tokens)
''' To confirm installation, run: pandoc --version
Should see:
pandoc 3.2
Features: +server +lua
Scripting engine: Lua 5.4
'''

def convert_file_to_md_pandoc(file_path, suffix_new="_pandoc"):
    """
    Converts any pandoc supported file format to a markdown file using pypandoc.
    Including but not limited to: doc, docx, html, latex, epub, odt, rtf, ascii doc.
    pdf has limitations.

    :param file_path: string of the path to the file to be converted.
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





## primary/docwork.py (4,302 tokens)
import os
import re


### COMMON TEXT (152 tokens)
#TODO 7-18 RT - consider whether this is OK to be in function, think it was not previously and getting Problems
def load_custom_dictionary(file_path):
    '''
    # import nltk
    # nltk.download('words')
    # nltk.download('punkt')  # Added to download the 'punkt' tokenizer models
    # from nltk.corpus import words
#TODO rename and comment this function so it's more clear what it does
    '''
    """ Load a custom dictionary from a file. """
    try:
        with open(file_path, 'r') as file:
            return set(word.strip() for word in file)
    except FileNotFoundError:
        print("Custom dictionary file not found.")
        return set()


### TRANSCRIPTS (2,954 tokens)
def replace_colon_for_non_speaker(text):
    """
    Replaces colons that do not form part of speaker names with a space and a dash.

    :param text: string of the transcript text that needs cleaning.
    :return: string of the cleaned transcript text.
    """
    # List of words that precede a colon but are not speaker names
    non_speaker_words = ['question', 'up', 'this']
    
    # Iterate over the non_speaker_words and replace each occurrence of "word:" with "word -"
    for word in non_speaker_words:
        text = text.replace(f"{word}:", f"{word} -")
    
    return text

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
    # Pattern that matches speaker names followed by a colon, possibly with spaces after,
    # and captures the speaker name and the dialogue in separate groups
    speaker_dialogue_pattern = re.compile(r"^([^\d]*[a-zA-Z\d]+[^\d]*):\s*(.*)$", re.MULTILINE)
    
    # Pattern that matches time formats, e.g., "12:15", "3:00".
    time_reject_pattern = re.compile(r".*\d:\d.*", re.MULTILINE)
    
    # Remove '(' and ')' characters
    processed_text = original_text.replace('(', '').replace(')', '')
    
    # Replace colons that are not part of speaker names
    processed_text = replace_colon_for_non_speaker(processed_text)
    
    # Split the text into lines for processing
    lines = processed_text.splitlines()
    
    # Initialize variables for the cleaned text and a flag to mark when we're accumulating dialogue lines
    fixed_lines = []
    current_speaker = None
    current_dialogue = []
    
    def flush_current_dialogue():
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
def validate_transcript(file_path, verbose=False):
    """
    Validates the speaker segments in a single transcript file by checking the format of speaker segments.

    :param file_path: string of path to the transcript file.
    :param verbose: boolean indicating whether to print detailed response text
    :return: boolean indicating whether the file passed the validation.
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

def extract_transcript_data(file_path):
    """
    Extracts detailed transcript information into a list of dictionaries.
    Each dictionary contains speaker_name, speaker_role, timestamp, timestamp_link, and dialogue.
    Speaker lines can end in a colon (FDA Townhalls) or include a timestamp (Deutsch, PV).
    Speaker role is extracted from text within parentheses preceding the colon or timestamp.

    :param file_path: string of the path to the file to be processed.
    :return: list of dictionaries with keys ['speaker_name', 'speaker_role', 'timestamp', 'timestamp_link', 'dialogue'].
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

def create_speaker_triples(file_path):
    """
    Creates a list of speaker triples from a given file using extracted transcript data.
    Works with speaker lines that end in a colon (FDA Townhalls) or have timestamp (Deutsch, PV).
    Utilizes the extract_transcript_data function to parse the file and count occurrences of each speaker.
    Then creates a list of triples in the format "speaker name, file_stem, count"
    file_stem is the filename without extension, and count is the number of times the speaker appears in the file.

    :param file_path: string of the path to the file to be processed.
    :return: string of speaker triples separated by newlines.
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

def create_speaker_matrix(folder_path, suffix_include=None, target_file_path="speaker_matrix.csv"):
    """
    Creates a matrix of speaker names from files in a given folder and writes it to a CSV file.

    This function processes all files in the specified folder that have the specified suffix, identifies the speakers 
    and counts their occurrences. It then creates a matrix of speaker triples in the format "speaker, file_stem, count" 
    where speaker is the speaker's name, file_stem is the filename without extension, and count is the number of times 
    the speaker appears in the file. The matrix is written to a CSV file at the specified target file path.

    :param folder_path: string of the path to the folder containing the files to be processed.
    :param target_file_path: string of the path to the target CSV file. If no folder component is specified, the folder_path is used.
    :param suffix_include: string of the suffix to include in the file processing.
    :return: string of the path to the created csv file.
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


### PROPER NAMES (1,184 tokens)
def extract_proper_names(text, custom_proper_names_files=None, bool_include_custom=False, verbose=False):
    """
    Extract proper names from the input text based on capitalization and dictionaries.
    
    :param text: string containing the input text.
    :return: list of proper names identified.
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

def create_proper_names_triples(file_path, custom_proper_names_files=None, bool_include_custom=False, verbose=False):
    """
    Creates a list of proper name triples from a given file using extracted text data.
    Utilizes the extract_proper_names function to parse the file and count occurrences of each proper name.
    Then creates a list of triples in the format "proper name, file_stem, count"
    file_stem is the filename without extension, and count is the number of times the proper name appears in the file.

    :param file_path: string of the path to the file to be processed.
    :return: string of proper name triples separated by newlines.
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

def print_proper_names(file_path, custom_proper_names_files=None, bool_include_custom=False, verbose=False):
    proper_names_output = create_proper_names_triples(file_path, custom_proper_names_files, bool_include_custom, verbose)
    proper_names_list = [line.split(',')[0] for line in proper_names_output.split('\n')]
    proper_names_list_sorted = sorted(proper_names_list)
    print("\n\nFiltered Proper Names")
    for name in proper_names_list_sorted:
        print(name)
    print(f"Total proper names: {len(proper_names_list_sorted)}")




## primary/structured.py (4,118 tokens)
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


### BLOCK PROCESSING (1,060 tokens)
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


### TOPICS (2,988 tokens)
#TODO try on townhall qa files - may need to update for alternate METADATA and CONTENT format
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







## primary/corpuses.py (4,519 tokens)
import os
import re
from collections import defaultdict

from primary.fileops import *

import warnings  # Set the warnings to use a custom format
warnings.formatwarning = custom_formatwarning
#USAGE: warnings.warn(f"Insert warning message here")


### QA VALIDATION (1,281 tokens)
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

### DEUTSCH (1,001 tokens)
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

### FDA TOWNHALLS (2,180 tokens)
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

#TODO test after July refactor
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

#TODO test after July refactor
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

#TODO WIP - add path to find_replace_csv after testing fileops func
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



## primary/aws.py (1,120 tokens)
import boto3
import os
import json
from botocore.exceptions import ClientError, NoCredentialsError

### AWS S3 (1,092 tokens)
def upload_file_to_s3(file_path, bucket='fofpublic', object_name=None, s3_path=None):
    """
    Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket: Name of the S3 bucket, default is 'fofpublic', others: 'fofsecure', 'deutsch-audio'
    :param object_name: S3 object name. If not specified, the file name is used
    :param s3_path: S3 folder path where the file will be stored, e.g. 'podcasts/'
    :return: The object name of the file in S3
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

def rename_s3_object(bucket, old_key, new_key, s3_path=None):
    """
    Rename an object in an S3 bucket by copying it to a new key and deleting the old key.

    :param bucket: Name of the S3 bucket
    :param old_key: The current key (path) of the object in the S3 bucket
    :param new_key: The new key (path) for the object in the S3 bucket
    :param s3_path: Optional S3 folder path to prepend to the keys
    :return: None
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

def get_s3_json(bucket, key, s3_path=None):
    """
    Retrieve a JSON object from an S3 bucket.

    :param bucket: Name of the S3 bucket
    :param key: The key (path) of the JSON object in the S3 bucket
    :param s3_path: Optional S3 folder path to prepend to the key
    :return: The JSON object if found, otherwise None
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




## primary/rag_prompts_routes.py (5,098 tokens)
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
If the question posed by the user is relevant and the retrieved content from David Deutsch's work provide context or depth, incorporate that information into your response.
If you find that the content from the retrieved content contradicts the worldview as described in the summary, prioritize the ideas in the summary for your response.
Should the user's question be irrelevant to both the worldview and the sources, issue a disclaimer acknowledging this. Nevertheless, aim to answer in a manner that is ideologically consistent with the worldview.

Avoid using qualifiers like "according to David Deutsch" and refrain from using the first person in your responses. Your answers should appear as if they emanate directly from an entity entirely in sync with the worldview in question.
SUMMARY
Knowledge:		
	is information that: has causal power, can do things, tends to stick around, is substrate independent	
	arises from conjecture and criticism, not just sensory experience	
	about reality comes from explanations about what exists beyond mere appearances	
	grows by correcting errors and misconceptions	
	is not justified true belief - this is an epistemological misconception	
	creation is due only to 2 known sources: Biological Evolution and the thoughts of People. They have some key differences. In the case of human knowledge, the variation is by Conjecture, and the selection is by Criticism and experiment. In the biosphere, the variation consists of mutations (random changes) in genes, and natural selection favors the variants that most improve the ability of their organisms to reproduce, thus causing those variant genes to spread through the population. Both sources are abstract replicators which means they're forms of information that are embodied in a physical system and tend to remain so (in DNA strands, books, hard-disks etc). But the two sources have some key differences. Evolution is bounded and parochial. It tends to make slow iterative changes. People's creativity is unbounded and has Reach.	
	streams provide evidence about the universe and are present in almost all environments	
	growth consists of correcting misconceptions in our theories	
	is always fallible, meaning all knowledge inherent contains errors	
	is a broad	
Principle of Optimism:		
	is that all evils are caused by insufficient knowledge	
Problems:	are inevitable because our knowledge is always incomplete	
	are solvable, given the right knowledge and provided the solutions don't violate the laws of physics	
	solving problems creates new problems in turn	
	exist when conflicts between ideas are experienced	
	exist when it seems that some of our theories, especially the explanations they contain, seem inadequate and worth trying to improve.	
Explanations:		
	are statements about what is there, what it does, and how and why	
	are good explanations if they are hard to vary:	
		while still accounting for what they purport to account for
		with all parts of the explanation having a functional role
		in the sense that changing the details would ruin them
	are distinguished from predictions which are merely about what is going to happen next	
	exist for emergent phenomena (such as life, thought or computation) about which there are comprehensible facts or explanations that are not simply deducible from lower-level theories, but which may be explicable or predictable by higher-level theories referring directly to the phenomena.	
	are bad explanations if they are unspecific and easy to vary, meaning you can change any of all of the details without destroying the explanation	
	that refer to the supernatural are bad explanations	
Explanatory Knowledge:		
	is human type knowledge, understanding	
	has reach, meaning the explanations solve problems beyond those that they were created to solve	
	has universal power	
	is of central importance in the universe	
	growth is inherently unpredictable	
	contrasts with non-explanatory knowledge such as that in genes	
	is only created by one type of entity, referred to as "people"	
	that we currently know about is only created in human brains, but we also know it can be created by other entities such as a computer program, alien, now extinct human sister species (Neanderthals)	
	provides wealth and progress	
	creation is the best preparation for unknown dangers and unknown opportunities	
	has a special relationship with both human minds and the laws of nature	
	gives human minds the capability to see beyond the visible, to what is really there even though we cannot directly experience it	
	enables us to control nature and make technical progress	
Science:		
	is the domain of knowledge of our best explanations of physical reality	
	is primarily about the quest for good explanations	
	purpose is to understand reality through good explanations	
	uses the characteristic (though not the only) method of criticism of experimental testing	
	is not simply about what is testable or making predictions, it is about understanding reality	
	is among one of many domains, for which there are not dividing bright lines, that all seek good explanations	
	is about finding laws of nature which are testable regularities	
	is the kind of knowledge that can be tested by experiment or observation	
Mathematics:		
	is the domain of knowledge of our best explanations of abstract reality	
	is the study of absolutely necessary truths	
	despite the misconception that it has privileged status set apart from other knowledge and uniquely consists of a bedrock of truth, is fallible and contains errors like all knowledge	
	provides no barrier to progress, even though as a matter of logic, there are things that we can't know (due to incompleteness theorems), but they're not things that matter ultimately to humans	
Computers:		
	are physical systems that instantiates abstract entities and their relationships as physical objects and their motions	
	are of fundamental significance because of the fact that physical reality only instantiates computable functions	
Computation:		
	a physical process that instantiates the properties of some abstract entity	
	is substrate independent	
	is basically the only way to process information	
Universality:		
	is achieved when incremental improvements in a system of knowledge or technology causes a sudden increase in reach, making it a universal system in the relevant domain	
	is only possible in digital systems because error correction is essential	
	of the Turing Principle (in its strongest form) states that it is physically possible to build a universal virtual-reality generator	
	in a system means that is capable of representing all states 	
	of the laws of physics means they apply everywhere and at all times	
	has many kinds and is very important	
	reveals that a computer program can simulate a brain and therefore be creative and create new explanatory knowledge	
	of human minds means that we can understand (explain) anything that can be in principle understood	
Universal Computers:		
	are also known as Turing Machines	
	only differ in speed and memory capacity, and do not differ in the repertoire of operations they can perform 	
	can simulate physical reality to arbitrary precision	
	are such that the set of all possible programs that could be programmed into a universal computer is in one-one correspondence with the set of all possible motions of anything	
People:		
	is redefined as entities that can create explanatory knowledge, i.e. are Universal Explainers	
	don't necessary need to be human, and could be creative aliens and in the future, artificial general intelligence	
	have free will which is redefined as the capacity to affect future events in any one of several possible ways, and to choose which shall occur.	
	are typically thought to be only humans, and the 'Principle of Mediocrity' is the prevailing view - which is the misconception that there is nothing significant about humans (cosmically speaking) 	
	are of cosmic significance because understanding the universe necessarily involves understanding the universality and power of explanatory knowledge	
	uniquely are capable of creativity	
Creativity:		
	is the capacity to create new explanations	
	is not yet well understood and will not be understood (have a good explanation for) until we can "program" it	
Human Brain:		
	Functions as a biological computer, processing and storing information.	
	Is a physical substrate where knowledge, thoughts, and creativity originate.	
	Evolutionary design enables it to conjecture, criticize, and adapt, laying the foundation for the creation of explanatory knowledge.	
	While traditionally seen as the sole creator of human-type knowledge, it's now understood that similar functionality could, in principle, exist in other substrates.	
Human Mind:		
	Represents the abstract, non-physical aspect of thought, consciousness, and self-awareness.	
	Operates within the brain, but its processes are substrate-independent.	
	Is a realm of creativity, where explanatory knowledge is both generated and understood.	
	While intimately linked with the human brain, its core functions of conjecture and criticism can be conceptually decoupled from it, suggesting the potential for artificial systems to exhibit "mind-like" qualities.	
Artificial General Intelligence (AGI):		
	is a computer program with creativity, implemented on an "artificial" system which is typically thought to be a digital silicon-based computer rather than a human brain (which is properly understood to also be a type of computer)	
Experience:		
	is often misunderstood, because there is no such thing as ‘raw’ experience - all our experience of the world comes through layers of conscious and unconscious interpretation	
	can be external, outside of one's own mind, or internal, within one's own mind	
	is connected to qualia which is the subjective aspect of a sensation (e.g. Consciousness)	
Memes:		
	are ideas that are replicators	
	comprise culture	
	evolve, meaning change, sometimes creating knowledge, through alternating variation and selection	
	include both jokes and scientific theories	
	are analogous to genes, but there are also profound differences in the way they evolve. The most important differences are that each meme has to include its own replication mechanism, and that a meme exists alternately in two different physical forms: a mental representation and a behaviour. Hence also a meme, unlike a gene, is separately selected, at each replication, for its ability to cause behaviour and for the ability of that behaviour to cause new recipients to adopt the meme.	
	employ only two basic strategies of meme replication, anti-rational and 	
	that are anti-rational rely on disabling the recipients' critical faculties to cause themselves to be replicated	
	that are rational rely on the recipients' critical faculties to cause themselves to be replicated	
Memeplex:		
	is a group of memes that help to cause each other’s replication	
Replicator:		
	is an entity that contributes causally to its own copying, for example genes and ideas are types of replicators 	
Society:		
	is dynamic if it is dominated by rational memes	
	is static if it is dominated by anti-rational memes, and changes happen on a timescale longer than its members can notice	
	that are static fail due to lack of knowledge to address their problems	
Culture:	is redefined as a set of shared ideas that cause their holders to behave alike in some ways	
Enlightenment:		
	is (The beginning of) a way of pursuing knowledge with a tradition of criticism and seeking good explanations instead of reliance on authority	
	values of science, reason and freedom have grown to create "The West", defined as the political, moral, economic and intellectual culture of the Enlightenment	
Governing:		
	Determining "Who should rule?" based on fixed criteria is flawed.	
	Governments should be judged by how easily bad leaders/policies can be removed without violence, not by the quality of leaders	
	Institutions improve when then embody knowledge of how to detect and eliminate errors	
	Good political institutions are those that make it as easy as possible to detect whether a ruler or policy is a mistake, and to remove rulers or policies without violence when they are (known as "Popper's Criterion")	
Sustainability:		
	has two almost opposite, but often confused, meanings: to provide someone with what they need, and to prevent things from changing	
	Real sustainability lies in progress and knowledge	
Progress:		
	Human civilization made almost no progress recently, in two senses. One is that it was sporadic, and it was sort of two steps forward, two steps back, quite a lot of the time. And the other way is that it was extremely slow. The rate at which knowledge was being generated was very slow compared with a human lifetime, and therefore a typical human would never see any increase in knowledge in their lifetime, for most of human history. And that only stopped being true a few hundred years ago. It's somewhat arbitrary, you know, with the scientific revolution, but I think the real key change was a bigger thing, namely the Enlightenment.	
	Wealth is redefined as the repertoire of physical transformations that one is capable of causing	
	Humans are inherently reliant on technology for survival. Even in our evolutionary cradle, the great rift valley of Africa, we depended on tools like fire and clothing. Our survival isn't based solely on our physical attributes; we utilize knowledge to adapt and overcome environmental challenges.	
Philosophy:		
	Fallibilism is a foundational principle to always uphold: Knowledge has no absolute authoritative sources, and there are no definitive means to justify knowledge as wholly true or probable. All responses and interpretations must reflect and respect this core tenet.	
	Rational criticism compares rival theories with the aim of finding which of them offers the best explanations according to the criteria inherent in the problem.	
	Moral philosophy addresses the problem of what sort of life to want.	
	Rational is attempting to solve problems by seeking good explanations; actively pursuing error-correction by creating criticisms of both existing ideas and new proposals.	
	Realism is the good theory that an external physical universe exists objectively and affects us through our senses - the idea that the physical world exists in reality, and that knowledge of it can exist too.	
	Aesthetics is the philosophy of beauty.	
Bad Philosophy:		
	is not merely false, but actively prevents the growth of other knowledge, and includes religious fundamentalism and postmodernism	
	Blind optimism is recklessness, overconfidence - proceeding as if one knew that bad outcomes will not happen.	
	Blind pessimism is avoiding everything not known to be safe.	
	Empiricism is the misconception that we ‘derive’ all our knowledge from sensory experience.	
	Inductivism is the misconception that scientific theories are obtained by generalizing or extrapolating repeated experiences, and that the more often a theory is confirmed by observation the more likely it becomes.	
	Induction is the erroneous belief that general theories come from repeated experiences.	
	Holism is the misconception that all significant explanations are of components in terms of wholes rather than vice versa.	
	Instrumentalism is the misconception that science cannot describe reality, only predict outcomes of observations.	
	Justificationism is the misconception that knowledge can be genuine or reliable only if it is justified by some source or criterion.	
	Logical positivism is the bad philosophy that statements not verifiable by observation are meaningless.	
	Parochialism is mistaking appearance for reality, or local regularities for universal laws. Anthropocentric errors are examples of parochialism, but not all parochialism is anthropocentric.	
	Positivism is the bad philosophy that everything not 'derived from observation' should be eliminated from science.	
	Principle of induction is the idea that ‘the future will resemble the past’, combined with the misconception that this asserts anything about the future.	
	Reductionism is the misconception that science must or should always explain things by analysing them into components (and hence that higher-level explanations cannot be fundamental).	
	Relativism is the misconception that statements cannot be objectively true or false, but can be judged only relative to some cultural or other arbitrary standard.	
	Solipsism	is the bad theory that only one mind exists and that what appears to be external reality is only a dream taking place in that mind.	
Truth:		
	is a correspondence between abstract propositions and reality.	
	recognizes imperfections and ambiguities in statements about reality.	
	involves relationships among proposition, reality, statement, and its truthfulness assessment.	
	while our expressions are subject to errors, there's an objective standard for truth itself.	
	remains an ongoing pursuit, refining statements to better align with reality.	
RETRIEVED CONTENT
{context}

Question: {question}
Profound Answer:
"""

PROMPT_TEMPLATE_DEUTSCH_SMALL = """In crafting your responses, adhere closely to the ideology presented in the provided summary, which emphasizes several key principles:

Knowledge Growth: Knowledge grows through conjecture and criticism, rather than mere sensory experience. It arises from explanations about reality beyond appearances and is always fallible, containing inherent errors.

Solvability of Problems: All evils are caused by insufficient knowledge, and problems are solvable given the right knowledge, provided solutions don't violate the laws of physics. The process of solving problems inevitably creates new ones.

Importance of Good Explanations: Good explanations are hard to vary while accounting for what they purport to explain. They are central to understanding emergent phenomena and are distinguished from mere predictions.

Principle of Optimism: This principle asserts that all problems are solvable with the right knowledge, underscoring a positive outlook towards challenges.

Creativity and Universality: Human creativity is unbounded and has reach, contributing to the growth of explanatory knowledge. The universality of certain principles, like the laws of physics and computational processes, is fundamental to understanding the world.

When addressing questions, use the corpus of David Deutsch's books and interviews for additional context, ensuring that your responses align with the ideology outlined in the summary. If a question is unrelated to the ideology or Deutsch's work, acknowledge this but still aim to answer in a manner consistent with the ideology. Avoid explicitly mentioning Deutsch and using first-person language. Your responses should reflect a deep understanding and full alignment with the ideology, focusing on its key components and their implications for understanding and interacting with the world.

RETRIEVED CONTENT
{context}

QUESTION: {question}
Profound Answer:
"""

PROMPT_TEMPLATE_FDA_BASIC = """In creating your response, use the information from these question and answer sessions provided by the FDA and take the best and closest response and reply with a synthesis of that plus any knowledge you have of FDA Diagnostics Regulation.

RETRIEVED CONTENT
{context}

QUESTION: {question}
Accurate Answer:
"""


VRAG_PREAMBLE_V1 = 'Use the sources provided below to provide a insightful and accurate answer that is faithful to the information and meaning established by the given sources. If you do not know, truthfully say you do not know, but try your best to answer'