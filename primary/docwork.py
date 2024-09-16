import os
import re


### COMMON TEXT
# TODO 7-18 RT - consider whether this is OK to be in function, think it was not previously and getting Problems
def load_custom_dictionary(file_path):
    '''
    # import nltk
    # nltk.download('words')
    # nltk.download('punkt')  # Added to download the 'punkt' tokenizer models
    # from nltk.corpus import words
# TODO rename and comment this function so it's more clear what it does
    '''
    """ Load a custom dictionary from a file. """
    try:
        with open(file_path, 'r') as file:
            return set(word.strip() for word in file)
    except FileNotFoundError:
        print("Custom dictionary file not found.")
        return set()


### TRANSCRIPTS
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

# TODO consider refactor by creating new function to determine if a line is a speaker line get_speaker_name(line) and return None if not speaker line but consider what to do if speaker line is invalid
# TODO sync this with validate qa
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


### PROPER NAMES
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
