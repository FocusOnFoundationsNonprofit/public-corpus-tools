# ===== START OF FILE primary/conversion.py =====
# Library of functions and execution code to do conversion tasks    

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

# from IPython.display import Markdown, display

from primary.fileops import *

# ---API KEYS AND SECRETS---
from dotenv import load_dotenv
load_dotenv(override=True)  # Load environment variables from .env file
LLAMA_CLOUD_API_KEY = os.environ["LLAMA_CLOUD_API_KEY"]
# INSERT in chalice/config.json "LLAMA_CLOUD_API_KEY": "LLAMA_CLOUD_API_KEY"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY_ORIG"]

# ---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

### LLAMAINDEX
def convert_llamaparse_pdf_to_md(file_path):
    suffix_append = "_llamaparse"
    documents = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown",verbose=True).load_data(file_path)
    #print(documents[0].text[0:1000])
    md_file_path = file_path.rsplit('.', 1)[0] + suffix_append + '.md'  # Replace the file extension with .md
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(documents[0].text)
    print("Completed LlamaParse pdf to md conversion and appended suffix: " + suffix_append + " on input file_path: " + file_path)
    return md_file_path
def mrun_convert_llamaparse_pdf_to_md():
    pass
#if __name__ == "__main__":
    file_path = 'data/misc_books/The Sovereign Child.pdf'
    print(convert_llamaparse_pdf_to_md(file_path))

# TODO WIP - not working because needs different gcloud auth than service account
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
def mtest_convert_llamaindex_gdocs_to_md(gdoc_id_list):
    pass
#if __name__ == "__main__": 
    cur_gdoc_id_list = ['19yTV3UUkOQrfbqOPcL5hhBw9eJyc_5ra5Uz_tKQcs24']
    convert_llamaindex_gdocs_to_md(cur_gdoc_id_list)

### PANDOC
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
def mtest_convert_file_to_md_pandoc():
    pass
#if __name__ == "__main__": 
    #cur_file_path = 'tests/test_manual_files/file_conversion/2021-05-18_Instructions for Use - FloodLAMP QuickColor COVID-19 Test v1.1.docx'
    cur_file_path = 'data/floodlamp_fda/subs/2021-05-18_Pre-EUA Sub - FloodLAMP Proposed Pooling and Asymptomatic Screening Study.docx'
    print(convert_file_to_md_pandoc(cur_file_path))

### MEGAPARSE
def convert_megaparse_pdf_to_md(file_path, use_llama_parse=False, use_vision=False):
    """
    Converts PDF to markdown using LlamaParse, MegaParse with GPT-4 Vision, or UnstructuredParser.
    
    :param file_path: string path to the PDF file
    :param use_llama_parse: bool, whether to use LlamaParse (True) or other parsers (False)
    :param use_vision: bool, whether to use GPT-4 Vision (True) or UnstructuredParser (False)
    :return: string path to the output markdown file
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
def mrun_convert_megaparse_pdf_to_md():
    pass
#if __name__ == "__main__":
    file_path = 'data/misc_books/The Sovereign Child.pdf'
    print(convert_megaparse_pdf_to_md(file_path))

### MS MARKITDOWN
def convert_file_to_md_msmid(file_path, new_suffix="_msmid"):
    """
    Converts a file to markdown using Microsoft's MarkItDown library and saves the output.

    :param file_path: string, path to the input file
    :param new_suffix: string, suffix to append to the output filename
    :return: string, path to the output markdown file
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
def mrun_convert_file_to_md_msmid():
    pass
#if __name__ == "__main__":
    file_path = 'data/misc_books/The Sovereign Child.pdf'
    print(convert_file_to_md_msmid(file_path))

# TODO not tested - from readme at https://github.com/microsoft/markitdown/blob/main/README.md
def get_image_description_msmid(image_file_path, verbose=True):
    # To use Large Language Models for image descriptions, provide llm_client and llm_model:
    client = OpenAI()
    md = MarkItDown(llm_client=client, llm_model="gpt-4o")
    result = md.convert(image_file_path)
    description = result.text_content   
    verbose_print(verbose, description)
    return description

### TEXT
_word_set = None  # Declare the global variable
def initialize_nltk(silent=True):
    """
    Initialize NLTK resources if not already downloaded and report their status.
    Also initializes the word set used for word joining.
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
def mrun_initialize_nltk():
    pass
#if __name__ == "__main__":
    initialize_nltk(silent=False)
# TODO 7-18 RT - consider whether this is OK to be in function, think it was not previously and getting Problems
def load_custom_dictionary(file_path):
    """ Load a custom dictionary from a file. """
    try:
        with open(file_path, 'r') as file:
            return set(word.strip() for word in file)
    except FileNotFoundError:
        print("Custom dictionary file not found.")
        return set()
def lines_alphabetize_and_remove_duplicates(file_path):
    """
    Alphabetizes and removes duplicates from a list.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Strip newline characters and sort the unique lines
    unique_lines = sorted(set(line.strip() for line in lines))
    
    # Overwrite the file with the sorted unique lines
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in unique_lines:
            file.write(line + '\n')
def mrun_lines_alphabetize_and_remove_duplicates():
    pass
#if __name__ == "__main__":
    lines_alphabetize_and_remove_duplicates('data/deutsch/eval_dev/cur_proper_names_o1-preview.txt')
def lines_compare_files(file_path_1, file_path_2, print_same=False, silent=False):
    """
    Compares lines between two files and returns lists of differences and matches.
    
    :param file_path_1: Path to first file
    :param file_path_2: Path to second file
    :param print_same: Boolean to control whether to print lines that appear in both files
    :return: Tuple of (lines only in file 1, lines only in file 2, lines in both files)
    """
    # Read and process lines from both files
    with open(file_path_1, 'r', encoding='utf-8') as file:
        lines_1 = set(line.strip() for line in file.readlines())
    
    with open(file_path_2, 'r', encoding='utf-8') as file:
        lines_2 = set(line.strip() for line in file.readlines())
    
    # Get base filenames for headers
    file_1_name = os.path.basename(file_path_1)
    file_2_name = os.path.basename(file_path_2)
    
    # Find differences and matches
    lines_only_in_1 = sorted(lines_1 - lines_2)
    lines_only_in_2 = sorted(lines_2 - lines_1)
    lines_in_both = sorted(lines_1 & lines_2)
    
    # Print results in markdown format if requested
    if not silent:
        print(f"\n## Lines only in {file_1_name}")
        for line in lines_only_in_1:
            print(line)
        
        print(f"\n\n## Lines only in {file_2_name}")
        for line in lines_only_in_2:
            print(line)

        if print_same:
            print("\n\n## Lines in both files")
            for line in lines_in_both:
                print(line)
    
    return lines_only_in_1, lines_only_in_2, lines_in_both
def mrun_lines_compare_files():
    pass
#if __name__ == "__main__":
    cur_file_path_1 = "data/deutsch/eval_dev/2024-03-06_PB_nova2gen_propernames.txt"
    cur_file_path_2 = "data/deutsch/eval_dev/2024-03-06_PB_dgwhspm_propernames.txt"
    lines_compare_files(cur_file_path_1, cur_file_path_2, print_same=False, silent=False)
def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.replace('__', '')  # Remove double underscores
    text = text.replace('**', '')  # Remove double asterisks
    text = text.strip()
    return text
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
    # Calculate markdown prefix if needed
    md_prefix = '#' * md_level + ' ' if md_level else ''
    
    if start_pos is not None:
        # Calculate space needed before and after title based on start position
        left_count = start_pos - len(md_prefix)
        right_count = total_length - left_count - len(title)
        
        # Ensure minimum padding
        if left_count < 2 or right_count < 2:
            left_count = 2
            right_count = 2
            
        left_chars = char * left_count
        right_chars = char * right_count
    else:
        # Center the title as before
        remaining_space = total_length - len(title) - len(md_prefix)
        if remaining_space < 4:  # Minimum 2 chars on each side
            remaining_space = 4
            
        chars_count = remaining_space // 2
        left_chars = char * chars_count
        right_chars = char * (remaining_space - chars_count)  # Handle odd remaining space
    
    # Build the header
    header = f"{md_prefix}{left_chars} {title} {right_chars}"
    
    # Add newlines as requested
    if start_newline:
        header = '\n' + header
    if end_newline:
        header = header + '\n'
        
    return header
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
    if surrounding_chars is None and surrounding_words is None:
        surrounding_chars = 20  # Default if neither specified
        
    # Get initial character-based bounds
    if surrounding_chars is not None:
        start = max(0, position - surrounding_chars)
        end = min(len(text), position + surrounding_chars)
    else:
        start = 0
        end = len(text)
        
    # Expand to word boundaries if needed
    if surrounding_words is not None or complete_words:
        # Find word boundaries
        while start > 0 and text[start-1].isalnum():
            start -= 1
        while end < len(text) and text[end].isalnum():
            end += 1
            
        if surrounding_words is not None:
            # Count words and expand if needed
            left_text = text[start:position]
            right_text = text[position:end]
            
            left_words = left_text.split()
            right_words = right_text.split()
            
            if len(left_words) > surrounding_words:
                start = position - len(' '.join(left_words[-surrounding_words:]))
            if len(right_words) > surrounding_words:
                end = position + len(' '.join(right_words[:surrounding_words]))
    
    return text[start:end]
def remove_extraneous_spaces_in_words(text, verbose=False):
    """
    Removes extraneous spaces that split valid words in text.
    Uses NLTK's word list with custom additions.
    
    :param text: str, text to process for split words
    :param verbose: bool, whether to print debug info
    :return: str, processed text with split words rejoined
    """
    global _word_set
    if _word_set is None:
        raise RuntimeError("NLTK resources not initialized. Call initialize_nltk() first.")
    
    lines = text.split('\n')
    changes = defaultdict(int)
    
    for i, line in enumerate(lines):
        words_in_line = line.split()
        j = 0
        while j < len(words_in_line) - 1:
            current_word = words_in_line[j]
            next_word = words_in_line[j + 1]
            combined = current_word + next_word
            
            if combined.lower() in _word_set:
                if verbose:
                    print(f"Found split word: '{current_word} {next_word}' -> '{combined}'")
                words_in_line[j] = combined
                words_in_line.pop(j + 1)
                changes[f"{current_word} {next_word} -> {combined}"] += 1
            else:
                j += 1
                
        lines[i] = ' '.join(words_in_line)
    
    if verbose and changes:
        print("\nChanges made:")
        for change, count in changes.items():
            print(f"- {change}: {count} occurrences")
            
    return '\n'.join(lines)
def mtest_remove_extraneous_spaces_in_words():
    pass
#if __name__ == "__main__":
    initialize_nltk(silent=False)
    test_text = 'Humorously, school is about college, and college is about getting a job and sustaining a life. And only then, *in your twen ties*, can food and bathing and clothes and entertainment be about those things in themselves. Shouldn’t childhood be the time when kids are free to explore those things that are integral to life, to learn about and develop relationships with them for their own sake? The magic of childhood is that kids don’t have dependents or even a responsibility to ensure their own sur vival, so it is precisely during this time that a person is most free to engage with the world directly.'
    print(remove_extraneous_spaces_in_words(test_text, verbose=True))

### MARKDOWN
def convert_csv_to_md_table(csv_content):
    """
    Convert CSV content to a markdown table.
    """
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    
    if not rows:
        return ""

    md_table = "| " + " | ".join(rows[0]) + " |\n"
    md_table += "|" + "|".join(["---"] * len(rows[0])) + "|\n"
    
    for row in rows[1:]:
        md_table += "| " + " | ".join(row) + " |\n"
    
    return md_table + "\n"
def analyze_quotes_characters(md_file_path):
    """
    Analyzes a markdown file for different types of quotes and apostrophes.
    Displays a formatted table of quote types, their Unicode values, and counts.
    """
    # Define quotes using Unicode values
    quotes = {
        '\u0027': "Straight single quote/apostrophe",  # Basic ASCII single quote
        '\u0022': "Straight double quote",             # Basic ASCII double quote
        '\u2018': "Left single quote",                 # Left single curly quote
        '\u2019': "Right single quote/apostrophe",     # Right single curly quote
        '\u201C': "Left double quote",                 # Left double curly quote
        '\u201D': "Right double quote"                 # Right double curly quote
    }

    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Print header
    print(f"\nQuote Analysis Report for: {md_file_path}")
    print("=" * 80)
    
    # Find the longest description for padding
    max_desc_length = max(len(desc) for desc in quotes.values())
    
    # Print formatted table header
    print(f"\n{'Description':<{max_desc_length}} {'Unicode':<10} {'Count':<10}")
    print("-" * (max_desc_length + 20))
    
    # Print each quote's information
    for unicode_char, description in quotes.items():
        count = content.count(unicode_char)
        unicode_val = f"U+{ord(unicode_char):04X}"
        print(f"{description:<{max_desc_length}} {unicode_val:<10} {count:<10}")

    return {unicode_char: content.count(unicode_char) for unicode_char in quotes}
def mrun_analyze_quotes_characters():
    pass
#if __name__ == "__main__":
    from primary.docwork import analyze_quotation_marks
    md_file_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/a_run_auto/2020-12-02_Virtual Town Hall 35_fixnames.md"
    analyze_quotes_characters(md_file_path)
    # print("\n=======\n")
    # text = read_complete_text(md_file_path)
    # print(analyze_quotation_marks(text))
def convert_markdown_to_md_mod_text(md_file_path):
    """
    Converts a markdown file to a modified text file with specific replacements.
    Changes the suffix to 'md-mod' and extension to '.txt'.
    Creates a copy of the input file before making modifications.
    
    :param md_file_path: string, path to the markdown file to be converted
    :return: string, path to the modified text file
    """
    # Define the find-replace pairs
    find_replace_pairs = [
        ("## ", "# "),
        ("QUESTION: ", "#### "),
        ("\nTIMESTAMP:", ""),
        ("ANSWER: ", ""),
        #("QUESTION NAME:.*\n(?:.*\n)*?STARS:.*\n", ""),
        ("## transcript", "## Transcript"),
        ("## qa", "## Questions and Answers (AI DRAFT - NOT APPROVED BY PVSD AND WFPD)"),
        ("## meeting chat log", "## Meeting Chat Log"),
        ("\n", "<<NL>>")
    ]

    txt_path = md_file_path.rsplit('.', 1)[0] + '.txt'
    shutil.copy2(md_file_path, txt_path)

    # change the suffix to md-mod by creating a copy
    txt_path = sub_suffix_in_file(txt_path, '_md-mod')
    
    # Apply the find-replace pairs
    total_replacements = find_and_replace_pairs(txt_path, find_replace_pairs, use_regex=True)
    
    print(f"Completed markdown to modified text conversion with {total_replacements} replacements")
    return txt_path
def mrun_convert_markdown_to_md_mod_text():
    pass
#if __name__ == "__main__":
    md_file_path = "data/pv/pv_epc_evac/2024-10-23_PVSD WFPD - Wildfire Preparedness Parent Presentation 3_combo.md"
    md_mod_file_path = convert_markdown_to_md_mod_text(md_file_path)
def combine_files_into_md(file_paths, target_file_path, max_file_size_mb=10):
    """
    Combine multiple files into a single markdown file.
    
    :param file_paths: List of file paths to combine (relative to repo root)
    :param target_file_path: Path for the output markdown file (relative to repo root)
    :param max_file_size_mb: Maximum allowed file size in MB (default: 10)
    :return: The relative path of the combined markdown file
    """
    supported_extensions = ['.txt', '.md', '.py', '.js', '.css', '.html', '.json', '.csv']
    max_file_size_bytes = max_file_size_mb * 1024 * 1024

    # Get the repo root directory
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    combined_file_path = os.path.join(repo_root, target_file_path)
    files_combined = 0

    with open(combined_file_path, 'w', encoding='utf-8') as output_file:
        for relative_path in file_paths:
            file_path = os.path.join(repo_root, relative_path)
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension not in supported_extensions:
                print(f"Skipping unsupported file: {file_name}")
                continue

            if os.path.getsize(file_path) > max_file_size_bytes:
                print(f"Skipping file exceeding size limit: {file_name}")
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()

                output_file.write(f"# {file_name}\n\n")

                if file_extension in ['.py', '.js', '.css', '.html', '.json']:
                    lang = file_extension[1:]  # Remove the dot
                    output_file.write(f"```{lang}\n{content}\n```\n\n")
                elif file_extension == '.csv':
                    output_file.write(convert_csv_to_md_table(content))
                else:
                    output_file.write(f"{content}\n\n")

                files_combined += 1

            except Exception as e:
                print(f"Error processing file {file_name}: {str(e)}")

    print(f"Successfully combined {files_combined} files into {combined_file_path}")
    return target_file_path
def mrun_combine_files_into_md():
    pass
#if __name__ == "__main__":
    file_paths = [
    "projects/math_quiz/math_analysis.html",
    "projects/math_quiz/math_analysis.js",
    # "projects/math_quiz/math_analysis.css",
    "projects/math_quiz/math_quiz.html",
    "projects/math_quiz/math_quiz.js",
    "projects/math_quiz/math_quiz.css"
    ]
    combine_files_into_md(file_paths, 'projects/math_quiz/combined_math_quiz.md')

### HTML
def wrap_qa_blocks_in_details(html_file_path, question_field="CLARIFIED QUESTION", answer_field="CLARIFIED ANSWER"):
    """
    Wraps QA blocks in nested details tags for collapsible viewing.
    
    :param html_file_path: string, path to the HTML file to modify
    :param question_field: string, field name for questions (default: CLARIFIED QUESTION)
    :param answer_field: string, field name for answers (default: CLARIFIED ANSWER)
    :return: None
    """
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to find QA blocks with all content
    qa_block_pattern = r'(<p>QA Block (\d+-\d+)<br>\n' + \
                      f'{question_field}: (.*?)<br>\n' + \
                      f'{answer_field}: (.*?)<br>\n' + \
                      r'.*?</p>)'
    
    def wrap_qa_block(match):
        full_block = match.group(1)
        block_num = match.group(2)
        question = match.group(3)
        answer = match.group(4)
        
        # Add block number to question
        question_with_num = f"{block_num}. {question}"
        
        # Create nested details structure with all content preserved
        wrapped_content = f'''  <details>
    <summary>{question_with_num}</summary>
    <details>
      <summary>{answer}</summary>
      {full_block}</details>
  </details>'''
        
        return wrapped_content
    
    # Replace QA blocks with wrapped versions
    modified_content = re.sub(qa_block_pattern, wrap_qa_block, content, flags=re.DOTALL)
    
    # Write the modified content back
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
def clean_summaries_in_html_file(html_file_path):
    """
    Removes href links from all summary tags in an HTML file while preserving the link text.
    Processes all levels of nested summaries.
    
    :param html_file_path: string, path to the HTML file to clean
    :return: None
    """
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Counter for summaries processed
    summaries_checked = 0
    summaries_cleaned = 0
    
    def clean_summary_content(match):
        nonlocal summaries_checked, summaries_cleaned
        summary_content = match.group(0)  # Get the full match including summary tags
        summaries_checked += 1
        
        # Only process if there's an href
        if 'href=' in summary_content:
            cleaned_content = re.sub(
                r'<a\s+[^>]*href="[^"]*"[^>]*>(.*?)</a>', 
                r'\1', 
                summary_content, 
                flags=re.DOTALL
            )
            if cleaned_content != summary_content:
                summaries_cleaned += 1
            return cleaned_content
        
        return summary_content
    
    # Process summaries recursively until no more changes
    prev_content = ""
    while content != prev_content:
        prev_content = content
        content = re.sub(
            r'(<summary>.*?</summary>)', 
            clean_summary_content, 
            content, 
            flags=re.DOTALL | re.IGNORECASE
        )
    
    print(f"\nProcessed {summaries_checked} summaries, cleaned {summaries_cleaned} with hrefs")
    
    # Write the modified content back
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(content)
def add_additional_html_from_template(html_file_path, template_file_path):
    """
    Adds non-empty HTML elements from a template file to their corresponding parent locations in the target HTML file.
    
    :param html_file_path: string, path to the HTML file to modify
    :param template_file_path: string, path to the template file to add
    :return: None
    """
    from bs4 import BeautifulSoup
    
    # Read both files
    with open(template_file_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse both files
    template_soup = BeautifulSoup(template_content, 'html.parser')
    html_soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process control panel
    template_control_panel = template_soup.find('div', class_='control-panel')
    if template_control_panel:
        target_header = html_soup.find('header')
        if target_header:
            # Remove existing control panel if it exists
            existing_control_panel = target_header.find('div', class_='control-panel')
            if existing_control_panel:
                existing_control_panel.decompose()
            # Add new control panel after h1
            h1_tag = target_header.find('h1')
            if h1_tag:
                h1_tag.insert_after(template_control_panel)
    
    # Process header-row and h3
    template_header_row = template_soup.find('div', class_='header-row')
    if template_header_row:
        target_header = html_soup.find('header')
        if target_header:
            # Find the h3 in the source
            h3_tag = html_soup.find('h3')
            if h3_tag:
                # Get the template h3 placeholder
                template_h3 = template_header_row.find('h3')
                if template_h3:
                    # Replace template h3 with actual h3
                    h3_tag.extract()
                    template_h3.replace_with(h3_tag)
                
                # Add the header-row to target header
                target_header.append(template_header_row)
    
    # Process script
    template_script = template_soup.find('script')
    if template_script:
        # Remove existing script if it exists
        existing_script = html_soup.find('script')
        if existing_script:
            existing_script.decompose()
        # Add new script at end of body
        body_tag = html_soup.find('body')
        if body_tag:
            body_tag.append(template_script)
    
    # Write modified content back to file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(html_soup.prettify()))
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
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to find the specified heading level
    pattern = f'<h{h_level}[^>]*>(.*?)</h{h_level}>'
    
    def modify_heading(match):
        heading_text = match.group(1)
        
        if insert:
            # Split on first underscore
            parts = heading_text.split('_', 1)
            if len(parts) > 1:
                base = parts[1]
                # Remove suffix if requested
                if remove_suffixext:
                    base = base.rsplit('_', 1)[0]
                return f'<h{h_level}>{parts[0]}_{tune_string} {base}</h{h_level}>'
            return match.group(0)  # No underscore found, return unchanged
        else:
            # Simply replace the entire heading text
            return f'<h{h_level}>{tune_string}</h{h_level}>'
    
    # Replace the heading content
    modified_content = re.sub(pattern, modify_heading, content, flags=re.DOTALL)
    
    # Write back to the file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
def convert_markdown_to_html(md_file_path, heading, collapse_h=4, css_file_path=None, cap_first=True):
    """
    Converts a markdown file to an html file using pypandoc and optionally replaces style with external CSS link.
    
    :param md_file_path: string, path to the markdown file to convert
    :param heading: string, heading to use for the document
    :param collapse_h: int, heading level to wrap with details/summary elements (default: 4)
    :param css_file_path: string or None, path to CSS file to link (if None - keeps default styles, if empty string - removes styles)
    :return: string, path to the output HTML file
    """
    html_file_path = md_file_path.replace('.md', '.html')
    convert_text = get_heading(md_file_path, heading)
    
    # Create temporary file with the text to convert
    temp_file_path = 'temp_convert_md_to_html.md'
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(convert_text)

    title = os.path.basename(md_file_path)
    
    pypandoc.convert_file(temp_file_path, 'html5', outputfile=html_file_path, 
        extra_args=[
            '--wrap=none',  # Prevents text wrapping
            '-f', 'gfm+hard_line_breaks',  # Input format
            '-t', 'html5',  # Explicitly set output format to HTML5
            '--standalone',  # Include full document structure with DOCTYPE,
            f'--metadata=title:{title}',  # Use filename as title
            '--columns=999999'  # Use a very large column width  
        ]
    )
    os.remove(temp_file_path)

    # Convert self-closing br tags to HTML5 format
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('<br />', '<br>')
    
    # Add details/summary around h4 tags
    if collapse_h:
        import re
        pattern = f'(<h{collapse_h}.*?</h{collapse_h}>)(.*?)(?=<h{collapse_h}|$)'
        def wrap_section(match):
            heading = match.group(1)  # The complete h4 tag
            content = match.group(2)  # The content after the h4
            return f'<details>\n  <summary>{heading}</summary>{content}\n</details>'
        content = re.sub(pattern, wrap_section, content, flags=re.DOTALL)
    
    # Handle CSS styling
    if css_file_path is not None:  # Check if we should modify styles
        style_start = content.find('<style')
        style_end = content.find('</style>') + 8  # +8 to include '</style>'
        
        if style_start != -1 and style_end != -1:
            if css_file_path == "":  # Empty string - remove styles completely
                content = content[:style_start] + content[style_end:]
            else:  # Non-empty string - replace with CSS link
                css_link = f'<link rel="stylesheet" href="{css_file_path}">'
                content = content[:style_start] + css_link + content[style_end:]
    # Capitalize first letter of headings if requested
    if cap_first:
        def capitalize_heading(match):
            tag_start = match.group(1)  # The opening h tag
            content = match.group(2)     # The heading text
            tag_end = match.group(3)     # The closing h tag
            # Capitalize first letter of actual text content
            content = content[0].upper() + content[1:] if content else content
            return f"{tag_start}{content}{tag_end}"
            
        content = re.sub(r'(<h\d[^>]*>)(.*?)(</h\d>)', capitalize_heading, content)

    # Write the modified content back
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Successful markdown to html conversion for file: {html_file_path}")
    return html_file_path
def mrun_convert_markdown_to_html():
    pass
#if __name__ == "__main__":
    md_file_path = "tests/test_manual_files/md_to_html_dev/2020-12-09_Virtual Town Hall 36_section-titles.md"
    css_file_path = "transcript-with-section-titles.css"
    html_file_path = convert_markdown_to_html(md_file_path, heading="### transcript", css_file_path=css_file_path)
    h_tune_html_file(html_file_path, "COVID-19 Diagnostics FDA", 1)


### OCR IMAGES
import cv2
import pytesseract
from PIL import Image
import numpy as np

def do_ocr_on_image(image_path, mode='color', binary_threshold=None):
    """
    Performs OCR on an image file using specified processing parameters.
    
    :param image_path: string path to the image file (JPEG, PNG, etc.)
    :param mode: string, 'binary', 'grayscale', or 'color' processing mode
    :param binary_threshold: int, binary threshold value (used if mode is 'binary')
    :return: string of the extracted text
    """
    # Read the image using cv2
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image at path: {image_path}")

    if mode == 'binary':
        # Convert to grayscale then apply binary thresholding
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if binary_threshold is not None:
            _, processed_image = cv2.threshold(gray, binary_threshold, 255, cv2.THRESH_BINARY)
        else:
            # Use Otsu's thresholding if no threshold is provided
            _, processed_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Convert back to RGB as required by pytesseract
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)
    elif mode == 'grayscale':
        # Convert to grayscale
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Convert back to RGB as required by pytesseract
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)
    elif mode == 'color':
        # Use original color image, just convert from BGR to RGB
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError("Invalid mode specified. Use 'binary', 'grayscale', or 'color'.")

    # Get OCR text
    text = pytesseract.image_to_string(processed_image)
    
    # Clean and return the text
    return text.strip()
def vary_ocr_on_image(image_path):
    """
    Performs OCR on an image using different modes and binary thresholds,
    outputting results to a markdown file.
    
    :param image_path: string path to the image file
    :return: string path to the output markdown file
    """
    # Constants
    SUFFIX_PAT = '_ocr-vary.md'
    BINARY_THRESHOLDS = [75, 100, 125, 150, 175]  # Range of thresholds to try
    
    # Create output markdown path
    output_path = image_path.rsplit('.', 1)[0] + SUFFIX_PAT
    
    # List to store all results
    results = []
    
    # Try different modes
    for mode in ['color', 'grayscale', 'binary']:
        if mode == 'binary':
            # Try different thresholds for binary mode
            for threshold in BINARY_THRESHOLDS:
                text = do_ocr_on_image(image_path, mode=mode, binary_threshold=threshold)
                results.append((f"## Binary Mode (threshold={threshold})", text))
        else:
            # Process color and grayscale modes
            text = do_ocr_on_image(image_path, mode=mode)
            results.append((f"## {mode.title()} Mode", text))
    
    # Write results to markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        for heading, text in results:
            f.write(f"{heading}\n\n{text}\n\n")
    
    print(f"OCR variations written to: {output_path}")
    return output_path
def mtest_do_ocr_on_image():
    pass
#if __name__ == "__main__":
    image_path = 'data/education/mentava/screenshots/IMG_2878.PNG'
    #print(do_ocr_on_image(image_path)) 
    print(vary_ocr_on_image(image_path))

SUPPORTED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
def create_md_ocr_on_image_folder(folder_path, mode='color', binary_threshold=None):
    """
    Performs OCR on all supported images in a folder and creates a single markdown file
    with the results. Each image's text will be under its own heading.
    
    :param folder_path: string path to the folder containing images
    :param mode: string, 'binary', 'grayscale', or 'color' processing mode
    :param binary_threshold: int, binary threshold value (used if mode is 'binary')
    :return: string path to the output markdown file
    """
    # Get all image files in the folder
    image_files = []
    for ext in SUPPORTED_IMAGE_EXTENSIONS:
        image_files.extend(get_files_in_folder(folder_path, suffixpat_include=ext))
        image_files.extend(get_files_in_folder(folder_path, suffixpat_include=ext.upper()))
    
    if not image_files:
        print(f"No supported image files found in {folder_path}")
        return None
    
    # Create output markdown file path using the folder name
    folder_name = os.path.basename(os.path.normpath(folder_path))
    output_path = os.path.join(folder_path, f"{folder_name}_ocr.md")
    
    # Process each image and write results to markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        for image_path in image_files:
            # Get filename for heading
            filename = os.path.basename(image_path)
            
            # Perform OCR
            try:
                text = do_ocr_on_image(image_path, mode=mode, binary_threshold=binary_threshold)
                
                # Write to markdown file
                f.write(f"## {filename}\n\n{text}\n\n")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                f.write(f"## {filename}\n\nError processing image: {str(e)}\n\n")
    
    print(f"OCR results written to: {output_path}")
    return output_path
def mtest_create_md_ocr_on_image_folder():
    pass
#if __name__ == "__main__":
    folder_path = 'data/education/mentava/screenshots'
    print(create_md_ocr_on_image_folder(folder_path)) 

# ===== END OF FILE primary/conversion.py =====
