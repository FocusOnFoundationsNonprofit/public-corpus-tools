# ===== START OF FILE primary/corpuses.py =====
# Library of functions and execution code to do corpus tasks

import os
import re
import warnings
from pathlib import Path
import csv
from collections import defaultdict
import urllib.parse
import pickle

from primary.fileops import *
from primary.transcribe import *
from primary.conversion import *
from primary.structured import *
from primary.llm import *
from primary.aws import *
from primary.dbgen import *
from primary.webflow_api import *
from primary.vectordb import *
from primary.rag import *
from primary.rag_prompts_routes import *

# ---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.


# Set the warnings to use a custom format
warnings.formatwarning = custom_formatwarning
# USAGE: warnings.warn(f"Insert warning message here")

CUSTOM_VALIDATORS = {
    "STARS": validate_stars,
    "TOPICS": validate_topics
}

### S3 WEBFLOW UPLOADS
def collect_s3_source_files(folder_path, transcript_suffix, qa_suffix):
    transcript_html = get_files_in_folder(folder_path, suffixpat_include=transcript_suffix + ".html")
    transcript_md   = get_files_in_folder(folder_path, suffixpat_include=transcript_suffix + ".md")
    qa_html         = get_files_in_folder(folder_path, suffixpat_include=qa_suffix + ".html")
    qa_md           = get_files_in_folder(folder_path, suffixpat_include=qa_suffix + ".md")
    return transcript_html, transcript_md, qa_html, qa_md
def build_s3_source_file_mapping(files_group, config, s3_upload=True, s3_prompt_overwrite=True):
    # files_group is a tuple of file lists (transcript_html, transcript_md, qa_html, qa_md)
    transcript_html, transcript_md, qa_html, qa_md = files_group
    file_mapping = defaultdict(dict)
    total_base_names = set()
    total_files = 0

    file_groups = [
        (transcript_html, "transcripts-html/", "transcript_html"),
        (transcript_md, "transcripts-md/", "transcript_md"),
        (qa_html, "qa-html/", "qa_html"),
        (qa_md, "qa-md/", "qa_md")
    ]
    
    for files, s3_subfolder, key_suffix in file_groups:
        for file_path in files:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            base_name = re.sub(f'{config["transcript_suffix"]}$|{config["qa_suffix"]}$', '', base_name)
            total_base_names.add(base_name)
            
            if s3_upload:
                upload_file_to_s3(
                    file_path, 
                    bucket=config["bucket"], 
                    s3_path=config["s3_path"] + s3_subfolder, 
                    prompt_overwrite=s3_prompt_overwrite
                )
                total_files += 1
            
            encoded_filename = urllib.parse.quote(os.path.basename(file_path))
            s3_url = f"https://{config['bucket']}.s3.us-west-2.amazonaws.com/{config['s3_path']}{s3_subfolder}{encoded_filename}"
            file_mapping[base_name][key_suffix] = s3_url

            # Handle metadata fields for transcript MD files
            if key_suffix == "transcript_md":
                # Get metadata field mapping from config, or use empty dict if not provided
                metadata_mapping = config.get("metadata_field_mapping", {})
                
                # Read each metadata field and map to the corresponding CMS field name
                for md_field, cms_field in metadata_mapping.items():
                    _, field_value = read_metadata_field_from_file(file_path, md_field)
                    # Convert 'link youtube' -> 'youtube_url' for internal mapping
                    internal_key = cms_field.replace('-', '_').lower()
                    file_mapping[base_name][internal_key] = field_value

    print(f"S3 Upload Summary: {len(total_base_names)} base names processed, {total_files} files uploaded.")
    return file_mapping
def create_cms_item_list(file_mapping, config):
    cms_items = []
    metadata_mapping = config.get("metadata_field_mapping", {})
    # Create reverse mapping from internal keys to CMS field names
    reverse_mapping = {cms_field.replace('-', '_').lower(): cms_field 
                      for _, cms_field in metadata_mapping.items()}
    
    for base_name, urls in file_mapping.items():
        if all(key in urls for key in ["transcript_html", "transcript_md", "qa_html", "qa_md"]):
            cms_name = base_name
            if config.get("cms_item_name_old") and config.get("cms_item_name_new"):
                cms_name = base_name.replace(config["cms_item_name_old"], config["cms_item_name_new"])
            
            # Start with required fields
            cms_item = {
                "name": cms_name,
                "s3-transcript-html-url": urls["transcript_html"],
                "s3-qa-html-url": urls["qa_html"],
                "s3-transcript-md-url": urls["transcript_md"],
                "s3-qa-md-url": urls["qa_md"],
            }
            
            # Add mapped metadata fields
            for internal_key, cms_field in reverse_mapping.items():
                cms_item[cms_field] = urls.get(internal_key, "")
            
            cms_items.append(cms_item)
    
    return cms_items
def process_webflow_cms(cms_items, config, webflow_cms_prompt_overwrite=True):
    collection_details = webflow_cms_get_collection_details(config["collection_id"], verbose=True)
    if not collection_details:
        print("Failed to fetch collection details for validation")
        return
    
    existing_items = webflow_cms_list_items(config["collection_id"], verbose=True)
    is_updating = False
    existing_items_map = {}
    if existing_items:
        existing_names = [item['fieldData'].get('name', '') for item in existing_items]
        existing_items_map = {item['fieldData'].get('name', ''): item['id'] for item in existing_items}
        overlapping_items = [cms_name for cms_name in 
                             [item["name"] for item in cms_items] if cms_name in existing_names]
        if overlapping_items:
            print("The following items already exist in the Webflow CMS:")
            for name in overlapping_items:
                print(f"- {name}")
            if webflow_cms_prompt_overwrite:
                response = input("Press Enter to proceed with updating these items, or 'x' to abort: ").lower()
                if response == 'x':
                    print("Aborting operation.")
                    return
            is_updating = True
    
    for item in cms_items:
        if is_updating and item['name'] in existing_items_map:
            result = webflow_cms_update_item(
                collection_id=config["collection_id"],
                item_id=existing_items_map[item['name']],
                field_data=item,
                collection_validation=False,
                verbose=True
            )
            if not result:
                print(f"Failed to update CMS item for {item['name']}")
        else:
            result = webflow_cms_create_item(
                collection_id=config["collection_id"],
                field_data=item,
                collection_validation=False,
                verbose=True
            )
            if not result:
                print(f"Failed to create CMS item for {item['name']}")
def process_corpus_s3_webflow_upload(config, s3_upload=True, webflow_upload=True, s3_prompt_overwrite=True, webflow_cms_prompt_overwrite=True):
    # Step 1: Collect Files
    files = collect_s3_source_files(config["folder_path"], config["transcript_suffix"], config["qa_suffix"])
    
    # Step 2: Build File Mapping and Upload to S3
    file_mapping = build_s3_source_file_mapping(files, config, s3_upload, s3_prompt_overwrite)
    
    # Step 3: Pause for confirmation before Webflow operations (if desired)
    if webflow_upload:
        response = input("Press Enter to continue with Webflow CMS operations, or 'x' to abort: ").lower()
        if response == 'x':
            print("Aborting operation.")
            return
    
    # Step 4: Create CMS Item List
    cms_items = create_cms_item_list(file_mapping, config)
    
    # Step 5: Process Webflow CMS Items
    if webflow_upload:
        process_webflow_cms(cms_items, config, webflow_cms_prompt_overwrite)
def mrun_process_corpus_s3_webflow_upload():
    pass
#if __name__ == "__main__":
    config = CONFIG_S3_WEBFLOW_UPLOAD_MY_CORPUS_HERE
    process_corpus_s3_webflow_upload(config, s3_upload=True, webflow_upload=True, s3_prompt_overwrite=True, webflow_cms_prompt_overwrite=True)

### GENERIC CORPUS
def count_chars_words_tokens(text):
    """
    Counts the number of characters, words, and tokens in a given text.

    :param text: string of text to be analyzed.
    :return: tuple of integers representing the number of characters, words, and tokens in the input text.
    """
    num_chars = len(text)
    num_words = len(text.split())
    num_tokens = count_tokens(text)  # in llm.py
    return num_chars, num_words, num_tokens
def count_chars_words_tokens_in_file(file_path):
    """
    Counts the number of characters, words, and tokens in a given file.

    :param file_path: string of the path to the file to be analyzed.
    :return: tuple of integers representing the number of characters, words, and tokens in the input file.
    """
    try:
        _, content = read_metadata_and_content(file_path)
    except:
        # If read_metadata_and_content fails, read the entire file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    
    # Check if content is actually text
    if not isinstance(content, str):
        raise ValueError(f"File content is not text: {file_path}")
    
    return count_chars_words_tokens(content)
def mtest_count_chars_words_tokens_in_file():
    pass
#if __name__ == "__main__":
    file_path = "data/sovereign-child/book/2025-01-11_Book - The Sovereign Child by Dr Aaron Stupple_section-titles.md"
    num_chars, num_words, num_tokens = count_chars_words_tokens_in_file(file_path)
    print(f"{'Number of characters:':<22} {num_chars:>10,}")
    print(f"{'Number of words:':<22} {num_words:>10,}")
    print(f"{'Number of tokens:':<22} {num_tokens:>10,}")
def create_csv_with_chars_words_tokens(output_file_path, folder_list, suffixpat_include=None, include_subfolders=False):
    """
    Creates a CSV file with the number of characters, words, and tokens for each file in a given folder.

    :param output_file_path: string of the path to the output CSV file.
    :param folder_list: list of strings representing paths to folders to be analyzed.
    :param suffixpat_include: string of the suffix pattern to be included in the analysis.
    :param include_subfolders: boolean indicating whether to include subfolders in the analysis.
    """
    # Create a list to store the results
    results = []
    
    # Process each folder separately
    for folder_path in folder_list:
        print(f"Processing folder: {folder_path}")
        
        # Get files for this folder
        folder_files = get_files_in_folder(folder_path, suffixpat_include=suffixpat_include, include_subfolders=include_subfolders)
        
        # Process each file in this folder
        for file_path in folder_files:
            file_name = os.path.basename(file_path)
            num_chars, num_words, num_tokens = count_chars_words_tokens_in_file(file_path)
            results.append([file_path, file_name, num_chars, num_words, num_tokens])
            print(f"  {file_name}: {num_chars} chars, {num_words} words, {num_tokens} tokens")
        
        # Print blank line after each folder to delineate sections
        print("\n")

    # Write the combined results to a CSV file
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Path', 'File Name', 'Characters', 'Words', 'Tokens'])
        writer.writerows(results)

#### TRANSCRIBE
def mrun_transcribe_using_callback():
    pass
#if __name__ == "__main__":
    videos_to_process = [  #  (title, link)
        ("2025-09-24_Alex Springer Award - Sam Altman and David Deutsch discuss AGI", "https://youtu.be/WZ22AJmuKKQ"),
    ] 
    process_multiple_videos(videos_to_process) # default set to audio_inbox, 'whisper-medium' 'nova-2-general' 'whisper-large' 'nova-2-meeting' 'enhanced-meeting'

    print("TESTING DOWNLOAD DEEPGRAM CALLBACK WAITING")     
    download_deepgram_callback_waiting()
def mrun_transcribe_with_audio_only():
    pass
#if __name__ == "__main__":
    audio_file_path = "data/audio_inbox/2025-09-24_Alex Springer Award - Sam Altman and David Deutsch discuss AGI.mp3"
    link = "https://youtu.be/WZ22AJmuKKQ"  # Can be None if no YouTube link exists
    model = "whisper-medium"  # Or other Deepgram model like "whisper-medium"
    process_deepgram_transcription_sync_from_audio_file(audio_file_path, link, model)

### DEUTSCH CORPUS
def mrun_create_deustch_qa_from_prepqa():
    pass
#if __name__ == "__main__":
    apply_to_folder(create_qa_file_select_speaker, 'data/deutsch/f5_run_qa_now', 'David Deutsch', FCALL_PROMPT_QA_DEUTSCH, suffixpat_include='_prepqa')
def mrun_create_deustch_qa_multi():
    pass
#if __name__ == "__main__":
    source_folder = 'data/deutsch/f6_needs_qafixed'
    for qa_file in os.listdir(source_folder):
        if qa_file.endswith('_qafixed.md'):
            qa_file_path = os.path.join(source_folder, qa_file)
            qa_multi_file_path = create_qa_multi_file_from_qa(qa_file_path, verbose=True)
            
            # Create copy with space appended to filename
            copy_folder = 'data/deutsch/fx_archive'
            qa_multi_file_name = os.path.basename(qa_multi_file_path)
            qa_multi_file_name_copy = qa_multi_file_name.replace('.md', ' copy.md')
            qa_multi_file_path_copy = os.path.join(copy_folder, qa_multi_file_name_copy)
            
            # Copy the file
            shutil.copy2(qa_multi_file_path, qa_multi_file_path_copy)
            print(f"Processed {qa_file}")

            set_last_updated(qa_multi_file_path, "RT multi-QA manual edits")


DEUTSCH_REQUIRED_FIELDS = ["QUESTION", "TIMESTAMP", "ANSWER", "TOPICS", "STARS"]  
DEUTSCH_FOLDER_PATHS = ["data/deutsch/f8_done_qafixed_and_vrb", "data/deutsch/f8_qafixed_talks"]
def mrun_renumber_multi_qa_deutsch():
    pass
#if __name__ == "__main__":
    for folder in ["data/deutsch/f9_process"]: #DEUTSCH_FOLDER_PATHS:
        apply_to_folder(renumber_multi_qa, folder, suffixpat_include="_qa-multi.md")
def mrun_get_num_questions_multi_qa_deutsch():
    pass
#if __name__ == "__main__":
    total_questions = 0
    for folder in DEUTSCH_FOLDER_PATHS:
        for file in os.listdir(folder):
            if file.endswith("_qa-multi.md"):
                file_path = os.path.join(folder, file)
                num_questions = get_num_questions_multi_qa(file_path)
                total_questions += num_questions
                #print(f"{file}: {num_questions} questions")
    print(f"\nTotal questions across all files: {total_questions}")
def validate_corpus_deutsch():
    validate_blocks_in_folders(DEUTSCH_FOLDER_PATHS, DEUTSCH_REQUIRED_FIELDS, CUSTOM_VALIDATORS, suffixpat_include="_qa-multi")
def mrun_validate_corpusdeutsch():
    pass
#if __name__ == "__main__":
    validate_corpus_deutsch()
def mrun_create_qrag_vector_db_deutsch(): # RUN VALIDATION FIRST
    pass
#if __name__ == "__main__":
    create_qrag_vectordb(DEUTSCH_FOLDER_PATHS, "deutsch-transcript-qrag", suffixpat_include="_qa-multi.md", embedding_field="QUESTION", date_from_filename=True, dummy_run=False)
def mrun_misc_corpus_deutsch():
    pass
#if __name__ == "__main__":
    cur_topics_matrix_csv = "data/deutsch/topics_matrix.csv"
    # cur_topics_matrix_csv = create_topics_matrix(DEUTSCH_FOLDER_PATHS)
    
    # cur_find_replace_pairs = [("%", " percent")]
    # for folder_path in DEUTSCH_FOLDER_PATHS:
    #     apply_to_folder(find_and_replace_pairs, folder_path, cur_find_replace_pairs)
    
    # change_topic_in_folders(DEUTSCH_FOLDER_PATHS, "quantum computer", "quantum computation")
    # review_singlet_topic(DEUTSCH_FOLDER_PATHS, cur_topics_matrix_csv, "z")
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
    cur_routes_dict = ROUTES_DICT_DEUTSCH_M1
    cur_vector_index_name = 'deutsch-transcript-qrag-95f-20250923'
    qrag_2step(cur_query, cur_vector_index_name, 10, cur_routes_dict)

def mrun_find_and_replace_on_deutsch():
    pass
#if __name__ == "__main__":  
    csv_file_path = "data/deutsch/findandreplace_deutsch.csv"
    # folder_path = "data/deutsch/dd_test_files"
    # suffixpat_include = "_vrb.md"
    # find_and_replace_from_csv(folder_path, csv_file_path, suffixpat_include=suffixpat_include, include_subfolders=False, include_metadata=True, verbose=True)
    # # ALL
    folders = ["data/deutsch/f8_done_qafixed_and_vrb", "data/deutsch/f8_qafixed_talks", "data/deutsch/f8_vrb_talks_only"]
    suffix_pats = ["_vrb.md", "_qafixed.md"]
    for folder in folders:
        for suffix_pat in suffix_pats:
            find_and_replace_from_csv(folder, csv_file_path, suffixpat_include=suffix_pat, include_subfolders=False, include_metadata=True, verbose=True)
def mrun_move_files_deutsch():
    pass
#if __name__ == "__main__":
    source_folders = DEUTSCH_FOLDER_PATHS
    destination_folder = "data/deutsch/fx_archive"
    suffixpat_include = "_propernames.md"
    for source_folder in source_folders:
        move_files_with_suffix(source_folder, destination_folder, suffixpat_include)

def mrun_create_top_stars_files_deutsch():  # 2-4-25 RT
    pass
#if __name__ == "__main__":
    folders = DEUTSCH_FOLDER_PATHS
    #folders = ["data/deutsch/f9_process"]  # 1st copy orig _qafixed and _vrb to this folder, then delete them after and copy new top-stars files there
    destination_folder = "data/deutsch/dd_top-stars_qa-multi"
    for folder in folders:
        qafixed_files = get_files_in_folder(folder, suffixpat_include='_qa-multi.md')
        for qafixed_file in qafixed_files:
            qa_top_stars_file_path = create_qa_top_stars_file(qafixed_file, num_blocks=5)
            print(create_transcript_top_stars_file(qa_top_stars_file_path))
        move_files_with_suffix(folder, destination_folder, suffixpat_include='_qa-topstars.md')
        move_files_with_suffix(folder, destination_folder, suffixpat_include='_vrb-topstars.md')
def mrun_create_html_files_for_deutsch():  # 2-3-25 RT
    pass
#if __name__ == "__main__":
    cur_folder_path = "data/deutsch/dd_top-stars_qa-multi"
    #cur_folder_path = "data/deutsch/dd_test_files"
    transcript_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_vrb-topstars.md')
    qa_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_qa-topstars.md')
    css_file_path = ""  # was "transcript-with-section-titles.css" for local testing
    new_heading_text = "David Deutsch Corpus" # 9-23-25 comment out h_tune_html_file(html_file_path, new_heading_text, 1)

    # transcripts
    for i, md_file_path in enumerate(transcript_md_files_to_run, 1):
        html_file_path = convert_markdown_to_html(md_file_path, heading="### transcript", css_file_path=css_file_path)
        #h_tune_html_file(html_file_path, new_heading_text, 1)
        clean_summaries_in_html_file(html_file_path)
        add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_transcript.html")

    # qa
    for i, md_file_path in enumerate(qa_md_files_to_run, 1):
        html_file_path = convert_markdown_to_html(md_file_path, heading="### qa", css_file_path=css_file_path)
        #h_tune_html_file(html_file_path, new_heading_text, 1)
        h_tune_html_file(html_file_path, "Extracted Question and Answer", 3, insert=False)
        wrap_qa_blocks_in_details(html_file_path, "QUESTION", "ANSWER")
        clean_summaries_in_html_file(html_file_path)
        add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_qa.html")
    
WEBFLOW_CMS_COLLECTION_ID_DEUTSCH_TRANSCRIPTS = "67a249cf5625c057b2fd345c"
CONFIG_S3_WEBFLOW_UPLOAD_DEUTSCH_TRANSCRIPTS = {
    "folder_path": "data/deutsch/f9_process", #"data/deutsch/dd_top-stars_qa-multi",
    "transcript_suffix": "_vrb-topstars",
    "qa_suffix": "_qa-topstars",
    "bucket": "fofpublic",
    "s3_path": "deutsch-sources-top-stars/",
    "collection_id": WEBFLOW_CMS_COLLECTION_ID_DEUTSCH_TRANSCRIPTS,
    "cms_item_name_old": "",
    "cms_item_name_new": "",
    "metadata_field_mapping": {
        "link youtube": "youtube-url",
        "link spotify": "spotify-url"
    }
}
def mrun_process_corpus_s3_webflow_upload():
    pass
#if __name__ == "__main__":
    config = CONFIG_S3_WEBFLOW_UPLOAD_DEUTSCH_TRANSCRIPTS
    process_corpus_s3_webflow_upload(config, s3_upload=True, webflow_upload=False, s3_prompt_overwrite=False, webflow_cms_prompt_overwrite=True)

def mrun_copy_suffix_files_deutsch():
    pass
#if __name__ == "__main__":
    # source_folder_list = DEUTSCH_FOLDER_PATHS
    # destination_folder = "/Users/randytrue/Documents/Code/copyrighted-files-private/dd-transcripts"
    # suffixpat_include_list = ["_vrb", "_read-qafixed"]
    
    # FOR RAW _dgwhspm files
    source_folder_list = ["data/deutsch/f9_raw"]
    destination_folder = "/Users/randytrue/Documents/Code/copyrighted-files-private/dd-transcripts"
    suffixpat_include_list = ["_dgwhspm.json", "_dgwhspm.md"]
    
    for source_folder in source_folder_list:
        for suffixpat_include in suffixpat_include_list:
            results = copy_files_with_suffix(source_folder, destination_folder, suffixpat_include)
            file_count = len(results)
            print(f"{file_count} files copied from '{source_folder}' with suffix '{suffixpat_include}'")
def mrun_create_csv_with_chars_words_tokens_deutsch():
    pass
#if __name__ == "__main__":
    source_folder_list = ["data/deutsch/f8_done_qafixed_and_vrb", "data/deutsch/f8_qafixed_talks", "data/deutsch/f8_vrb_talks_only"]
    output_file_path = "data/deutsch/dd_chars_words_tokens.csv"
    suffixpat_include = "_vrb"
    include_subfolders = False
    create_csv_with_chars_words_tokens(output_file_path, source_folder_list, suffixpat_include, include_subfolders)


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
    
    create_qrag_vectordb(PV_EVAC_FOLDER_PATHS, "pv-evac-qrag", suffixpat_include="_qaprop", embedding_field="QUESTION", date_from_filename=True)
def mtest_qrag_2step_pv_evac():
    pass
#if __name__ == "__main__":
    cur_query = "What are the most important things parents need to know about related to evacuation in schools?"
    cur_routes_dict = ROUTES_DICT_PV_EVAC_V1
    cur_vector_index_name = 'pv-evac-qrag-3f-20241106'
    qrag_2step(cur_query, cur_routes_dict, cur_vector_index_name)
def mrun_create_pv_evac_multi_qa():  # 10-11-2025 RT
    pass
#if __name__ == "__main__":
    qa_file_path = "data/pv/pv_epc_evac/f2_draftqa/2024-10-23_PVSD WFPD - Wildfire Preparedness Parent Presentation 3_qafixed.md"
    qa_multi_file_path = create_qa_multi_file_from_qa(qa_file_path, verbose=True)
def mrun_renumber_pv_evacmulti_qa():
    pass
#if __name__ == "__main__":
    cur_file_path = "data/pv/pv_epc_evac/2024-10-23_PVSD WFPD - Wildfire Preparedness Parent Presentation 3_qa-multi.md"
    renumber_multi_qa(cur_file_path, verbose=True)

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
def mrun_corpus_fda_townhalls():
    pass
#if __name__ == "__main__":
    #validate_blocks_in_folders([FDA_TOWNHALLS_QA_FOLDER], FDA_TOWNHALLS_REQUIRED_FIELDS, CUSTOM_VALIDATORS, suffixpat_include="_qa-qonly.md")
    #validate_iso_dates_in_filename([FDA_TOWNHALLS_QA_FOLDER], suffixpat_include="_qa-qonly.md")
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
def mrun_flex_fda_townhalls_folder():  # for running whatever you want on the folder it's flexible!
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


### SOVEREIGN CHILD
SOVEREIGN_CHILD_REQUIRED_FIELDS = ["QUESTION", "ANSWER", "TOPICS", "STARS"]
SOVEREIGN_CHILD_FOLDER = "data/sovereign-child/new_processed"
SUFFIXPAT_INCLUDE = "_qa-multi.md"
def mrun_corpus_sovereign_child():
    pass
#if __name__ == "__main__":
    #validate_blocks_in_folders([SOVEREIGN_CHILD_FOLDER], SOVEREIGN_CHILD_REQUIRED_FIELDS, CUSTOM_VALIDATORS, suffixpat_include=SUFFIXPAT_INCLUDE)
    #validate_iso_dates_in_filename([SOVEREIGN_CHILD_FOLDER], suffixpat_include=SUFFIXPAT_INCLUDE)
    create_qrag_vectordb([SOVEREIGN_CHILD_FOLDER], "sovereign-child-qrag", suffixpat_include=SUFFIXPAT_INCLUDE, embedding_field="QUESTION", date_from_filename=True)
def mtest_qrag_2step_sovereign_child():
    pass
# if __name__ == "__main__":
    cur_query = "Is delayed gratification good for kids?"
    cur_routes_dict = ROUTES_DICT_SOVEREIGN_CHILD_M1
    cur_vector_index_name = 'sovereign-child-qrag-7f-20250805'
    #print(cur_routes_dict)
    qrag_2step(cur_query, cur_vector_index_name, 10, cur_routes_dict)
def mrun_deepseek_sovereign_child():
    pass
#if __name__ == "__main__":
    start_time = time.time()
    #model = "o3-mini"
    model = "deepseek-reasoner"
    query = "What is a thorough response to a parent who thinks compulsory school is good?"
    routes_dict = ROUTES_DICT_SOVEREIGN_CHILD_V1
    vector_index_name = "sovereign-child-qrag-2f-20250208"
    num_chunks = 20
    qrag_routing_response = qrag_routing_call(query, vector_index_name, num_chunks, routes_dict)
    quoted_qa = qrag_routing_response["content"]["quoted_qa"]
    #print(quoted_qa)
    prompt_initial = "Answer the USER QUESTION below the following multiple sources of context:\nUse as the top priority context the QUOTED QA which have been extracted from the sources that are the primary subject for this AI tool.\nUse the BOOK TEXT as additional important context.\nUse as background context your knowledge of the parenting philosophy Taking Children Seriously, as well as the ideas of David Deutsch in his books The Fabric of Reality and The Beginning of Infinity.\n\n"
    query_context = "<USER_QUESTION>\n" + query + "\n</USER_QUESTION>\n\n"
    rag_context = "<QUOTED_QA>\n" + quoted_qa.rstrip() + "\n</QUOTED_QA>\n\n"
    large_context_file_path = "data/misc_books/Sovereign Child/2025-01-13_Book - The Sovereign Child by Dr Aaron Stupple_trimmed.md"
    #large_context_file_path = "data/misc_books/Sovereign Child/2025-01-13_Book - The Sovereign Child by Dr Aaron Stupple_trimmed-TEST.md"
    _, book_text = read_file_flex(large_context_file_path)
    book_text = book_text.split('\n', 1)[1].lstrip()  # remove CONTENT line and any blank lines that follow that
    book_text = book_text.rstrip()
    large_context = "<BOOK_TEXT>\n" + book_text.rstrip() + "\n</BOOK_TEXT>\n\n"
    prompt_parts = {
        'prompt_initial': prompt_initial,
        'query': query,
        'query_context': query_context,
        'rag_context': rag_context,
        'large_context': large_context,
        'large_context_file_path': large_context_file_path
    }
    md_file_path = "data/misc_books/Sovereign Child/deepseek_sovereign_child_include-both.md"
    response = reasoning_prompt_to_md_multipart(prompt_parts, model=model, md_file_path=md_file_path, heading_level=1)

    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"Total execution time: {minutes}:{seconds:02d}")
def mrun_count_tokens_sovereign_child():
    pass
#if __name__ == "__main__":
    cur_file_path = "data/misc_books/Sovereign Child/2025-01-13_Book - The Sovereign Child by Dr Aaron Stupple_trimmed.md"
    text = read_complete_text(cur_file_path)
    print(count_tokens(text))
def mrun_create_html_files_for_sovereign_child_v1():
    pass
#if __name__ == "__main__":
    cur_folder_path = SOVEREIGN_CHILD_FOLDER
    #transcript_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_section-titles.md')
    #qa_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_qa-qonly.md')
    #qa_md_files_to_run = ["data/misc_books/Sovereign Child/2025-01-17_Tim Ferriss Show - Naval and Aaron Stupple on Sovereign Child_qa-qonly.md"]
    css_file_path = ""  # was "transcript-with-section-titles.css"

    # transcripts
    # for i, md_file_path in enumerate(transcript_md_files_to_run, 1):
    #     html_file_path = convert_markdown_to_html(md_file_path, heading="### transcript", css_file_path=css_file_path)
    #     h_tune_html_file(html_file_path, "", 1)
    #     clean_summaries_in_html_file(html_file_path)
    #     add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_transcript.html")

    # qa
    # for i, md_file_path in enumerate(qa_md_files_to_run, 1):
    #     html_file_path = convert_markdown_to_html(md_file_path, heading="### qa", css_file_path=css_file_path)
    #     h_tune_html_file(html_file_path, "", 1)
    #     h_tune_html_file(html_file_path, "AI Extracted Question and Answer", 3, insert=False)
    #     wrap_qa_blocks_in_details(html_file_path, "QUESTION", "ANSWER")
    #     clean_summaries_in_html_file(html_file_path)
    #     add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_qa.html")
def mrun_create_html_files_for_sovereign_child_v2():  # for _qa-multi
    pass
#if __name__ == "__main__":
    cur_folder_path = SOVEREIGN_CHILD_FOLDER
    transcript_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_vrb.md')
    qa_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include='_qa-multi.md')
    css_file_path = ""  # was "transcript-with-section-titles.css"

    # transcripts
    for i, md_file_path in enumerate(transcript_md_files_to_run, 1):
        html_file_path = convert_markdown_to_html(md_file_path, heading="### transcript", css_file_path=css_file_path)
        h_tune_html_file(html_file_path, "", 1)
        clean_summaries_in_html_file(html_file_path)
        add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_transcript.html")

    # qa
    for i, md_file_path in enumerate(qa_md_files_to_run, 1):
        html_file_path = convert_markdown_to_html(md_file_path, heading="### qa", css_file_path=css_file_path)
        h_tune_html_file(html_file_path, "", 1)
        h_tune_html_file(html_file_path, "AI Extracted Question and Answer", 3, insert=False)
        wrap_qa_blocks_in_details(html_file_path, "QUESTION", "ANSWER")
        clean_summaries_in_html_file(html_file_path)
        add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_qa.html")
def mrun_create_html_file_for_book():
    pass
#if __name__ == "__main__":
    # md_file_path = "data/misc_books/Sovereign Child/2025-01-13_Book - The Sovereign Child by Dr Aaron Stupple_section-titles.md"
    # html_file_path = convert_markdown_to_html(md_file_path, heading="CONTENT", collapse_h=4, css_file_path="", bold_first_line=False, wrap_subsections=True)
    # h_tune_html_file(html_file_path, "", 1)
    # #h_tune_html_file(html_file_path, "Book", 3, insert=False)
    # clean_summaries_in_html_file(html_file_path)
    # add_additional_html_from_template(html_file_path, "web/md_to_html_dev/additions_transcript.html")

    #html_file_path = "data/misc_books/Sovereign Child/2025-01-13_Book - The Sovereign Child by Dr Aaron Stupple_section-titles.html"
    
    # Upload to S3
    cur_bucket = "fofpublic"
    # cur_s3_path = "sources-sovereign-child/transcripts-html/"
    # upload_file_to_s3(html_file_path, bucket=cur_bucket, s3_path=cur_s3_path, prompt_overwrite=False)

    html_file_path = "data/misc_books/Sovereign Child/2025-01-13_Book - The Sovereign Child by Dr Aaron Stupple_qa-qonly.html"
    cur_s3_path = "sources-sovereign-child/qa-html/"
    upload_file_to_s3(html_file_path, bucket=cur_bucket, s3_path=cur_s3_path, prompt_overwrite=False)
def mrun_create_sovereign_child_qa_from_prepqa():
    pass
#if __name__ == "__main__":
    CUR_FILE_PATH = 'data/sovereign-child/new_to_process/2025-06-26_Infinite Loops - The Sovereign Child Liberating Kids from the Tyranny of Rules_prepqa.md'
    create_qa_file_select_speaker(CUR_FILE_PATH, 'Aaron Stupple', FCALL_PROMPT_QA_DIALOGUE_FROMANSWER)
def mrun_create_sovereign_child_multi_qa():
    pass
#if __name__ == "__main__":
    qa_file_path = "data/sovereign-child/new_to_process/2025-06-02_Walk Ins Welcome - Raising Kids To Think For Themselves_qafixed.md"
    qa_multi_file_path = create_qa_multi_file_from_qa(qa_file_path, verbose=True)

def mrun_propagate_heading4_placeholders():
    pass
#if __name__ == "__main__":
    cur_file_path = "data/misc_books/Sovereign Child/2025-01-13_Book - The Sovereign Child by Dr Aaron Stupple_qa-qonly.md"
    extract_log_text = get_heading(cur_file_path, "### extract log")
    qa_text = get_heading(cur_file_path, "### qa")
    
    if not extract_log_text or not qa_text:
        ValueError(f"No extract log text or qa text found in file: {cur_file_path}")

    questions = []
    
    # Process each line
    lines = extract_log_text.split('\n')
    for i, line in enumerate(lines):
        # Look for heading level 5 "Questions Extraction"
        if line.strip() == "##### Questions Extraction":
            # Get the next line after the heading
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('Q '):
                    # Get everything after the colon, strip whitespace
                    question_parts = next_line.split(':', 1)
                    if len(question_parts) > 1:
                        question = question_parts[1].strip()
                        questions.append(question)
    
    # Now find each question in the qa and add placeholder heading
    qa_lines = qa_text.split('\n')
    insertions = 0
    for question in questions:
        # Find the line number containing this question
        for i, line in enumerate(qa_lines):
            if line.strip().startswith('QUESTION: ' + question):
                # Add placeholder heading before the question
                qa_lines.insert(i, '#### X')
                insertions += 1
                break
    
    print(f"Added {insertions} placeholder headings")
    print(f"First 5 questions: {questions[:5]}")
    print(f"Total questions: {len(questions)}")
    set_heading(cur_file_path, '\n'.join(qa_lines), "### qa")
def get_timestamps_for_qa_from_transcript(qa_file_path, transcript_file_path, debug=True):
    """
    Adds timestamps to QA blocks by matching answers with transcript dialogue.

    :param qa_file_path: string, path to QA markdown file
    :param transcript_file_path: string, path to transcript markdown file
    :return: None, updates QA file in place
    """
    # Get all H4 headings from both files
    qa_text = get_heading(qa_file_path, "### qa")
    transcript_text = get_heading(transcript_file_path, "### transcript")
    
    qa_h4_headings = [line.strip() for line in qa_text.split('\n') if line.startswith('#### ')]
    transcript_h4_headings = [line.strip() for line in transcript_text.split('\n') if line.startswith('#### ')]
    
    # for i in range(len(qa_h4_headings)):
    #     print(f"qa: {qa_h4_headings[i]}")
    #     print(f"tr: {transcript_h4_headings[i]}")
    #     print()

    # Verify headings match
    if qa_h4_headings != transcript_h4_headings:
        raise ValueError("H4 headings in QA and transcript files do not match exactly")
    
    print(f"H4 headings match in both files. Found {len(qa_h4_headings)} sections.")
    
    # Initialize counters and lists
    match_count = 0
    mismatch_count = 0
    no_match_count = 0
    total_blocks = 0
    mismatch_blocks = []
    no_match_blocks = []
    
    # Build new QA text with sections
    new_qa_sections = []
    
    # Process each section
    for section_heading in qa_h4_headings:
        # Add section heading to new text
        new_qa_sections.append(section_heading)
        
        # Get QA blocks and transcript text for this section
        qa_blocks = get_blocks_from_file(qa_file_path, section_heading)
        section_transcript = get_heading(transcript_file_path, section_heading)
        
        section_updated_blocks = []
        
        # Process each QA block in this section
        for block in qa_blocks:
            fields = get_all_fields_dict(block)
            qa_block_id = get_field_value(block, 'QA BLOCK')
            qa_speaker = get_field_value(block, 'SPEAKER ANSWER')
            verbatim_answer = get_field_value(block, 'VERBATIM ANSWER')
            
            if not qa_speaker or not verbatim_answer:
                ValueError(f"No speaker question or verbatim answer found for block: {block}")
            
            # Extract all dialogue segments with timestamps and create list of dictionaries
            dialogue_segments = []
            timestamp = None
            
            lines = section_transcript.split('\n')
            for i in range(len(lines)-1):  # -1 to avoid index error
                line = lines[i]
                if '[' in line and ']' in line and 'http' in line:
                    # Extract timestamp and speaker
                    parts = line.split('[')
                    if len(parts) > 1:
                        transcript_speaker = parts[0].strip()
                        # Get the dialogue from the next line
                        dialogue = lines[i + 1].strip()
                        segment = {
                            'line': line,
                            'speaker': transcript_speaker,
                            'dialogue': dialogue,
                            'score': 0
                        }
                        dialogue_segments.append(segment)
                        if not timestamp:
                            timestamp = line
            
            # Calculate scores for each segment
            verbatim_answer_trimmed = ' '.join(verbatim_answer.split()[:10]).lower()
            
            def clean_text(text):
                # Remove punctuation, convert to lowercase, and normalize whitespace
                import re
                text = re.sub(r'[.,!?"]', '', text.lower())
                return ' '.join(text.split())
            
            def get_match_score(text1, text2):
                # Clean both texts
                text1 = clean_text(text1)
                text2 = clean_text(text2)
                
                # Get words from both texts
                words1 = set(text1.split())
                words2 = set(text2.split())
                
                # Calculate word overlap
                common_words = words1.intersection(words2)
                if not words1:
                    return 0
                
                # Score based on how many words match
                word_match_ratio = len(common_words) / len(words1)
                
                # Bonus for sequential words matching
                from difflib import SequenceMatcher
                sequence_ratio = SequenceMatcher(None, text1, text2).ratio()
                
                # Combine scores with more weight on word matches
                return (word_match_ratio * 0.7) + (sequence_ratio * 0.3)
            
            best_score = 0
            best_segment = None
            
            for segment in dialogue_segments:
                score = get_match_score(verbatim_answer_trimmed, segment['dialogue'])
                segment['score'] = score
                if score > best_score:
                    best_score = score
                    best_segment = segment
            
            total_blocks += 1
            
            # Now check speaker match only for the best matching segment
            match_threshold = 0.5
            should_debug = False

            if best_segment and best_score > match_threshold:  # Threshold for good match
                if best_segment['speaker'] == qa_speaker:
                    # Strip everything before the first '[' for the timestamp
                    timestamp_line = best_segment['line'][best_segment['line'].find('['):]
                    fields['TIMESTAMP'] = timestamp_line
                    match_count += 1
                else:
                    timestamp_line = best_segment['line'][best_segment['line'].find('['):]
                    fields['TIMESTAMP'] = timestamp_line
                    mismatch_count += 1
                    mismatch_blocks.append(qa_block_id)
                    should_debug = True
            else:
                timestamp_line = timestamp[timestamp.find('['):]
                fields['TIMESTAMP'] = timestamp_line
                no_match_count += 1
                no_match_blocks.append(qa_block_id)
                should_debug = True

            # Reconstruct block with new timestamp before ANSWER
            updated_block = []
            for field, content in fields.items():
                if field == 'ANSWER':
                    # Insert TIMESTAMP before ANSWER
                    updated_block.append(f"TIMESTAMP: {fields['TIMESTAMP']}")
                if field != 'TIMESTAMP':  # Skip TIMESTAMP in normal iteration
                    updated_block.append(f"{field}: {content}")
            section_updated_blocks.append('\n'.join(updated_block) + '\n')  # Add newline after each block

            if debug and should_debug:
                print("\nDebug info:")
                print(f"QA Block: '{qa_block_id}'")
                print(f"Expected speaker: '{qa_speaker}'")
                print(f"Best match speaker: '{best_segment['speaker'] if best_segment else 'None'}'")
                print(f"Verbatim answer (trimmed): '{verbatim_answer_trimmed}'")
                print("\nAll segments sorted by score:")
                sorted_segments = sorted(dialogue_segments, key=lambda x: x['score'], reverse=True)
                for segment in sorted_segments:
                    print(f"Score: {segment['score']:.3f}")
                    print(f"Speaker line: {segment['speaker']} [{segment['line'].split('[')[1]}")
                    print(f"Dialogue: {segment['dialogue'][:100]}...")
                    print()
                debug = False  # Turn off debug after first error
        
        # Add all blocks for this section
        new_qa_sections.extend(section_updated_blocks)
        new_qa_sections.append('')  # Add blank line between sections
    
    # Print statistics
    print(f"Matches found: {match_count}")
    print(f"\nSpeaker mismatches: {mismatch_count}  {mismatch_blocks}")
    print(f"\nNo matches found: {no_match_count}  {no_match_blocks}")
    print(f"\nTotal blocks processed: {total_blocks}")
    
    # Write entire QA text with all sections
    final_qa_text = '\n'.join(new_qa_sections)
    set_heading(qa_file_path, final_qa_text, "### qa")
def mrun_get_timestamps_for_qa_from_transcript():
    pass
#if __name__ == "__main__":
    qa_file_path = "data/misc_books/Sovereign Child/2025-01-17_Tim Ferriss Show - Naval and Aaron Stupple on Sovereign Child_qa-qonly.md"
    transcript_file_path = "data/misc_books/Sovereign Child/2025-01-17_Tim Ferriss Show - Naval and Aaron Stupple on Sovereign Child_section-titles.md"
    get_timestamps_for_qa_from_transcript(qa_file_path, transcript_file_path)

WEBFLOW_CMS_COLLECTION_ID_SOVCHILD_TRANSCRIPTS = "68bf0edd549d72aa1a32bf7f"
CONFIG_S3_WEBFLOW_UPLOAD_SOVCHILD_TRANSCRIPTS = {
    "folder_path": "data/sovereign-child/new_processed",
    "transcript_suffix": "_vrb",
    "qa_suffix": "_qa-multi",
    "bucket": "fofpublic",
    "s3_path": "index-sovereign-child/",
    "collection_id": WEBFLOW_CMS_COLLECTION_ID_SOVCHILD_TRANSCRIPTS,
    "cms_item_name_old": "",
    "cms_item_name_new": "",
    "metadata_field_mapping": {
        "link youtube": "youtube-url",
        "link spotify": "spotify-url"
    }
}
def mrun_process_corpus_s3_webflow_upload():
    pass
#if __name__ == "__main__":
    config = CONFIG_S3_WEBFLOW_UPLOAD_SOVCHILD_TRANSCRIPTS
    process_corpus_s3_webflow_upload(config, s3_upload=True, webflow_upload=True, s3_prompt_overwrite=False, webflow_cms_prompt_overwrite=False)


#### OLD SOVEREIGN CHILD UPLOAD FUNCTION ####
def upload_s3_and_webflow_sovereign_child(s3_upload=True, s3_prompt_overwrite=True, webflow_upload=True):
    """
    Uploads Sovereign Child files to S3 and creates corresponding Webflow CMS items.

    :param s3_upload: bool, whether to upload files to S3
    :param s3_prompt_overwrite: bool, whether to prompt before overwriting S3 files
    :param webflow_upload: bool, whether to create Webflow CMS items
    :return: None
    """
    cur_folder_path = "data/misc_books/Sovereign Child"
    transcript_suffix = "_section-titles"
    qa_suffix = "_qa-qonly"
    cur_bucket = "fofpublic"
    cur_s3_path = "sources-sovereign-child/"
    collection_id = SOVEREIGN_CHILD_ID
    cms_name = "Sovereign Child"

    # transcript_html_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=transcript_suffix+".html")
    # transcript_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=transcript_suffix+".md")
    # qa_html_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=qa_suffix+".html")
    # qa_md_files_to_run = get_files_in_folder(cur_folder_path, suffixpat_include=qa_suffix+".md")
    
    transcript_html_files_to_run = []
    transcript_md_files_to_run = []
    single_qa_md_file_to_run = "data/misc_books/Sovereign Child/2025-01-17_Tim Ferriss Show - Naval and Aaron Stupple on Sovereign Child_qa-qonly.md"
    single_qa_html_file_to_run = single_qa_md_file_to_run.replace(".md", ".html")
    qa_md_files_to_run = [single_qa_md_file_to_run]
    qa_html_files_to_run = [single_qa_html_file_to_run]

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
                _, youtube_url = read_metadata_field_from_file(file_path, "youtube link")
                _, pdf_url = read_metadata_field_from_file(file_path, "pdf link")  # not working for book
                
                file_mapping[base_name]["youtube_url"] = youtube_url
                file_mapping[base_name]["pdf_url"] = pdf_url

    # Print summary after all uploads complete
    print(colored(f"\nS3 Upload Summary:", "green"))
    print(colored(f"  Total base names processed: {len(total_base_names)}", "green"))
    print(colored(f"  Total files uploaded: {total_files}", "green"))
    
    if webflow_upload:
        # Prompt user before proceeding
        response = input("\nPress Enter to continue with Webflow CMS operations, or 'x' to abort: ").lower()
        if response == 'x':
            print("Aborting operation.")
            return

        # Validate Webflow collection once before creating items
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
            overlapping_items = [cms_name for base_name, urls in file_mapping.items()]
            
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
            cms_item = {
                "name": base_name,
                "s3-transcript-html-url": urls["transcript_html"],
                "s3-qa-html-url": urls["qa_html"],
                "s3-transcript-md-url": urls["transcript_md"],
                "s3-qa-md-url": urls["qa_md"],
                "youtube-url": urls.get("youtube_url", ""),
                "pdf-url": urls.get("pdf_url", "")
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
def mrun_upload_s3_and_webflow_sovereign_child():
    pass
#if __name__ == "__main__":
    upload_s3_and_webflow_sovereign_child(s3_upload=True, s3_prompt_overwrite=False, webflow_upload=False)



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


### ARCHIVE RELATED
CUR_FOLDER = "data/floodlamp/various/external-programs-reports"
def create_csv_originals_mapping(folder_path, orig_folder_pattern="orig", suffixpat_include=None, ignore_files=None):
    """
    Creates a CSV mapping root folder files to their original source files.
    Searches subfolders containing the orig_folder_pattern for original files.
    Matches files by base name with suffixes stripped (using remove_all_suffixes_in_str).
    Reports to terminal any original files that don't have a corresponding converted file.

    :param folder_path: string of the path to the folder containing converted files at root.
    :param orig_folder_pattern: string pattern to identify original file subfolders.
    :param suffixpat_include: string of the suffix pattern that root files must have.
    :param ignore_files: list of strings of specific file names to ignore.
    :return: string of the path to the created CSV file.
    """
    if ignore_files is None:
        ignore_files = []
    
    # Get all files in root folder (not subfolders) - first get all, then filter
    all_root_files = get_files_in_folder(folder_path, include_subfolders=False)
    
    # Separate .md files from non-.md files, excluding ignored files
    root_files = []
    non_md_files = []
    for file_path in all_root_files:
        file_name = os.path.basename(file_path)
        if file_name in ignore_files:
            continue
        if file_path.endswith('.md'):
            root_files.append(file_path)
        else:
            non_md_files.append(file_path)
    
    # Build a dictionary of root file core names (without suffixes) to their full paths
    # Key: core name (no suffixes), Value: full path
    root_file_dict = {}
    root_file_display = {}  # Keep track of display name (with suffix) for CSV
    for file_path in root_files:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # Strip all suffixes for matching purposes
        core_name = remove_all_suffixes_in_str(base_name)
        root_file_dict[core_name] = file_path
        root_file_display[core_name] = base_name
    
    # Get all subfolders that contain the orig pattern
    orig_folders = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path) and orig_folder_pattern.lower() in item.lower():
            orig_folders.append(item_path)
    
    # Build a dictionary of original file core names (without suffixes) to their full paths and extensions
    # Key: core name (no suffixes), Value: list of {path, extension, base_name}
    orig_file_dict = {}
    for orig_folder in orig_folders:
        orig_files = get_files_in_folder(orig_folder, include_subfolders=True)
        for file_path in orig_files:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            extension = os.path.splitext(file_path)[1]
            # Strip all suffixes for matching purposes
            core_name = remove_all_suffixes_in_str(base_name)
            if core_name not in orig_file_dict:
                orig_file_dict[core_name] = []
            orig_file_dict[core_name].append({'path': file_path, 'extension': extension, 'base_name': base_name})
    
    # Create CSV file path
    csv_path = os.path.join(folder_path, '_file-mapping.csv')
    
    # Track matched and unmatched originals
    matched_originals = set()
    
    # Write to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header row
        writer.writerow(['converted_file', 'original_file_type', 'original_file_path'])
        
        # Write data rows for each root file (sorted by core name)
        for core_name in sorted(root_file_dict.keys()):
            root_path = root_file_dict[core_name]
            rel_root_path = os.path.relpath(root_path, folder_path)
            
            if core_name in orig_file_dict:
                # Found matching original(s)
                orig_info = orig_file_dict[core_name]
                matched_originals.add(core_name)
                if len(orig_info) == 1:
                    writer.writerow([rel_root_path, orig_info[0]['extension'], orig_info[0]['path']])
                else:
                    # Multiple originals found
                    extensions = ', '.join([o['extension'] for o in orig_info])
                    paths = ', '.join([o['path'] for o in orig_info])
                    writer.writerow([rel_root_path, f"MULTI: {extensions}", paths])
            else:
                # No original found
                writer.writerow([rel_root_path, 'no original file found', ''])
    
    # Report root files that are not .md
    if non_md_files:
        print("\n=== ROOT FILES THAT ARE NOT .md ===")
        for file_path in sorted(non_md_files):
            rel_path = os.path.relpath(file_path, folder_path)
            print(f"  {rel_path}")
        print(f"\nTotal: {len(non_md_files)} root file(s) that are not .md")
    
    # Report extra originals without converted files
    unmatched_originals = set(orig_file_dict.keys()) - matched_originals
    if unmatched_originals:
        print("\n=== ORIGINALS WITHOUT CONVERTED FILES ===")
        for core_name in sorted(unmatched_originals):
            for orig_info in orig_file_dict[core_name]:
                print(f"  {orig_info['path']}")
        print(f"\nTotal: {len(unmatched_originals)} original file(s) without converted markdown versions")
    else:
        print("\nAll original files have corresponding converted files.")
    
    print(f"\nCSV created: {csv_path}")
    print(f"Root files mapped: {len(root_file_dict)}")
    print(f"Root files that are not .md: {len(non_md_files)}")
    print(f"Matching original files found: {len(matched_originals)}")
    
    return csv_path
def mrun_create_csv_originals_mapping():
    pass
#if __name__ == "__main__":
    folder = "data/floodlamp/guides"
    create_csv_originals_mapping(folder, orig_folder_pattern="orig", suffixpat_include=".md", ignore_files=["_file-mapping.csv"])
def report_md_coverage(folder_path, include_subfolders=False):
    """
    Reports statistics about markdown file coverage in a folder.
    Prints total files, total .md files, and lists files without corresponding .md files.

    :param folder_path: string of the path to the folder to analyze.
    :param include_subfolders: boolean indicating whether to include files from subfolders.
    :return result: none, prints the report to stdout.
    """
    # Get all files in the folder
    all_files = get_files_in_folder(folder_path, include_subfolders=include_subfolders)
    
    # Separate .md files from non-.md files
    md_files = []
    non_md_files = []
    for file_path in all_files:
        if file_path.lower().endswith('.md'):
            md_files.append(file_path)
        else:
            non_md_files.append(file_path)
    
    # Build a set of base names (without extension) for .md files
    md_base_names = set()
    for file_path in md_files:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        md_base_names.add(base_name)
    
    # Find non-.md files that don't have a corresponding .md file
    files_without_md = []
    for file_path in non_md_files:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if base_name not in md_base_names:
            files_without_md.append(os.path.basename(file_path))
    
    # Sort alphabetically
    files_without_md.sort()
    
    # Print aggregate stats, lining up numbers for up to 3 digits with enough space and justification
    print(f"\n=== MD COVERAGE REPORT ===")
    print(f"Folder: {folder_path}")
    print(f"Total files:                     {len(all_files):3d}")
    print(f"Total .md files:                 {len(md_files):3d}")
    print(f"Files without corresponding .md: {len(files_without_md):3d}")
    
    # List files without corresponding .md
    if files_without_md:
        print(f"\n=== FILES WITHOUT CORRESPONDING .md ===")
        for file_name in files_without_md:
            print(f"{file_name}")
def mrun_report_md_coverage():
    pass
#if __name__ == "__main__":
    folder = "data/floodlamp/guides/test-site"
    report_md_coverage(folder, include_subfolders=False)

def read_metadata_template(template_path):
    """
    Reads metadata template from a file, stopping at the first blank line.

    :param template_path: string, path to the metadata template file.
    :return template: string, the metadata template content up to the first blank line.
    """
    with open(template_path, 'r', encoding='utf-8') as file:
        lines = []
        for line in file:
            if line.strip() == '':
                break
            lines.append(line)
    return ''.join(lines)
def extract_metadata_field(text, field_name):
    """
    Extracts the value of a metadata field from text.

    :param text: string, the text containing metadata fields.
    :param field_name: string, the name of the field to extract (e.g., 'conversion').
    :return value: string, the extracted value or empty string if not found.
    """
    import re
    # Match field_name: value (everything after colon until end of line)
    pattern = rf'^{re.escape(field_name)}:\s*(.*)$'
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ''

def process_single_fixed_md_file(file_path, template_path, suffix_to_remove="_fixed"):
    """
    Processes a single markdown file: removes suffix from filename, replaces metadata with template,
    fills in metadata fields, and strips image data from the end.

    :param file_path: string, path to the markdown file to process.
    :param template_path: string, path to the metadata template file.
    :param suffix_to_remove: string, the suffix to remove from the filename (without .md extension).
    :return new_file_path: string, the path to the renamed/processed file.
    """
    # Read the metadata template
    template = read_metadata_template(template_path)
    
    # Get file info
    folder = os.path.dirname(file_path)
    old_filename = os.path.basename(file_path)
    
    # Calculate new filename by removing the suffix
    # e.g., "2025-01-01_something_fixed.md" -> "2025-01-01_something.md"
    if old_filename.endswith(suffix_to_remove + ".md"):
        new_filename = old_filename[:-len(suffix_to_remove + ".md")] + ".md"
    else:
        raise ValueError(f"File does not end with expected suffix '{suffix_to_remove}.md': {old_filename}")
    
    # Extract metadata field values from new filename
    # file_name: the new filename with .md extension
    file_name_value = new_filename
    
    # file_date: from beginning of filename (YYYY-MM-DD format, before first underscore)
    file_date_value = new_filename.split('_')[0] if '_' in new_filename else ''
    
    # title: filename without date prefix and without extension
    # Remove the date and underscore from the beginning, then remove .md extension
    name_without_ext = os.path.splitext(new_filename)[0]
    if '_' in name_without_ext:
        title_value = '_'.join(name_without_ext.split('_')[1:])
    else:
        title_value = name_without_ext
    
    # Read the original file content
    complete_text = read_complete_text(file_path)
    
    # Extract old metadata values before modifying content
    # Find the metadata section (everything before CONTENT marker)
    content_marker = 'CONTENT'
    content_start = complete_text.find(content_marker)
    if content_start == -1:
        content_marker = '## content'
        content_start = complete_text.find(content_marker)
    
    if content_start != -1:
        old_metadata_section = complete_text[:content_start]
    else:
        old_metadata_section = ''
    
    # Extract 'conversion' value from old metadata
    conversion_value = extract_metadata_field(old_metadata_section, 'conversion')
    
    # Extract 'primary file' value and get its extension for conversion_input_file_type
    primary_file_value = extract_metadata_field(old_metadata_section, 'primary file')
    if primary_file_value:
        # Get the extension without the dot (e.g., 'pdf' from 'file.pdf')
        _, ext = os.path.splitext(primary_file_value)
        conversion_input_file_type_value = ext.lstrip('.') if ext else ''
    else:
        conversion_input_file_type_value = ''
    
    # Fill in the template fields
    filled_template = template
    filled_template = filled_template.replace('file_name: ', f'file_name: {file_name_value}')
    filled_template = filled_template.replace('file_date: ', f'file_date: {file_date_value}')
    filled_template = filled_template.replace('title: ', f'title: {title_value}')
    
    # Fill in conversion from old metadata (overwrite template value)
    # First, replace any existing conversion value with just the field name, then add the value
    import re
    filled_template = re.sub(r'^conversion:.*$', f'conversion: {conversion_value}', filled_template, flags=re.MULTILINE)
    
    # Fill in conversion_input_file_type from primary file extension
    filled_template = re.sub(r'^conversion_input_file_type:.*$', f'conversion_input_file_type: {conversion_input_file_type_value}', filled_template, flags=re.MULTILINE)
    
    # Find and remove existing metadata (everything before CONTENT marker)
    if content_start != -1:
        # Keep content from CONTENT onwards (skip the marker line itself)
        content_after_marker = complete_text[content_start + len(content_marker):]
        # Strip leading newlines from content
        content_after_marker = content_after_marker.lstrip('\n')
    else:
        # No metadata found, use complete text as content
        content_after_marker = complete_text
    
    # Strip image data from the end
    # Look for [image1]: <data:image/png;base64,
    image_marker = '[image1]: <data:image/png;base64,'
    image_start = content_after_marker.find(image_marker)
    if image_start != -1:
        content_after_marker = content_after_marker[:image_start].rstrip()
    
    # Combine filled template with CONTENT marker and content, add trailing blank line
    # METADATA as first line, two blank lines before CONTENT, one blank line after CONTENT before the actual content
    new_content = 'METADATA\n' + filled_template + '\n\nCONTENT\n\n' + content_after_marker + '\n'
    
    # Write the new content to the file (still at original path)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    # Rename the file
    new_file_path = os.path.join(folder, new_filename)
    os.rename(file_path, new_file_path)
    
    return new_file_path
def process_fixed_md_files_in_folder(folder_path, template_path, suffix_pattern="_fixed.md", include_subfolders=False):
    """
    Processes all markdown files with the specified suffix in a folder.
    Removes suffix from filenames, replaces metadata with template, fills in metadata fields,
    and strips image data from the end.

    :param folder_path: string, path to the folder containing files to process.
    :param template_path: string, path to the metadata template file.
    :param suffix_pattern: string, the suffix pattern to match files (default "_fixed.md").
    :param include_subfolders: boolean, whether to include files from subfolders.
    :return results: list of tuples (old_path, new_path) for each processed file.
    """
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Extract suffix without .md for the processing function
    if suffix_pattern.endswith('.md'):
        suffix_to_remove = suffix_pattern[:-3]  # Remove .md
    else:
        suffix_to_remove = suffix_pattern
    
    results = []
    for file_path in all_files:
        try:
            new_path = process_single_fixed_md_file(file_path, template_path, suffix_to_remove)
            results.append((file_path, new_path))
            print(f"Processed: {os.path.basename(file_path)} -> {os.path.basename(new_path)}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Print summary
    print(f"\n=== PROCESSING COMPLETE ===")
    print(f"Folder: {folder_path}")
    print(f"Files processed: {len(results)}")
    
    return results
def mrun_process_fixed_md_files():
    pass
#if __name__ == "__main__":
    folder = CUR_FOLDER
    metadata_template = "data/floodlamp/metadata_template.md"
    process_fixed_md_files_in_folder(folder, metadata_template, suffix_pattern="_fixed.md", include_subfolders=False)


def update_metadata_words_tokens(folder_path, suffix_pattern=".md", include_subfolders=False, ignore_files=None):
    """
    Updates metadata with words and tokens counts from the content section of markdown files.
    Skips files without metadata/content structure or without both 'words' and 'tokens' fields in metadata.
    When include_subfolders is True, skips subfolders that start with underscore.

    :param folder_path: string, path to the folder containing markdown files.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :param ignore_files: list of strings of specific file names to ignore.
    :return results: dict with 'processed' count and 'skipped' list of (filename, reason) tuples.
    """
    if ignore_files is None:
        ignore_files = []
    
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter out ignored files and files in subfolders starting with underscore
    files_to_process = []
    for f in all_files:
        if os.path.basename(f) in ignore_files:
            continue
        # Skip files in subfolders that start with underscore
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    processed_count = 0
    skipped_files = []  # List of (filename, reason) tuples
    
    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        
        # Try to read metadata and content
        try:
            metadata, content = read_metadata_and_content(file_path)
        except ValueError:
            skipped_files.append((file_name, "no metadata/content structure"))
            continue
        
        # Parse metadata to check for words and tokens fields
        metadata_dict = _parse_metadata_from_text(metadata)
        
        if 'words' not in metadata_dict or 'tokens' not in metadata_dict:
            skipped_files.append((file_name, "metadata missing 'words' or 'tokens' field"))
            continue
        
        # Get content text only (strip the CONTENT marker)
        content_text = content
        if content_text.startswith('CONTENT'):
            content_text = content_text[len('CONTENT'):].lstrip('\n')
        elif content_text.startswith('## content'):
            content_text = content_text[len('## content'):].lstrip('\n')
        
        # Count words and tokens from content only
        _, num_words, num_tokens = count_chars_words_tokens(content_text)
        
        # Update metadata with new values
        updated_metadata = _update_metadata_field(metadata, 'words', str(num_words))
        updated_metadata = _update_metadata_field(updated_metadata, 'tokens', str(num_tokens))
        
        # Write the updated file back (direct overwrite in place)
        try:
            complete_text = updated_metadata.rstrip('\n') + '\n\n\n' + content.rstrip('\n') + '\n'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(complete_text)
            processed_count += 1
            print(f"Updated: {file_name} - words: {num_words}, tokens: {num_tokens}")
        except Exception as e:
            skipped_files.append((file_name, f"write error: {str(e)}"))
            continue
    
    # Print summary
    print(f"\n=== UPDATE METADATA COMPLETE ===")
    print(f"Folder: {folder_path}")
    print(f"Files processed: {processed_count}")
    
    if skipped_files:
        print(f"\n=== SKIPPED FILES ({len(skipped_files)}) ===")
        for file_name, reason in skipped_files:
            print(f"  {file_name}: {reason}")
    
    return {'processed': processed_count, 'skipped': skipped_files}
def _update_metadata_field(metadata, field_name, new_value):
    """
    Updates a specific field in metadata string with a new value.

    :param metadata: string, the metadata content.
    :param field_name: string, the name of the field to update.
    :param new_value: string, the new value for the field.
    :return updated_metadata: string, the metadata with the field updated.
    """
    lines = metadata.split('\n')
    updated_lines = []
    
    for line in lines:
        if ':' in line and not line.strip().startswith('#'):
            parts = line.split(':', 1)
            if len(parts) >= 1:
                current_field = parts[0].strip()
                if current_field == field_name:
                    # Preserve the original indentation/format
                    prefix = line[:len(line) - len(line.lstrip())]
                    updated_lines.append(f"{prefix}{field_name}: {new_value}")
                    continue
        updated_lines.append(line)
    
    return '\n'.join(updated_lines)
def mrun_update_metadata_words_tokens():
    pass
#if __name__ == "__main__":
    folder = CUR_FOLDER # "data/floodlamp/guides"
    update_metadata_words_tokens(folder, suffix_pattern=".md", include_subfolders=False, ignore_files=["_metadata-extract.csv", "_file-mapping.csv"])

def overwrite_metadata_field_in_folder(folder_path, metadata_field, metadata_new_value, suffix_pattern=".md", include_subfolders=False):
    """
    Overwrites a specific metadata field with a new value across all matching files in a folder.
    Reports files where the metadata field was not found.
    When include_subfolders is True, skips subfolders that start with underscore.

    :param folder_path: string, path to the folder containing markdown files.
    :param metadata_field: string, the name of the metadata field to overwrite.
    :param metadata_new_value: string, the new value to set for the metadata field.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :return results: dict with 'updated' count and 'not_found' list of filenames where field wasn't found.
    """
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter files in subfolders starting with underscore when include_subfolders is True
    files_to_process = []
    for f in all_files:
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    updated_count = 0
    field_not_found_files = []  # List of filenames where the field wasn't found
    
    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        
        # Try to read metadata and content
        try:
            metadata, content = read_metadata_and_content(file_path)
        except ValueError:
            # No metadata/content structure, skip this file
            field_not_found_files.append(file_name)
            continue
        
        # Check if the field exists in metadata
        metadata_dict = _parse_metadata_from_text(metadata)
        
        if metadata_field not in metadata_dict:
            field_not_found_files.append(file_name)
            continue
        
        # Update metadata with new value
        updated_metadata = _update_metadata_field(metadata, metadata_field, metadata_new_value)
        
        # Write the updated file back
        try:
            complete_text = updated_metadata.rstrip('\n') + '\n\n\n' + content.rstrip('\n') + '\n'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(complete_text)
            updated_count += 1
            print(f"Updated: {file_name} - {metadata_field}: {metadata_new_value}")
        except Exception as e:
            print(f"Error writing {file_name}: {e}")
            continue
    
    # Print summary
    print(f"\n=== OVERWRITE METADATA FIELD COMPLETE ===")
    print(f"Folder: {folder_path}")
    print(f"Field: {metadata_field}")
    print(f"New value: {metadata_new_value}")
    print(f"Files updated: {updated_count}")
    
    if field_not_found_files:
        print(f"\n=== FILES WITHOUT '{metadata_field}' FIELD ({len(field_not_found_files)}) ===")
        for file_name in sorted(field_not_found_files):
            print(f"  {file_name}")
    
    return {'updated': updated_count, 'not_found': field_not_found_files}
def mrun_overwrite_metadata_field_in_folder():
    pass
#if __name__ == "__main__":
    folder = "data/floodlamp/regulatory/ldts"
    overwrite_metadata_field_in_folder(folder, "subcategory", "ldts", suffix_pattern=".md", include_subfolders=False)

def replace_string_in_filename_title(folder_path, find_string, replace_string, suffix_pattern=".md", include_subfolders=False, replace_title=True, strip_leading_date_from_title=True):
    """
    Replaces a specific string in file_name and title metadata fields across all matching files.
    Case-sensitive replacement. Optionally strips leading date (YYYY-MM-DD_) from title.
    Also renames the actual file to match the new file_name.
    When include_subfolders is True, skips subfolders that start with underscore.

    :param folder_path: string, path to the folder containing markdown files.
    :param find_string: string, the string to find (case-sensitive).
    :param replace_string: string, the string to replace with.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :param replace_title: boolean, whether to apply replacement to the title field (default True).
    :param strip_leading_date_from_title: boolean, whether to strip YYYY-MM-DD_ prefix from title (default True).
    :return results: dict with 'updated' count and 'no_match' list of filenames where find_string wasn't found.
    """
    import re
    
    # Regex pattern for leading date: YYYY-MM-DD_
    leading_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter files in subfolders starting with underscore when include_subfolders is True
    files_to_process = []
    for f in all_files:
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    updated_count = 0
    no_match_files = []  # List of filenames where find_string wasn't found
    
    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        
        # Try to read metadata and content
        try:
            metadata, content = read_metadata_and_content(file_path)
        except ValueError:
            # No metadata/content structure, skip this file
            no_match_files.append(file_name)
            continue
        
        # Parse metadata to get current values
        metadata_dict = _parse_metadata_from_text(metadata)
        
        # Get current file_name and title from metadata
        current_file_name = metadata_dict.get('file_name', '')
        current_title = metadata_dict.get('title', '')
        
        # Check if find_string exists in file_name or title
        found_in_file_name = find_string in current_file_name
        found_in_title = find_string in current_title if replace_title else False
        
        if not found_in_file_name and not found_in_title:
            no_match_files.append(file_name)
            continue
        
        # Perform replacements
        new_file_name = current_file_name.replace(find_string, replace_string) if found_in_file_name else current_file_name
        
        if replace_title:
            new_title = current_title.replace(find_string, replace_string)
        else:
            new_title = current_title
        
        # Strip leading date from title if requested
        if strip_leading_date_from_title:
            new_title = leading_date_pattern.sub('', new_title)
        
        # Update metadata fields
        updated_metadata = _update_metadata_field(metadata, 'file_name', new_file_name)
        updated_metadata = _update_metadata_field(updated_metadata, 'title', new_title)
        
        # Write the updated file back
        try:
            complete_text = updated_metadata.rstrip('\n') + '\n\n\n' + content.rstrip('\n') + '\n'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(complete_text)
            
            # Rename the actual file if file_name changed
            if new_file_name != current_file_name and new_file_name:
                new_file_path = os.path.join(file_dir, new_file_name)
                os.rename(file_path, new_file_path)
                # print(f"Updated & Renamed: {file_name} -> {new_file_name}")
                # print(f"  title: {new_title}")
            # else:
                # print(f"Updated: {file_name}")
                # print(f"  file_name: {new_file_name}")
                # print(f"  title: {new_title}")
            
            updated_count += 1
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue
    
    # Print summary
    print(f"\n=== REPLACE STRING IN FILENAME/TITLE COMPLETE ===")
    print(f"Folder: {folder_path}")
    print(f"Find: '{find_string}' -> Replace: '{replace_string}'")
    print(f"Replace in title: {replace_title}")
    print(f"Strip leading date from title: {strip_leading_date_from_title}")
    print(f"Files updated: {updated_count}")
    
    if no_match_files:
        print(f"\n=== FILES WITHOUT '{find_string}' ({len(no_match_files)}) ===")
        for fname in sorted(no_match_files):
            print(f"  {fname}")
    
    return {'updated': updated_count, 'no_match': no_match_files}
def mrun_replace_string_in_filename_title():
    pass
#if __name__ == "__main__":
    folder = "data/floodlamp/regulatory/fda-policy"
    replace_string_in_filename_title(folder, "WEBCOPY", "FDA Website", suffix_pattern=".md", include_subfolders=False, replace_title=True, strip_leading_date_from_title=True)


# GitHub URL constants - change these if the repo changes
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/FocusOnFoundationsNonprofit/floodlamp-archive-wip/main/"
GITHUB_BLOB_BASE_URL = "https://github.com/FocusOnFoundationsNonprofit/floodlamp-archive-wip/blob/main/"
def add_and_validate_github_urls(folder_path, suffix_pattern=".md", include_subfolders=False, ignore_files=None, dry_run=False, prompt_to_fix=True):
    """
    Adds and validates format of GitHub URLs in markdown file metadata.
    For xfile_github_download_url and pdf_github_url fields:
    - If value is "NA", skip (don't validate or add)
    - If value is empty, construct and add it based on category/subcategory/filename
    - If value is present, validate it matches the expected pattern
    When include_subfolders is True, skips subfolders that start with underscore.

    :param folder_path: string, path to the folder containing markdown files.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :param ignore_files: list of strings of specific file names to ignore.
    :param dry_run: boolean, if True, don't write changes, just report what would be done.
    :param prompt_to_fix: boolean, if True and not dry_run, prompt to fix URL mismatches.
    :return results: dict with 'added', 'validated', 'errors', 'fixed', 'skipped' counts and details.
    """
    if ignore_files is None:
        ignore_files = []
    
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter out ignored files and files in subfolders starting with underscore
    files_to_process = []
    for f in all_files:
        if os.path.basename(f) in ignore_files:
            continue
        # Skip files in subfolders that start with underscore
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    # Results tracking
    results = {
        'added': [],        # List of (filename, field, url) tuples
        'validated': [],    # List of (filename, field) tuples
        'errors': [],       # List of (filename, field, expected, actual) tuples
        'fixed': [],        # List of (filename, field, new_url) tuples - mismatches that were corrected
        'skipped': [],      # List of (filename, reason) tuples
        'files_modified': 0
    }
    
    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        
        # Read the file content
        try:
            complete_text = read_complete_text(file_path)
        except Exception as e:
            results['skipped'].append((file_name, f"read error: {str(e)}"))
            continue
        
        # Parse metadata
        metadata_dict = _parse_metadata_from_text(complete_text)
        
        # Check for required fields to construct URLs
        required_fields = ['file_name', 'category', 'xfile_type']
        missing = [f for f in required_fields if f not in metadata_dict]
        if missing:
            results['skipped'].append((file_name, f"missing required fields: {', '.join(missing)}"))
            continue
        
        # Get metadata values
        md_file_name = metadata_dict.get('file_name', '')
        category = metadata_dict.get('category', '')
        subcategory = metadata_dict.get('subcategory', '')
        xfile_type = metadata_dict.get('xfile_type', '')
        
        # Get current URL values
        current_xfile_url = metadata_dict.get('xfile_github_download_url', '')
        current_pdf_url = metadata_dict.get('pdf_github_url', '')
        
        # Construct the base filename (without .md extension) for URL
        if md_file_name.endswith('.md'):
            base_filename = md_file_name[:-3]
        else:
            base_filename = md_file_name
        
        # URL encode the filename (spaces become %20, etc.)
        url_encoded_filename = urllib.parse.quote(base_filename, safe='')
        
        # Construct the path: category/subcategory/ or just category/ if no subcategory
        if subcategory:
            url_path = f"{category}/{subcategory}/"
        else:
            url_path = f"{category}/"
        
        # Track if we need to update this file
        file_modified = False
        updated_text = complete_text
        
        # Process xfile_github_download_url
        if 'xfile_github_download_url' in metadata_dict:
            xfile_result = _process_github_url_field(
                current_xfile_url, 
                'xfile_github_download_url',
                GITHUB_RAW_BASE_URL,
                url_path,
                url_encoded_filename,
                xfile_type,
                file_name,
                results,
                dry_run,
                prompt_to_fix
            )
            if xfile_result['action'] in ('add', 'fix'):
                updated_text = _update_metadata_field(updated_text, 'xfile_github_download_url', xfile_result['url'])
                file_modified = True
        
        # Process pdf_github_url
        if 'pdf_github_url' in metadata_dict:
            pdf_result = _process_github_url_field(
                current_pdf_url,
                'pdf_github_url', 
                GITHUB_BLOB_BASE_URL,
                url_path,
                url_encoded_filename,
                'pdf',
                file_name,
                results,
                dry_run,
                prompt_to_fix
            )
            if pdf_result['action'] in ('add', 'fix'):
                updated_text = _update_metadata_field(updated_text, 'pdf_github_url', pdf_result['url'])
                file_modified = True
        
        # Write back if modified and not dry run
        if file_modified:
            if not dry_run:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_text)
                    results['files_modified'] += 1
                except Exception as e:
                    results['errors'].append((file_name, 'write', '', f"write error: {str(e)}"))
            else:
                results['files_modified'] += 1  # Count as would-be-modified in dry run
    
    # Print summary
    _print_github_url_results(results, folder_path, dry_run)
    
    return results
def _process_github_url_field(current_value, field_name, base_url, url_path, url_encoded_filename, extension, file_name, results, dry_run=False, prompt_to_fix=True):
    """
    Processes a single GitHub URL field - validates existing or constructs new.

    :param current_value: string, the current value of the field.
    :param field_name: string, the name of the field being processed.
    :param base_url: string, the base GitHub URL (raw or blob).
    :param url_path: string, the category/subcategory path.
    :param url_encoded_filename: string, the URL-encoded filename without extension.
    :param extension: string, the file extension to append.
    :param file_name: string, the markdown file name for reporting.
    :param results: dict, the results tracking dictionary.
    :param dry_run: boolean, if True, don't prompt or make changes.
    :param prompt_to_fix: boolean, if True and not dry_run, prompt to fix mismatches.
    :return result: dict with 'action' ('skip', 'validate', 'add', 'fix', 'error') and 'url' if applicable.
    """
    # Skip if NA
    if current_value.upper() == 'NA':
        return {'action': 'skip'}
    
    # Construct the expected URL
    expected_url = f"{base_url}{url_path}{url_encoded_filename}.{extension}"
    
    # If empty, add it
    if not current_value.strip():
        results['added'].append((file_name, field_name, expected_url))
        return {'action': 'add', 'url': expected_url}
    
    # If present, validate it
    # Normalize both URLs for comparison (handle minor encoding differences)
    normalized_current = _normalize_github_url(current_value)
    normalized_expected = _normalize_github_url(expected_url)
    
    if normalized_current == normalized_expected:
        results['validated'].append((file_name, field_name))
        return {'action': 'validate'}
    else:
        # URL mismatch found
        if not dry_run and prompt_to_fix:
            # Prompt user to fix this mismatch
            print(f"\n--- URL MISMATCH ---")
            print(f"  File: {file_name}")
            print(f"  Field: {field_name}")
            print(f"  Expected: {expected_url}")
            print(f"  Actual:   {current_value}")
            response = input("  Update to expected URL? (y/n): ").strip().lower()
            if response == 'y':
                results['fixed'].append((file_name, field_name, expected_url))
                return {'action': 'fix', 'url': expected_url}
        
        # Record as error (not fixed)
        results['errors'].append((file_name, field_name, expected_url, current_value))
        return {'action': 'error'}
def _normalize_github_url(url):
    """
    Normalizes a GitHub URL for comparison by handling encoding variations.

    :param url: string, the URL to normalize.
    :return normalized: string, the normalized URL.
    """
    # Decode and re-encode to standardize encoding
    try:
        # Parse the URL
        parsed = urllib.parse.urlparse(url)
        # Decode and re-encode the path portion
        decoded_path = urllib.parse.unquote(parsed.path)
        # Re-encode with consistent rules
        encoded_path = urllib.parse.quote(decoded_path, safe='/')
        # Rebuild the URL
        normalized = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"
        return normalized.lower()  # Case-insensitive comparison
    except:
        return url.lower()
def _print_github_url_results(results, folder_path, dry_run):
    """
    Prints the results of GitHub URL processing.

    :param results: dict, the results tracking dictionary.
    :param folder_path: string, the folder path processed.
    :param dry_run: boolean, whether this was a dry run.
    """
    prefix = "[DRY RUN] " if dry_run else ""
    
    print(f"\n=== {prefix}GITHUB URL PROCESSING RESULTS ===")
    print(f"Folder: {folder_path}")
    
    # Report URLs added
    if results['added']:
        print(f"\n--- URLs ADDED ({len(results['added'])}) ---")
        for file_name, field, url in results['added']:
            print(f"  {file_name}")
            print(f"    {field}: {url}")
    
    # Report URLs fixed (mismatches that were corrected)
    if results['fixed']:
        print(f"\n--- URLs FIXED ({len(results['fixed'])}) ---")
        for file_name, field, url in results['fixed']:
            print(f"  {file_name}")
            print(f"    {field}: {url}")
    
    # Report validation successes
    if results['validated']:
        print(f"\n--- URLs VALIDATED ({len(results['validated'])}) ---")
        for file_name, field in results['validated']:
            print(f"  {file_name}: {field} ✓")
    
    # Report errors (mismatches that were NOT fixed)
    if results['errors']:
        print(f"\n--- URL MISMATCHES (not fixed) ({len(results['errors'])}) ---")
        for file_name, field, expected, actual in results['errors']:
            print(f"  {file_name}")
            print(f"    Field: {field}")
            print(f"    Expected: {expected}")
            print(f"    Actual:   {actual}")
    
    # Report skipped files
    if results['skipped']:
        print(f"\n--- FILES SKIPPED ({len(results['skipped'])}) ---")
        for file_name, reason in results['skipped']:
            print(f"  {file_name}: {reason}")
    
    # Summary
    print(f"\n--- SUMMARY ---")
    print(f"Files modified: {results['files_modified']}")
    print(f"URLs added: {len(results['added'])}")
    print(f"URLs fixed: {len(results['fixed'])}")
    print(f"URLs validated: {len(results['validated'])}")
    print(f"URL mismatches (not fixed): {len(results['errors'])}")
    print(f"Files skipped: {len(results['skipped'])}")
def mrun_add_and_validate_github_urls():
    pass
#if __name__ == "__main__":
    folder = CUR_FOLDER # "data/floodlamp/guides"
    add_and_validate_github_urls(folder, suffix_pattern=".md", include_subfolders=False, ignore_files=["_metadata-extract.csv", "_file-mapping.csv"], dry_run=False)

def check_urls_are_live(folder_path, suffix_pattern=".md", include_subfolders=False, ignore_files=None, timeout=10, verbose=True):
    """
    Checks if all URLs in the metadata of markdown files are live (not returning 404 or other errors).
    Automatically checks any metadata field whose name contains "_url".

    :param folder_path: string, path to the folder containing markdown files.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :param ignore_files: list, specific file names to ignore.
    :param timeout: integer, timeout in seconds for HTTP requests.
    :param verbose: boolean, if True, print progress during checking.
    :return results: dict, with 'live', 'dead', 'skipped', 'errors' counts and details.
    """
    import requests
    
    if ignore_files is None:
        ignore_files = []
    
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter out ignored files and files in subfolders starting with underscore
    files_to_process = []
    for f in all_files:
        if os.path.basename(f) in ignore_files:
            continue
        # Skip files in subfolders that start with underscore
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    # Results tracking
    results = {
        'live': [],         # List of (file_path, field, url) tuples
        'dead': [],         # List of (file_path, field, url, status_code, reason) tuples
        'skipped': [],      # List of (file_path, field, url, reason) tuples
        'errors': [],       # List of (file_path, reason) tuples for file-level errors
        'files_processed': 0,
        'urls_checked': 0
    }
    
    total_files = len(files_to_process)
    
    for idx, file_path in enumerate(files_to_process, 1):
        file_name = os.path.basename(file_path)
        
        if verbose:
            print(f"[{idx}/{total_files}] Checking: {file_name}")
        
        # Read the file content
        try:
            complete_text = read_complete_text(file_path)
        except Exception as e:
            results['errors'].append((file_path, f"read error: {str(e)}"))
            continue
        
        # Parse metadata
        metadata_dict = _parse_metadata_from_text(complete_text)
        
        if not metadata_dict:
            results['errors'].append((file_path, "no metadata found"))
            continue
        
        results['files_processed'] += 1
        
        # Find URL fields to check (any field with "_url" in the name)
        fields_to_check = _get_url_fields_from_metadata(metadata_dict)
        
        for field_name, url in fields_to_check:
            # Skip empty or NA values
            if url is None:
                results['skipped'].append((file_path, field_name, url, '"None"'))
                continue
            if url.strip() == '':
                results['skipped'].append((file_path, field_name, url, "empty"))
                continue
            if url.strip().upper() == 'NA':
                results['skipped'].append((file_path, field_name, url, f'"{url.strip()}"'))
                continue
            
            # Skip non-URL values
            if not _looks_like_url(url):
                results['skipped'].append((file_path, field_name, url, f'not a URL: "{url.strip()}"'))
                continue
            
            # Check if the URL is live
            check_result = _check_single_url(url, timeout)
            results['urls_checked'] += 1
            
            if check_result['is_live']:
                results['live'].append((file_path, field_name, url))
                if verbose:
                    print(f"  ✓ {field_name}: {url[:60]}...")
            else:
                results['dead'].append((file_path, field_name, url, check_result['status_code'], check_result['reason']))
                if verbose:
                    print(f"  ✗ {field_name}: {url[:60]}... ({check_result['reason']})")
    
    # Print summary
    _print_url_check_results(results, folder_path)
    
    return results
def _get_url_fields_from_metadata(metadata_dict):
    """
    Extracts URL fields from metadata dictionary by checking for "_url" in field names.

    :param metadata_dict: dict, the parsed metadata dictionary.
    :return fields: list, of (field_name, value) tuples for URL fields.
    """
    fields = []
    
    for field_name, value in metadata_dict.items():
        # Check if field name contains "_url"
        if '_url' in field_name.lower():
            fields.append((field_name, value))
    
    return fields
def _looks_like_url(value):
    """
    Checks if a value looks like a URL.

    :param value: string, the value to check.
    :return is_url: boolean, True if the value looks like a URL.
    """
    if not value or not isinstance(value, str):
        return False
    
    value = value.strip()
    return value.startswith('http://') or value.startswith('https://')
def _check_single_url(url, timeout=10):
    """
    Checks if a single URL is live by making an HTTP HEAD request.

    :param url: string, the URL to check.
    :param timeout: integer, timeout in seconds for the request.
    :return result: dict, with 'is_live' boolean, 'status_code' integer, and 'reason' string.
    """
    import requests
    
    try:
        # Use HEAD request first (faster, less bandwidth)
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        
        # Some servers don't support HEAD, try GET if we get 405
        if response.status_code == 405:
            response = requests.get(url, timeout=timeout, allow_redirects=True, stream=True)
            response.close()
        
        # Consider 2xx and 3xx as live
        if response.status_code < 400:
            return {'is_live': True, 'status_code': response.status_code, 'reason': 'OK'}
        else:
            return {'is_live': False, 'status_code': response.status_code, 'reason': f"HTTP {response.status_code}"}
    
    except requests.exceptions.Timeout:
        return {'is_live': False, 'status_code': None, 'reason': 'Timeout'}
    except requests.exceptions.ConnectionError:
        return {'is_live': False, 'status_code': None, 'reason': 'Connection Error'}
    except requests.exceptions.TooManyRedirects:
        return {'is_live': False, 'status_code': None, 'reason': 'Too Many Redirects'}
    except requests.exceptions.SSLError:
        return {'is_live': False, 'status_code': None, 'reason': 'SSL Error'}
    except requests.exceptions.RequestException as e:
        return {'is_live': False, 'status_code': None, 'reason': f"Request Error: {str(e)[:50]}"}
    except Exception as e:
        return {'is_live': False, 'status_code': None, 'reason': f"Error: {str(e)[:50]}"}
def _path_to_file_url(file_path):
    """
    Converts a file path to a file:// URL with proper encoding for spaces.

    :param file_path: string, the file path to convert.
    :return file_url: string, the file:// URL.
    """
    # Get absolute path
    abs_path = os.path.abspath(file_path)
    # URL encode the path (spaces become %20, etc.)
    encoded_path = urllib.parse.quote(abs_path, safe='/')
    return f"file://{encoded_path}"
def _print_url_check_results(results, folder_path):
    """
    Prints the results of URL live checking.

    :param results: dict, the results tracking dictionary.
    :param folder_path: string, the folder path processed.
    """
    print(f"\n=== URL LIVE CHECK RESULTS ===")
    print(f"Folder: {folder_path}")
    
    # Report dead URLs (errors found)
    if results['dead']:
        print(f"\n--- DEAD URLs ({len(results['dead'])}) ---")
        # Group by file path
        dead_by_file = {}
        for fpath, field, url, status_code, reason in results['dead']:
            if fpath not in dead_by_file:
                dead_by_file[fpath] = []
            dead_by_file[fpath].append((field, url, reason))
        for fpath, entries in dead_by_file.items():
            file_url = _path_to_file_url(fpath)
            print(f"{file_url}")
            for field, url, reason in entries:
                print(f"  {field} ({reason})")
                print(f"    URL: {url}")
    
    # Report live URLs
    # if results['live']:
    #     print(f"\n--- LIVE URLs ({len(results['live'])}) ---")
    #     for fpath, field, url in results['live']:
    #         print(f"  {fpath}: {field} ✓")
    
    # Report skipped URLs
    if results['skipped']:
        print(f"\n--- SKIPPED URLs ({len(results['skipped'])}) ---")
        # Group by file path
        skipped_by_file = {}
        for fpath, field, url, reason in results['skipped']:
            if fpath not in skipped_by_file:
                skipped_by_file[fpath] = []
            skipped_by_file[fpath].append((field, reason))
        # ANSI color codes
        RED = '\033[91m'
        RESET = '\033[0m'
        for fpath, entries in skipped_by_file.items():
            file_url = _path_to_file_url(fpath)
            print(f"{file_url}")
            for field, reason in entries:
                # Highlight in red if not NA (needs to be fixed)
                if reason == '"NA"':
                    print(f"  {field} ({reason})")
                else:
                    print(f"  {RED}{field} ({reason}){RESET}")
    
    # Report file-level errors
    if results['errors']:
        print(f"\n--- FILE ERRORS ({len(results['errors'])}) ---")
        for fpath, reason in results['errors']:
            print(f"  {fpath}: {reason}")
    
    # Summary
    print(f"\n--- SUMMARY ---")
    print(f"Files processed: {results['files_processed']}")
    print(f"URLs checked: {results['urls_checked']}")
    print(f"Live URLs: {len(results['live'])}")
    print(f"Dead URLs: {len(results['dead'])}")
    print(f"Skipped URLs: {len(results['skipped'])}")
    print(f"File errors: {len(results['errors'])}")
    
    if results['dead']:
        print(f"\n⚠️  {len(results['dead'])} dead URL(s) found! See details above.")
    else:
        print(f"\n✓ All checked URLs are live!")
def mrun_check_urls_are_live():
    pass
#if __name__ == "__main__":
    folder = CUR_FOLDER
    check_urls_are_live(folder, suffix_pattern=".md", include_subfolders=True, ignore_files=["_metadata-extract.csv", "_file-mapping.csv"])


def extract_metadata_to_csv(folder_path, template_path, suffix_pattern=".md", include_subfolders=False, ignore_files=None, ignore_leading_underscore=True, exclude_subfolders=None):
    """
    Extracts metadata from markdown files and writes to a CSV file.
    Uses a metadata template to define expected fields and their order.
    Reports files with fields that don't match the template.
    When include_subfolders is True, skips subfolders that start with underscore.

    :param folder_path: string, path to the folder containing markdown files.
    :param template_path: string, path to the metadata template file.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :param ignore_files: list of strings of specific file names to ignore.
    :param ignore_leading_underscore: boolean, whether to ignore files starting with underscore.
    :param exclude_subfolders: list of strings, subfolder names to exclude from processing.
    :return csv_path: string, the path to the created CSV file.
    """
    if ignore_files is None:
        ignore_files = []
    if exclude_subfolders is None:
        exclude_subfolders = []
    
    # Read the metadata template and extract field names in order
    template_content = read_metadata_template(template_path)
    template_fields = _parse_template_field_names(template_content)
    template_fields_set = set(template_fields)
    
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter out ignored files and files in subfolders starting with underscore
    files_to_process = []
    for f in all_files:
        file_basename = os.path.basename(f)
        if file_basename in ignore_files:
            continue
        # Skip files starting with underscore based on parameter
        if ignore_leading_underscore and file_basename.startswith('_'):
            continue
        # Skip files in subfolders that start with underscore or are in excluded subfolders
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
            # Check if any parent folder is in the exclude list
            if len(path_parts) > 1 and any(part in exclude_subfolders for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    # Collect all metadata from all files
    all_metadata = []  # List of dicts: {file_path, metadata_dict}
    
    for file_path in files_to_process:
        complete_text = read_complete_text(file_path)
        metadata_dict = _parse_metadata_from_text(complete_text)
        h1_count = _count_h1_headings_in_content(complete_text)
        
        all_metadata.append({
            'file_path': file_path,
            'metadata': metadata_dict,
            'h1_count': h1_count
        })
    
    # CSV columns: actual file name first, then template fields in order, then h1_count
    csv_columns = ['file_name_actual'] + template_fields + ['h1_count']
    
    # Track files with non-standard metadata
    files_with_nonstandard = []
    
    # Prepare rows for CSV
    csv_rows = []
    for entry in all_metadata:
        file_path = entry['file_path']
        metadata = entry['metadata']
        h1_count = entry['h1_count']
        file_name = os.path.basename(file_path)
        
        # Check for fields that don't match template
        file_fields = set(metadata.keys())
        extra_fields = file_fields - template_fields_set
        missing_fields = template_fields_set - file_fields
        
        if extra_fields or missing_fields:
            files_with_nonstandard.append({
                'file_name': file_name,
                'file_path': file_path,
                'extra_fields': extra_fields,
                'missing_fields': missing_fields
            })
        
        # Build row using template field order, plus h1_count
        row = {'file_name_actual': file_name}
        for field in template_fields:
            row[field] = metadata.get(field, '')
        row['h1_count'] = h1_count
        csv_rows.append(row)
    
    # Create CSV file path
    csv_path = os.path.join(folder_path, '_metadata-extract.csv')
    
    # Write to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    # Report files with non-standard metadata
    if files_with_nonstandard:
        print("\n=== FILES WITH NON-STANDARD METADATA ===")
        for entry in files_with_nonstandard:
            file_url = _path_to_file_url(entry['file_path'])
            print(f"\n{file_url}")
            if entry['extra_fields']:
                print(f"  Extra fields: {', '.join(sorted(entry['extra_fields']))}")
            if entry['missing_fields']:
                print(f"  Missing fields: {', '.join(sorted(entry['missing_fields']))}")
        print(f"\nTotal: {len(files_with_nonstandard)} file(s) with non-standard metadata")
    else:
        print("\nAll files have metadata matching the template.")
    
    # Print summary
    print(f"\n=== METADATA EXTRACTION COMPLETE ===")
    print(f"Folder: {folder_path}")
    print(f"Template: {template_path}")
    print(f"Files processed: {len(files_to_process)}")
    print(f"Template fields: {', '.join(template_fields)}")
    print(f"CSV created: {csv_path}")
    
    return csv_path
def _parse_template_field_names(template_content):
    """
    Parses field names from metadata template content, preserving order.

    :param template_content: string, the metadata template content.
    :return field_names: list of strings, field names in order they appear.
    """
    field_names = []
    for line in template_content.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            # Split on first colon only
            parts = line.split(':', 1)
            if len(parts) >= 1:
                field_name = parts[0].strip()
                if field_name:
                    field_names.append(field_name)
    return field_names
def _parse_metadata_from_text(text):
    """
    Parses metadata fields from markdown text between METADATA and CONTENT markers.

    :param text: string, the complete text of a markdown file.
    :return metadata_dict: dict, mapping field names to their values.
    """
    metadata_dict = {}
    
    # Find metadata section
    metadata_start = text.find('METADATA')
    if metadata_start == -1:
        return metadata_dict
    
    # Find content marker (try both formats)
    content_marker = 'CONTENT'
    content_start = text.find(content_marker, metadata_start)
    if content_start == -1:
        content_marker = '## content'
        content_start = text.find(content_marker, metadata_start)
    
    if content_start == -1:
        # No content marker, use entire text after METADATA
        metadata_section = text[metadata_start + len('METADATA'):]
    else:
        metadata_section = text[metadata_start + len('METADATA'):content_start]
    
    # Parse each line for field: value format
    for line in metadata_section.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            # Split on first colon only
            parts = line.split(':', 1)
            if len(parts) == 2:
                field_name = parts[0].strip()
                field_value = parts[1].strip()
                # Skip empty field names
                if field_name:
                    metadata_dict[field_name] = field_value
    
    return metadata_dict
def _count_h1_headings_in_content(text):
    """
    Counts the number of H1 headings (lines starting with '# ') in the content section of markdown text.

    :param text: string, the complete text of a markdown file.
    :return h1_count: int, the number of H1 headings in the content section.
    """
    # Find content marker (try both formats)
    content_marker = 'CONTENT'
    content_start = text.find(content_marker)
    if content_start == -1:
        content_marker = '## content'
        content_start = text.find(content_marker)
    
    if content_start == -1:
        # No content marker found, return 0
        return 0
    
    # Get the content section (after the CONTENT marker)
    content_section = text[content_start + len(content_marker):]
    
    # Count H1 headings (lines that start with '# ' after stripping leading whitespace)
    h1_count = 0
    for line in content_section.split('\n'):
        stripped = line.strip()
        # Check for exactly H1: starts with '# ' and not '##'
        if stripped.startswith('# ') and not stripped.startswith('## '):
            h1_count += 1
    
    return h1_count
def mrun_extract_metadata_to_csv():
    folder = "data/floodlamp/guides"
    metadata_template = "data/floodlamp/metadata_template.md"
    extract_metadata_to_csv(folder, metadata_template, suffix_pattern=".md", include_subfolders=True, ignore_files=["_metadata-extract.csv", "_file-mapping.csv"], exclude_subfolders=["fda-townhalls"])
if __name__ == "__main__":
    folder = "data/floodlamp/regulatory"
    metadata_template = "data/floodlamp/metadata_template.md"
    exclude_subfolders = ["fda-townhalls"]
    extract_metadata_to_csv(folder, metadata_template, suffix_pattern=".md", include_subfolders=True, ignore_files=["_metadata-extract.csv", "_file-mapping.csv"], exclude_subfolders=exclude_subfolders)

def process_single_md_file(file_path, do_update_words_tokens=True, do_add_github_urls=True, do_check_urls_live=True, timeout=10):
    """
    Processes a single markdown file: updates words/tokens metadata, adds GitHub URLs, and checks if URLs are live.
    Wraps the existing folder-based functions by using the filename as the suffix pattern.

    :param file_path: string, path to the markdown file to process.
    :param do_update_words_tokens: boolean, whether to update words and tokens in metadata.
    :param do_add_github_urls: boolean, whether to add GitHub URLs to metadata.
    :param do_check_urls_live: boolean, whether to check if URLs are live.
    :param timeout: integer, timeout in seconds for HTTP requests when checking URLs.
    :return results: dict with processing results from each operation.
    """
    # Extract folder path and filename from the file path
    folder_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    
    results = {
        'file': file_name,
        'words_tokens': None,
        'github_urls': None,
        'url_checks': None
    }
    
    print(f"\n=== PROCESSING SINGLE FILE: {file_name} ===")
    print(f"Folder: {folder_path}")
    
    # Step 1: Update words and tokens
    if do_update_words_tokens:
        print(f"\n--- Step 1: Update Words/Tokens ---")
        results['words_tokens'] = update_metadata_words_tokens(folder_path, suffix_pattern=file_name)
    
    # Step 2: Add GitHub URLs (using prompt_to_fix=False to avoid interactive prompts)
    if do_add_github_urls:
        print(f"\n--- Step 2: Add GitHub URLs ---")
        results['github_urls'] = add_and_validate_github_urls(folder_path, suffix_pattern=file_name, prompt_to_fix=False)
    
    # Step 3: Check if URLs are live
    if do_check_urls_live:
        print(f"\n--- Step 3: Check URLs Are Live ---")
        results['url_checks'] = check_urls_are_live(folder_path, suffix_pattern=file_name, timeout=timeout)
    
    print(f"\n=== SINGLE FILE PROCESSING COMPLETE ===")
    
    return results
def mrun_process_single_md_file():
    pass
#if __name__ == "__main__":
    file_path = "data/floodlamp/regulatory/fl-fda-subs/2021-10-04_FloodLAMP Email to Tim Stenzel - 4 pages.md"
    process_single_md_file(file_path, do_update_words_tokens=True, do_add_github_urls=True, do_check_urls_live=True)

def mrun_copy_these_files():
    pass
#if __name__ == "__main__":
    source_folder = "data/floodlamp/regulatory/_fda-townhalls-dev/f5_fixnames/a_done_site"
    destination_folder = "data/floodlamp/regulatory/fda-townhalls"
    copy_files_with_suffix(source_folder, destination_folder, suffixpat_include="_qa-qonly.md")

def extract_token_counts_to_csv(folder_path, suffix_pattern=".md", include_subfolders=False, ignore_files=None):
    """
    Extracts word and token counts from the content section of markdown files and writes to a CSV file.
    Uses read_metadata_and_content to separate metadata from content.
    When include_subfolders is True, skips subfolders that start with underscore.

    :param folder_path: string, path to the folder containing markdown files.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :param ignore_files: list of strings of specific file names to ignore.
    :return csv_path: string, the path to the created CSV file.
    """
    if ignore_files is None:
        ignore_files = []
    
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter out ignored files and files in subfolders starting with underscore
    files_to_process = []
    for f in all_files:
        if os.path.basename(f) in ignore_files:
            continue
        # Skip files in subfolders that start with underscore
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    # Collect token counts from all files
    csv_rows = []
    skipped_files = []
    
    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        
        # Try to read metadata and content
        try:
            metadata, content = read_metadata_and_content(file_path)
        except ValueError:
            skipped_files.append((file_name, "no metadata/content structure"))
            continue
        
        # Get content text only (strip the CONTENT marker)
        content_text = content
        if content_text.startswith('CONTENT'):
            content_text = content_text[len('CONTENT'):].lstrip('\n')
        elif content_text.startswith('## content'):
            content_text = content_text[len('## content'):].lstrip('\n')
        
        # Count words and tokens from content only
        _, num_words, num_tokens = count_chars_words_tokens(content_text)
        
        csv_rows.append({
            'file_name': file_name,
            'tokens': num_tokens,
            'words': num_words
        })
    
    # Create CSV file path
    csv_path = os.path.join(folder_path, '_token-counts.csv')
    
    # Write to CSV
    csv_columns = ['file_name', 'tokens', 'words']
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    # Print summary
    print(f"\n=== TOKEN COUNTS EXTRACTION COMPLETE ===")
    print(f"Folder: {folder_path}")
    print(f"Files processed: {len(csv_rows)}")
    print(f"CSV created: {csv_path}")
    
    if skipped_files:
        print(f"\n=== SKIPPED FILES ({len(skipped_files)}) ===")
        for file_name, reason in skipped_files:
            print(f"  {file_name}: {reason}")
    
    return csv_path
def mrun_extract_token_counts_to_csv():
    pass
#if __name__ == "__main__":
    folder = "data/floodlamp/regulatory/irb"
    extract_token_counts_to_csv(folder, suffix_pattern="_section-titles.md", include_subfolders=False, ignore_files=["_token-counts.csv"])

def extract_summary_shorts_to_composite_md(folder_path, suffix_pattern=".md", include_subfolders=False, ignore_files=None, output_filename="_summary-shorts-composite.md"):
    """
    Extracts summary_short field from metadata of markdown files and creates a composite markdown file.
    Each file's summary_short is preceded by an H1 heading with the file name.
    When include_subfolders is True, skips subfolders that start with underscore.

    :param folder_path: string, path to the folder containing markdown files.
    :param suffix_pattern: string, the suffix pattern to match files (default ".md").
    :param include_subfolders: boolean, whether to include files from subfolders (skips _prefixed folders).
    :param ignore_files: list of strings of specific file names to ignore.
    :param output_filename: string, the name of the output composite markdown file.
    :return output_path: string, the path to the created composite markdown file.
    """
    if ignore_files is None:
        ignore_files = []
    
    # Get all files matching the suffix pattern
    all_files = get_files_in_folder(folder_path, suffixpat_include=suffix_pattern, include_subfolders=include_subfolders)
    
    # Filter out ignored files and files in subfolders starting with underscore
    files_to_process = []
    for f in all_files:
        if os.path.basename(f) in ignore_files:
            continue
        # Skip files in subfolders that start with underscore
        if include_subfolders:
            rel_path = os.path.relpath(f, folder_path)
            path_parts = rel_path.split(os.sep)
            # Check if any parent folder (not the file itself) starts with underscore
            if len(path_parts) > 1 and any(part.startswith('_') for part in path_parts[:-1]):
                continue
        files_to_process.append(f)
    
    # Sort files alphabetically by filename
    files_to_process.sort(key=lambda x: os.path.basename(x).lower())
    
    # Collect summary shorts from all files
    entries = []  # List of (file_name, summary_short) tuples
    skipped_files = []  # List of (file_name, reason) tuples
    
    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        
        # Read the file content
        try:
            complete_text = read_complete_text(file_path)
        except Exception as e:
            skipped_files.append((file_name, f"read error: {str(e)}"))
            continue
        
        # Parse metadata
        metadata_dict = _parse_metadata_from_text(complete_text)
        
        if not metadata_dict:
            skipped_files.append((file_name, "no metadata found"))
            continue
        
        # Check for summary_short field
        if 'summary_short' not in metadata_dict:
            skipped_files.append((file_name, "no summary_short field in metadata"))
            continue
        
        summary_short = metadata_dict['summary_short']
        
        # Skip if summary_short is empty or NA
        if not summary_short.strip():
            skipped_files.append((file_name, "summary_short is empty"))
            continue
        if summary_short.strip().upper() == 'NA':
            skipped_files.append((file_name, "summary_short is NA"))
            continue
        
        entries.append((file_name, summary_short))
    
    # Build the composite markdown content
    composite_lines = []
    for file_name, summary_short in entries:
        # Add H1 heading with file name (without .md extension for cleaner display)
        display_name = file_name[:-3] if file_name.endswith('.md') else file_name
        composite_lines.append(f"# {display_name}")
        composite_lines.append(summary_short)
        composite_lines.append("")
        composite_lines.append("")  # Extra blank line between entries
    
    # Create output file path
    output_path = os.path.join(folder_path, output_filename)
    
    # Write the composite markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(composite_lines).rstrip('\n') + '\n')
    
    # Print summary
    print(f"\n=== SUMMARY SHORTS COMPOSITE EXTRACTION COMPLETE ===")
    print(f"Folder: {folder_path}")
    print(f"Files processed: {len(entries)}")
    print(f"Composite markdown created: {output_path}")
    
    if skipped_files:
        print(f"\n=== SKIPPED FILES ({len(skipped_files)}) ===")
        for file_name, reason in skipped_files:
            print(f"  {file_name}: {reason}")
    
    return output_path
def mrun_extract_summary_shorts_to_composite_md():
    pass
#if __name__ == "__main__":
    folder = CUR_FOLDER
    extract_summary_shorts_to_composite_md(folder, suffix_pattern=".md", include_subfolders=False, ignore_files=["_summary-shorts-composite.md", "_metadata-extract.csv", "_file-mapping.csv"])

def count_files_by_category(root_folder="data/floodlamp", categories_file="data/floodlamp/categories.md", ignore_leading_underscore=True):
    """
    Scans the folder structure and counts .md files and unique base filenames per subcategory.
    Outputs results in tab-separated format for pasting into a spreadsheet.
    Reports mismatched folder names.

    :param root_folder: string, path to the root floodlamp folder.
    :param categories_file: string, path to the categories.md file defining expected structure.
    :param ignore_leading_underscore: boolean, whether to ignore folders and files starting with underscore.
    :return results: dict with counts per category and subcategory.
    """
    # Parse categories.md to get expected structure
    categories = {}  # {category_name: [subcategory1, subcategory2, ...]}
    current_category = None
    
    with open(categories_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('## '):
                current_category = line[3:].strip()
                categories[current_category] = []
            elif line and current_category:
                categories[current_category].append(line)
    
    # Collect all expected subcategory folder names
    expected_subcategories = set()
    for cat, subcats in categories.items():
        for subcat in subcats:
            expected_subcategories.add(subcat)
    
    # Also collect category names (top-level folders we expect)
    expected_categories = set(categories.keys())
    
    # Track mismatched folders
    mismatched_folders = []
    
    # Results storage: {category: {subcategory: {'md_count': n, 'unique_basenames': n}}}
    results = {}
    
    # Scan the actual folder structure
    if os.path.exists(root_folder):
        for item in os.listdir(root_folder):
            # Skip dot-prefixed items always, underscore-prefixed based on parameter
            if item.startswith('.'):
                continue
            if ignore_leading_underscore and item.startswith('_'):
                continue
            
            item_path = os.path.join(root_folder, item)
            if not os.path.isdir(item_path):
                continue
            
            # This should be a category folder
            category_name = item
            if category_name not in expected_categories:
                mismatched_folders.append(f"Category: {category_name}")
                continue
            
            results[category_name] = {}
            
            # Scan subcategories within this category
            for subitem in os.listdir(item_path):
                # Skip dot-prefixed items always, underscore-prefixed based on parameter
                if subitem.startswith('.'):
                    continue
                if ignore_leading_underscore and subitem.startswith('_'):
                    continue
                
                subitem_path = os.path.join(item_path, subitem)
                if not os.path.isdir(subitem_path):
                    continue
                
                subcategory_name = subitem
                
                # Check if subcategory is expected for this category
                if subcategory_name not in categories.get(category_name, []):
                    mismatched_folders.append(f"Subcategory: {category_name}/{subcategory_name}")
                    continue
                
                # Count .md files and unique base filenames in this subcategory
                md_count = 0
                base_names = set()
                
                for root, dirs, files in os.walk(subitem_path):
                    # Filter out underscore-prefixed subdirectories based on parameter
                    if ignore_leading_underscore:
                        dirs[:] = [d for d in dirs if not d.startswith('_')]
                    
                    for file in files:
                        # Skip underscore-prefixed files based on parameter
                        if ignore_leading_underscore and file.startswith('_'):
                            continue
                        if file.endswith('.md'):
                            md_count += 1
                            # Extract base name (remove extension and any suffix patterns)
                            base_name = os.path.splitext(file)[0]
                            # Remove common suffixes like _qa, _transcript, _section-titles, etc.
                            # to get the true unique base name
                            base_names.add(base_name)
                
                results[category_name][subcategory_name] = {
                    'md_count': md_count,
                    'unique_basenames': len(base_names)
                }
    
    # Calculate totals for each category first (needed for printing totals at top)
    category_totals = {}
    for category_name in categories.keys():
        cat_md_total = 0
        cat_basename_total = 0
        for subcategory_name in categories[category_name]:
            if category_name in results and subcategory_name in results[category_name]:
                cat_md_total += results[category_name][subcategory_name]['md_count']
                cat_basename_total += results[category_name][subcategory_name]['unique_basenames']
        category_totals[category_name] = {'md_count': cat_md_total, 'unique_basenames': cat_basename_total}
    
    # Find the longest name for column alignment (include category names with "## " prefix)
    max_name_len = 0
    for category_name in categories.keys():
        max_name_len = max(max_name_len, len(f"## {category_name}"))
        for subcategory_name in categories[category_name]:
            max_name_len = max(max_name_len, len(subcategory_name))
    
    # Add some padding
    col1_width = max_name_len + 2
    col2_width = 10  # "MD Files" header width
    col3_width = 16  # "Unique Basenames" header width
    
    # Print output in fixed-width format for terminal
    print("\n=== FILE COUNTS BY CATEGORY ===\n")
    print(f"{'Name':<{col1_width}}  {'MD Files':>{col2_width}}  {'Unique Basenames':>{col3_width}}")
    print("-" * (col1_width + col2_width + col3_width + 4))
    
    # Build CSV rows
    csv_rows = []
    
    for category_name in categories.keys():
        # Print category total at the TOP with ## prefix
        cat_totals = category_totals[category_name]
        print(f"{'## ' + category_name:<{col1_width}}  {cat_totals['md_count']:>{col2_width}}  {cat_totals['unique_basenames']:>{col3_width}}")
        csv_rows.append({'name': f"## {category_name}", 'md_files': cat_totals['md_count'], 'unique_basenames': cat_totals['unique_basenames']})
        
        # Print subcategories
        for subcategory_name in categories[category_name]:
            if category_name in results and subcategory_name in results[category_name]:
                md_count = results[category_name][subcategory_name]['md_count']
                unique_basenames = results[category_name][subcategory_name]['unique_basenames']
            else:
                # Folder doesn't exist, report zeros
                md_count = 0
                unique_basenames = 0
            
            print(f"{subcategory_name:<{col1_width}}  {md_count:>{col2_width}}  {unique_basenames:>{col3_width}}")
            csv_rows.append({'name': subcategory_name, 'md_files': md_count, 'unique_basenames': unique_basenames})
        
        print()  # Blank line between categories
    
    # Write CSV file
    csv_path = os.path.join(root_folder, '_file-counts.csv')
    csv_columns = ['name', 'md_files', 'unique_basenames']
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    print(f"CSV file created: {csv_path}")
    
    # Print mismatched folders at the end
    if mismatched_folders:
        print("\n=== MISMATCHED FOLDERS (not in categories.md) ===")
        for folder in mismatched_folders:
            print(f"  {folder}")
    
    return results
def mrun_count_files_by_category():
    pass
#if __name__ == "__main__":
    count_files_by_category()


# ===== END OF FILE primary/corpuses.py =====
