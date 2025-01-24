# ===== START OF FILE primary/corpuses.py =====
# Library of functions and execution code to do corpus tasks

import os
import re
import warnings
from pathlib import Path
import csv
from collections import defaultdict
import urllib.parse

from primary.fileops import *
from primary.conversion import *
from primary.structured import *
from primary.llm import *
from primary.aws import *
from primary.dbgen import *
from primary.webflow_api import *
from primary.vectordb import *
from primary.rag import *

# ---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.


# Set the warnings to use a custom format
warnings.formatwarning = custom_formatwarning
# USAGE: warnings.warn(f"Insert warning message here")

CUSTOM_VALIDATORS = {
    "STARS": validate_stars,
    "TOPICS": validate_topics
}

### DEUTSCH CORPUS
DEUTSCH_REQUIRED_FIELDS = ["QUESTION", "TIMESTAMP", "ANSWER", "EDITS", "TOPICS", "STARS"]  
DEUTSCH_FOLDER_PATHS = ["data/deutsch/f8_done_qafixed_and_vrb", "data/deutsch/f8_qafixed_talks"]
def validate_corpus_deutsch():
    validate_blocks_in_folders(DEUTSCH_FOLDER_PATHS, DEUTSCH_REQUIRED_FIELDS, CUSTOM_VALIDATORS, suffixpat_include="_qafixed")
def mrun_deutsch_corpus():
    pass
#if __name__ == "__main__":
    validate_corpus_deutsch()

    # from primary.structured import create_topics_matrix, change_topic_in_folders, review_singlet_topic
    # cur_topics_matrix_csv = "data/deutsch/topics_matrix.csv"
    #cur_topics_matrix_csv = create_topics_matrix(DEUTSCH_FOLDER_PATHS)
    
    # cur_find_replace_pairs = [("%", " percent")]
    # for folder_path in DEUTSCH_FOLDER_PATHS:
    #     apply_to_folder(find_and_replace_pairs, folder_path, cur_find_replace_pairs)
    
    # change_topic_in_folders(DEUTSCH_FOLDER_PATHS, "quantum computer", "quantum computation")
    # review_singlet_topic(DEUTSCH_FOLDER_PATHS, cur_topics_matrix_csv, "z")

    #from primary.vectordb import create_qrag_vectordb
    #create_qrag_vectordb(DEUTSCH_FOLDER_PATHS, "deutsch-transcript-qrag", suffixpat_include="_qafixed")
def mrun_deutsch_download_new_s3_files():
    pass
#if __name__ == "__main__":
    bucket = 'fofsecure'
    s3_path = 's3-qrag-deutsch-v3'
    local_folder = 'exchanges/deutsch_qrag'
    download_new_s3_files(bucket, s3_path, local_folder)
def mrun_deutsch_index_exchanges_and_pii():
    pass
#if __name__ == "__main__":
    root_folder = 'exchanges/deutsch_qrag'  # Replace with your root folder
    exclude_subfolders = None  # ['not-reviewed']
    db_path = index_exchanges_in_db(root_folder, exclude_subfolders)

    # db_path = 'exchanges/deutsch_qrag/exchanges.db'
    users_csv_path = 'exchanges/deutsch_qrag/pii-users.csv'
    copy_exchanges_db_with_user_pii(db_path, users_csv_path) 
def mtest_qrag_2step_deutsch():
    pass
#if __name__ == "__main__":
    cur_query = "What is the meaning of life?"
    cur_routes_dict = ROUTES_DICT_DEUTSCH_V4
    cur_vector_index_name = 'deutsch-transcript-qrag-78f-20240926'
    qrag_2step(cur_query, cur_routes_dict, cur_vector_index_name)

### PV EVAC CORPUS
PV_EVAC_FULL_FIELDS = ["QUESTION", "TIMESTAMP", "ANSWER", "QUESTION NAME", "ANSWER NAME", "ORIGINAL QUESTION", "STATUS", "TOPICS", "STARS"]
PV_EVAC_REQUIRED_FIELDS = ["QUESTION", "TIMESTAMP", "ANSWER", "QUESTION NAME", "ANSWER NAME", "STATUS", "TOPICS", "STARS"]
def mrun_propagate_fields_pv_evac():
    pass
#if __name__ == "__main__":
    file_path = 'data/pv/pv_epc_evac/2023-09-20_PVSD WFPD - Wildfire Preparedness Parent Presentation 1_qaman.md'
    #file_path = "data/pv/pv_epc_evac/2023-11-15_PVSD WFPD - Wildfire Preparedness Parent Presentation 2_qaman.md"
    #file_path = "data/pv/pv_epc_evac/2024-10-23_PVSD WFPD - Wildfire Preparedness Parent Presentation 3_qaman.md"
    propagate_fields_by_subheading(file_path, PV_EVAC_FULL_FIELDS, PV_EVAC_REQUIRED_FIELDS, delete_fields=["QUESTION NUMBER"], heading = "### qa")   

PV_EVAC_FOLDER_PATHS = ["data/pv/pv_epc_evac"]
def validate_corpus_pv_evac():
    validate_blocks_in_folders(PV_EVAC_FOLDER_PATHS, PV_EVAC_REQUIRED_FIELDS, CUSTOM_VALIDATORS, suffixpat_include="_qaprop")
def mrun_pv_epc_corpus():
    pass
#if __name__ == "__main__":
    #validate_corpus_pv_evac()

    # from primary.conversion import convert_markdown_to_md_mod_text
    # file_path = 'data/pv/pv_epc_evac/2023-09-20_PVSD WFPD - Wildfire Preparedness Parent Presentation 1_combo.md'
    # convert_markdown_to_md_mod_text(file_path)
    # file_path = "data/pv/pv_epc_evac/2023-11-15_PVSD WFPD - Wildfire Preparedness Parent Presentation 2_combo.md"
    # convert_markdown_to_md_mod_text(file_path)
    # file_path = "data/pv/pv_epc_evac/2024-10-23_PVSD WFPD - Wildfire Preparedness Parent Presentation 3_combo.md"
    # convert_markdown_to_md_mod_text(file_path)
    
    from primary.vectordb import create_qrag_vectordb
    create_qrag_vectordb(PV_EVAC_FOLDER_PATHS, "pv-evac-qrag", suffixpat_include="_qaprop")
def mtest_qrag_2step_pv_evac():
    pass
#if __name__ == "__main__":
    cur_query = "What are the most important things parents need to know about related to evacuation in schools?"
    cur_routes_dict = ROUTES_DICT_PV_EVAC_V1
    cur_vector_index_name = 'pv-evac-qrag-3f-20241106'
    qrag_2step(cur_query, cur_routes_dict, cur_vector_index_name)

### FDA TOWNHALLS CORPUS
FDA_TOWNHALLS_REQUIRED_FIELDS = ["CLARIFIED QUESTION", "CLARIFIED ANSWER", "VERBATIM QUESTION", "VERBATIM ANSWER", "SPEAKER QUESTION", "SPEAKER ANSWER", "TOPICS", "REVIEW FLAG"]
FDA_TOWNHALLS_QA_FOLDER = "data/floodlamp/reg/fda-townhalls/f5_fixnames/a_done_site"
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
def clean_fda_townhall_file(file_path):
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
def mtest_clean_fda_townhalls_file():
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/docwork_tests/town_hall_tests/clean_tests/2020-10-14_Virtual Town Hall 30.md"
    #cur_file_path = "data/floodlamp_fda/townhalls/f3_md_metadata/2022-06-15_Virtual Town Hall 87.md"
    clean_fda_townhall_file(cur_file_path)
def clean_fda_townhalls_folder(source_folder, destination_folder):
    """
    Cleans the files in the source folder and moves the cleaned files to the destination folder.

    :param source_folder: string of the path to the source folder containing the files to be cleaned.
    :param destination_folder: string of the path to the destination folder where the cleaned files will be moved.
    :return: None
    """
    apply_to_folder(clean_fda_townhall_file, source_folder)
    move_files_with_suffix(source_folder, destination_folder, "_cleaned")
# TODO WIP - add path to find_replace_csv after testing fileops func
def mtest_clean_fda_townhalls_folder():
    pass
#if __name__ == "__main__": 
    source_folder = "data/floodlamp_fda/townhalls/f3_md_metadata"
    destination_folder = "data/floodlamp_fda/townhalls/f4_md_cleaned"
    clean_fda_townhalls_folder(source_folder, destination_folder)
def mrun_fda_townhalls_create_speaker_matrix():
    pass
#if __name__ == "__main__": 
    from primary.docwork import create_speaker_matrix
    create_speaker_matrix('data/floodlamp/reg/fda-townhalls/f5_fixnames','_fixnames', 'matrix_speakers_fdatownhalls.csv')
def mrun_find_and_replace_on_fda_townhalls():
    pass
#if __name__ == "__main__":     
    from primary.fileops import find_and_replace_from_csv, apply_to_folder, sub_suffix_in_file
    
    # ***NOTE*** must manually copy orig-folder to create fixnames_folder, enter that new path below
    orig_folder = 'data/floodlamp_fda/townhalls/f4_md_cleaned_manualedits'
    suffix_orig = '_cleaned'
    fixnames_folder = 'data/floodlamp/reg/fda-townhalls/f5_fixnames/done_auto'
    suffix_new = '_section-titles'
    csv_file_path = 'data/floodlamp/reg/fda-townhalls/names_findandreplace_fda_townhalls.csv'
    
    # TODO need to fix in docwork
    #print(validate_townhalls(cur_folder_path))
    #print(create_speakers_matrix(cur_folder_path))
    #apply_to_folder(sub_suffix_in_file, fixnames_folder, suffix_new, suffixpat_include='_fixnamed')
    # ***NOTE*** must copy files before running
    #find_and_replace_from_csv(fixnames_folder, csv_file_path, suffixpat_include=suffix_orig, verbose=True)
    #apply_to_folder(sub_suffix_in_file, fixnames_folder, suffix_new, suffixpat_include=suffix_orig)
    # NEXT PASS
    find_and_replace_from_csv(fixnames_folder, csv_file_path, suffixpat_include=suffix_new, include_subfolders=True, verbose=True)
def mrun_fda_townhalls_corpus():
    pass
#if __name__ == "__main__":
    #validate_blocks_in_folders([FDA_TOWNHALLS_QA_FOLDER], FDA_TOWNHALLS_REQUIRED_FIELDS, CUSTOM_VALIDATORS, suffixpat_include="_qa-qonly.md")
    #validate_iso_dates_in_filename([FDA_TOWNHALLS_QA_FOLDER], suffixpat_include="_qa-qonly.md")

    from primary.vectordb import create_qrag_vectordb
    create_qrag_vectordb([FDA_TOWNHALLS_QA_FOLDER], "fda-townhalls-qrag", suffixpat_include="_qa-qonly.md", embedding_field="CLARIFIED QUESTION", date_from_filename=True)

def csv_of_num_characters_transcript_and_qa(folder_path, transcript_suffix='_fixnames', qa_suffix='_qa-qonly'):
    """
    Creates a CSV file with character counts for transcript and QA files.

    :param folder_path: string, path to folder containing transcript and QA files
    :param transcript_suffix: string, suffix for transcript files
    :param qa_suffix: string, suffix for QA files
    :return csv_path: string, path to the created CSV file
    """
    # Get all transcript files
    transcript_file_paths = get_files_in_folder(folder_path, suffixpat_include=transcript_suffix)
    
    # Create CSV path in the folder
    csv_path = os.path.join(folder_path, 'character_counts.csv')
    
    # Write to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['base_name', 'transcript_chars', 'qa_chars'])
        
        # Process each file pair
        for transcript_file_path in transcript_file_paths:
            # Get base name (remove suffix and extension)
            base_name = os.path.basename(transcript_file_path)
            base_name = os.path.splitext(base_name)[0]  # Remove extension
            base_name = base_name[:-len(transcript_suffix)]  # Remove suffix
            
            # Get corresponding QA file path
            qa_file_path = sub_suffix_in_str(transcript_file_path, qa_suffix)
            
            # Get text content
            transcript_text = get_heading(transcript_file_path, '### transcript')
            qa_text = get_heading(qa_file_path, '### qa')
            
            # Get character counts
            transcript_chars = len(transcript_text) if transcript_text else 0
            qa_chars = len(qa_text) if qa_text else 0
            
            # Write row
            writer.writerow([base_name, transcript_chars, qa_chars])
    
    return csv_path
def mrun_csv_of_num_characters_transcript_and_qa():
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/done_auto"
    print(csv_of_num_characters_transcript_and_qa(cur_folder_path))
def mrun_section_titles():
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/a_run_auto"
    files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_section-titles')

    for i, file_path in enumerate(files_to_run, 1):
        #write_section_titles(file_path, SCALL_PROMPT_SECTION_TITLE)
        propagate_section_titles_to_qa(file_path)
def mrun_convert_fda_townhalls_transcript_to_html():
    pass
#if __name__ == "__main__":
    md_file_path = "tests/test_manual_files/md_to_html_dev/2020-12-09_Virtual Town Hall 36_section-titles.md"
    css_file_path = "transcript-with-section-titles.css"
    html_file_path = convert_markdown_to_html(md_file_path, heading="### transcript", css_file_path=css_file_path)
    h_tune_html_file(html_file_path, "COVID-19 Diagnostics FDA", 1)
    add_additional_html_from_template(html_file_path, "tests/test_manual_files/md_to_html_dev/additions_transcript.html")
def mrun_convert_fda_townhalls_qa_to_html():
    pass
#if __name__ == "__main__":
    md_file_path = "tests/test_manual_files/md_to_html_dev/2020-12-09_Virtual Town Hall 36_qa-qonly-BRIEF.md"
    css_file_path = "transcript-with-section-titles.css"
    html_file_path = convert_markdown_to_html(md_file_path, heading="### qa", css_file_path=css_file_path)
    h_tune_html_file(html_file_path, "COVID-19 Diagnostics FDA", 1)
    h_tune_html_file(html_file_path, "AI Extracted Question and Answer", 3, insert=False)
    wrap_qa_blocks_in_details(html_file_path, "CLARIFIED QUESTION", "CLARIFIED ANSWER")
    add_additional_html_from_template(html_file_path, "tests/test_manual_files/md_to_html_dev/additions_qa.html")
def mrun_create_html_files_for_fda_townhalls():
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/a_run_auto"
    transcript_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_section-titles.md')
    qa_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_qa-qonly.md')
    css_file_path = ""  # was "transcript-with-section-titles.css"

    # transcripts
    for i, md_file_path in enumerate(transcript_md_files_to_run, 1):
        html_file_path = convert_markdown_to_html(md_file_path, heading="### transcript", css_file_path=css_file_path)
        h_tune_html_file(html_file_path, "FDA COVID-19 Diagnostics", 1)
        clean_summaries_in_html_file(html_file_path)
        add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_transcript.html")
    # save transcript html files

    # qa
    for i, md_file_path in enumerate(qa_md_files_to_run, 1):
        html_file_path = convert_markdown_to_html(md_file_path, heading="### qa", css_file_path=css_file_path)
        h_tune_html_file(html_file_path, "FDA COVID-19 Diagnostics", 1)
        h_tune_html_file(html_file_path, "AI Extracted Question and Answer", 3, insert=False)
        wrap_qa_blocks_in_details(html_file_path, "CLARIFIED QUESTION", "CLARIFIED ANSWER")
        clean_summaries_in_html_file(html_file_path)
        add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_qa.html")
def upload_s3_and_webflow_fda_townhalls(s3_upload=True, s3_prompt_overwrite=True, webflow_upload=True):
    """
    Uploads FDA townhall files to S3 and creates corresponding Webflow CMS items.

    :param s3_upload: bool, whether to upload files to S3
    :param s3_prompt_overwrite: bool, whether to prompt before overwriting S3 files
    :param webflow_upload: bool, whether to create Webflow CMS items
    :return: None
    """
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/a_run_auto"
    transcript_suffix = "_section-titles"
    qa_suffix = "_qa-qonly"
    cur_bucket = "fofpublic"
    cur_s3_path = "fl-c19-fda-townhalls/"
    collection_id = FDA_C19_TOWNHALLS_ID
    CMS_OLD_NAME = "Virtual Town Hall"
    CMS_NEW_NAME = "FDA C19 Dx Town Hall"

    transcript_html_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=transcript_suffix+".html")
    transcript_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=transcript_suffix+".md")
    qa_html_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=qa_suffix+".html")
    qa_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=qa_suffix+".md")
    
    cms_items = []

    # Initialize counters
    total_base_names = set()
    total_files = 0

    # Build mapping of base names to file paths and metadata
    file_mapping = defaultdict(dict)
    for files, s3_subfolder, key_suffix in [
        (transcript_html_files_to_run, "transcripts-html/", "transcript_html"),
        (transcript_md_files_to_run, "transcripts-md/", "transcript_md"),
        (qa_html_files_to_run, "qa-html/", "qa_html"),
        (qa_md_files_to_run, "qa-md/", "qa_md")
    ]:
        for file_path in files:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            base_name = re.sub(f'{transcript_suffix}$|{qa_suffix}$', '', base_name)
            
            # Print status in blue for each base name's first file
            if base_name not in total_base_names:
                total_base_names.add(base_name)
            
            # Upload to S3 if not skipped
            if s3_upload:
                upload_file_to_s3(file_path, bucket=cur_bucket, s3_path=cur_s3_path + s3_subfolder, prompt_overwrite=s3_prompt_overwrite)
                total_files += 1
            
            # Store S3 URL with URL-encoded filename
            encoded_filename = urllib.parse.quote(os.path.basename(file_path))
            s3_url = f"https://{cur_bucket}.s3.us-west-2.amazonaws.com/{cur_s3_path}{s3_subfolder}{encoded_filename}"
            file_mapping[base_name][key_suffix] = s3_url

            # For transcript MD files, read metadata fields
            if key_suffix == "transcript_md":
                _, youtube_url = read_metadata_field_from_file(file_path, "link youtube")
                _, pdf_url = read_metadata_field_from_file(file_path, "link pdf")
                _, slides_url = read_metadata_field_from_file(file_path, "link slides")
                
                file_mapping[base_name]["youtube_url"] = youtube_url
                file_mapping[base_name]["pdf_url"] = pdf_url
                file_mapping[base_name]["slides_url"] = slides_url

    # Print summary after all uploads complete
    print(colored(f"\nS3 Upload Summary:", "green"))
    print(colored(f"  Total base names processed: {len(total_base_names)}", "green"))
    print(colored(f"  Total files uploaded: {total_files}", "green"))
    # Prompt user before proceeding
    response = input("\nPress Enter to continue with Webflow CMS operations, or 'x' to abort: ").lower()
    if response == 'x':
        print("Aborting operation.")
        return

    # Validate Webflow collection once before creating items
    if webflow_upload:
        collection_details = webflow_cms_get_collection_details(collection_id, verbose=True)
        if not collection_details:
            print(colored("Failed to fetch collection details for validation", "red"))
            return

        # Check for existing items
        existing_items = webflow_cms_list_items(collection_id, verbose=True)
        if existing_items:
            existing_names = [item['fieldData'].get('name', '') for item in existing_items]
            existing_items_map = {item['fieldData'].get('name', ''): item['id'] for item in existing_items}
            
            # Check if any of our new items already exist
            overlapping_items = [cms_name for base_name, urls in file_mapping.items() 
                               if (cms_name := base_name.replace(CMS_OLD_NAME, CMS_NEW_NAME)) in existing_names]
            
            if overlapping_items:
                print(colored("\nThe following items already exist in the Webflow CMS:", "blue"))
                for name in overlapping_items:
                    print(f"- {name}")
                
                response = input("\nPress Enter to proceed with updating these Webflow CMS items, or 'x' to abort: ").lower()
                if response == 'x':
                    print("Aborting operation.")
                    return
                
                # Store whether we're updating for later use
                is_updating = True
            else:
                is_updating = False
        else:
            is_updating = False

    # Create CMS items list
    for base_name, urls in file_mapping.items():
        if all(key in urls for key in ["transcript_html", "transcript_md", "qa_html", "qa_md"]):
            cms_name = base_name.replace(CMS_OLD_NAME, CMS_NEW_NAME)
            cms_item = {
                "name": cms_name,
                "s3-transcript-html-url": urls["transcript_html"],
                "s3-qa-html-url": urls["qa_html"],
                "s3-transcript-md-url": urls["transcript_md"],
                "s3-qa-md-url": urls["qa_md"],
                "youtube-url-3": urls.get("youtube_url", ""),  # this has -3 because it was recreated multiple times and it cannot be reset
                "pdf-url": urls.get("pdf_url", ""),
                "slides-url": urls.get("slides_url", "")
            }
            cms_items.append(cms_item)

    # Create or update Webflow CMS items
    if webflow_upload:
        for item in cms_items:
            if is_updating and item['name'] in existing_items_map:
                # Update existing item
                result = webflow_cms_update_item(
                    collection_id=collection_id,
                    item_id=existing_items_map[item['name']],
                    field_data=item,
                    collection_validation=False,  # Skip validation since we did it once
                    verbose=True
                )
                if not result:
                    print(colored(f"Failed to update CMS item for {item['name']}", "red"))
            else:
                # Create new item
                result = webflow_cms_create_item(
                    collection_id=collection_id,
                    field_data=item,
                    collection_validation=False,  # Skip validation since we did it once
                    verbose=True
                )
                if not result:
                    print(colored(f"Failed to create CMS item for {item['name']}", "red"))
def mrun_upload_s3_and_webflow_fda_townhalls():
    pass
#if __name__ == "__main__":
    upload_s3_and_webflow_fda_townhalls(s3_upload=True, s3_prompt_overwrite=False, webflow_upload=True)
def mrun_flex_fda_townhalls_folder():
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/floodlamp/reg/fda-townhalls/f5_fixnames/done_auto"
    transcript_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_section-titles.md')

    for i, md_file_path in enumerate(transcript_md_files_to_run, 1):
        filename = os.path.basename(md_file_path)
        if "Virtual Town Hall" not in filename:
            print(colored(f"File does not contain 'Virtual Town Hall': {filename}", "red"))
        else:
            print(colored(f"File contains 'Virtual Town Hall': {filename}", "green"))

        
        # _, link_slides = read_metadata_field_from_file(md_file_path, "link slides")
        # if link_slides:
        #     print(f"link_slides: {link_slides} for file: {md_file_path}")

def mtest_pinecone_retrieve_fda_townhalls():
    pass
#if __name__ == "__main__":
    test_vector_index_name = 'fda-townhalls-qrag-4f-20250114'
    test_query = "What is the FDA's response to the COVID-19 pandemic?"
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(test_query, test_vector_index_name, num_chunks=5)
    print("Retrieved IDs and scores:")
    for id, score in retrieved_ids_scores.items():
        print(f"{id}: {score}")
    
    print(colored("Retrieving chunks with date range", "yellow"))
    date_range = ["2020-03-01", "2020-03-29"]
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(test_query, test_vector_index_name, num_chunks=5, date_range=date_range)
    print(f"Retrieved IDs and scores with date range of {date_range}:")
    for id, score in retrieved_ids_scores.items():
        print(f"{id}: {score}")
def mtest_qrag_2step_fda_townhalls():
    pass
#if __name__ == "__main__":
    cur_query = "What is the approach to open source EUAs?"
    cur_routes_dict = ROUTES_DICT_FDA_TOWNHALLS_V1
    cur_vector_index_name = 'fda-townhalls-qrag-100f-20250114'
    qrag_2step(cur_query, cur_routes_dict, cur_vector_index_name)
def mtest_s3_upload_fda_townhalls():
    pass
#if __name__ == "__main__":
    json_file_path = "tests/test_manual_files/jsons/qrag-exch_2025-01-01_000000.json"
    s3_path = "s3-qrag-fda-townhalls"
    upload_file_to_s3(json_file_path, bucket='fofsecure', s3_path=s3_path)

''' ’,'   ''' # curvy apostrophe

### CORPUS ORGANIZATION
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
    # Get all files using get_files_in_folder
    files = get_files_in_folder(folder_path, suffixpat_include, suffixpat_exclude, include_subfolders)
    
    # Create dictionaries to store base names and suffixes
    base_names = set()
    suffixes = set()
    file_dict = defaultdict(dict)
    suffix_extensions = {}  # Store extension for each suffix
    
    # Process each file
    for file_path in files:
        # Get relative path
        rel_path = os.path.relpath(file_path, folder_path)
        
        # Get base name without extension
        file_base = os.path.splitext(os.path.basename(file_path))[0]
        extension = os.path.splitext(file_path)[1]
        
        # Get suffix
        suffix = get_suffix(file_path)
        if suffix is None:
            base_name = file_base
        else:
            # Remove suffix from base name
            base_name = file_base[:-len(suffix)]
        
        # Add to sets and dictionary
        base_names.add(base_name)
        if suffix:
            suffixes.add(suffix)
            suffix_extensions[suffix] = extension
        file_dict[base_name][suffix if suffix else ''] = file_path
    
    # Convert sets to sorted lists
    base_names = sorted(base_names)
    suffixes = sorted(suffixes)
    
    # Create CSV file path
    csv_path = os.path.join(folder_path, 'files_by_suffix.csv')
    
    # Write to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header row with suffixes and extensions
        header = ['base_filename'] + [(suffix + suffix_extensions[suffix]) if suffix else 'no_suffix' for suffix in suffixes]
        writer.writerow(header)
        
        # Write data rows
        for base_name in base_names:
            row = [base_name]
            for suffix in suffixes:
                row.append(file_dict[base_name].get(suffix, ''))
            writer.writerow(row)
    
    return csv_path
def mrun_create_csv_of_files_by_suffix():
    pass
#if __name__ == "__main__":
    create_csv_of_files_by_suffix("data/deutsch/f8_done_qafixed_and_vrb", suffixpat_include=".md")
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
    if not folders:
        raise ValueError("No folders provided")

    # Initialize collections for all folders
    all_base_names = set()
    all_suffixes = set()
    file_dict = defaultdict(lambda: defaultdict(list))  # Nested defaultdict to store lists of paths
    suffix_extensions = {}  # Store extension for each suffix
    
    # Process each folder
    for folder_path in folders:
        files = get_files_in_folder(folder_path, suffixpat_include, suffixpat_exclude, include_subfolders)
        
        # Process each file
        for file_path in files:
            file_base = os.path.splitext(os.path.basename(file_path))[0]
            extension = os.path.splitext(file_path)[1]
            
            suffix = get_suffix(file_path)
            if suffix is None:
                base_name = file_base
            else:
                base_name = file_base[:-len(suffix)]
                suffix_extensions[suffix] = extension
            
            # Add to collections
            all_base_names.add(base_name)
            if suffix:
                all_suffixes.add(suffix)
            
            # Add path to the list for this base_name/suffix combination
            file_dict[base_name][suffix if suffix else ''].append(file_path)
    
    # Create CSV in the first folder
    csv_path = os.path.join(folders[0], 'files_by_suffix.csv')
    
    # Convert sets to sorted lists
    all_base_names = sorted(all_base_names)
    all_suffixes = sorted(all_suffixes)
    
    # Write to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header row with suffixes and extensions
        header = ['base_filename'] + [(suffix + suffix_extensions[suffix]) if suffix else 'no_suffix' 
                                    for suffix in all_suffixes]
        writer.writerow(header)
        
        # Write data rows
        for base_name in all_base_names:
            row = [base_name]
            for suffix in all_suffixes:
                paths = file_dict[base_name].get(suffix, [])
                if not paths:
                    row.append('')  # Empty cell if no files exist
                elif len(paths) == 1:
                    row.append(paths[0])  # Single path if only one file exists
                else:
                    # MULTI entry if multiple files exist
                    row.append('MULTI=' + ','.join(paths))
            writer.writerow(row)
    
    return csv_path
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
    if not folders:
        raise ValueError("No folders provided")

    # Create initial CSV from first folder
    csv_path = create_csv_of_files_by_suffix(folders[0], suffixpat_include, suffixpat_exclude, include_subfolders)
    
    if len(folders) == 1:
        return csv_path

    # Read existing CSV into memory
    data = []
    headers = []
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get header row
        data = list(reader)

    # Process additional folders
    base_name_idx = {row[0]: i for i, row in enumerate(data)}  # Index of existing base names
    suffix_idx = {col: i for i, col in enumerate(headers)}  # Index of existing suffixes

    for folder in folders[1:]:
        # Get files from current folder
        files = get_files_in_folder(folder, suffixpat_include, suffixpat_exclude, include_subfolders)
        
        for file_path in files:
            file_base = os.path.splitext(os.path.basename(file_path))[0]
            extension = os.path.splitext(file_path)[1]
            
            suffix = get_suffix(file_path)
            if suffix is None:
                base_name = file_base
                col_header = 'no_suffix'
            else:
                base_name = file_base[:-len(suffix)]
                col_header = suffix + extension

            # Add new suffix column if needed
            if col_header not in suffix_idx:
                headers.append(col_header)
                suffix_idx[col_header] = len(headers) - 1
                for row in data:
                    row.append('')

            # Add new base name row if needed
            if base_name not in base_name_idx:
                new_row = [''] * len(headers)
                new_row[0] = base_name
                data.append(new_row)
                base_name_idx[base_name] = len(data) - 1

            # Update cell value
            col_idx = suffix_idx[col_header]
            row_idx = base_name_idx[base_name]
            current_value = data[row_idx][col_idx]
            
            if not current_value:
                data[row_idx][col_idx] = file_path
            else:
                # Handle multiple files
                if current_value.startswith('MULTI='):
                    data[row_idx][col_idx] = current_value + ',' + file_path
                else:
                    data[row_idx][col_idx] = 'MULTI=' + current_value + ',' + file_path

    # Sort rows by base name
    data.sort(key=lambda x: x[0])

    # Write updated CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

    return csv_path
def mrun_create_csv_of_files_by_suffix_folders():
    pass
#if __name__ == "__main__":
    create_csv_of_files_by_suffix_folders(DEUTSCH_FOLDER_PATHS, suffixpat_include=".md")


# ===== END OF FILE primary/corpuses.py =====
