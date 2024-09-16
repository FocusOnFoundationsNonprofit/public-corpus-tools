
import os
import re
import logging
import pypandoc

from llama_parse import LlamaParse  # pip install llama-index llama-parse
from llama_index.core import SummaryIndex
from llama_index.readers.google import GoogleDocsReader  # pip install llama-index llama-index-readers-google
# from IPython.display import Markdown, display

from config import LLAMA_CLOUD_API_KEY


### LLAMAINDEX
def convert_llamaparse_pdf_to_md(file_path):
    suffix_append = "_llamaparse"
    documents = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown",verbose=True).load_data(file_path)
    print(documents[0].text[0:1000])
    md_file_path = file_path.rsplit('.', 1)[0] + suffix_append + '.md'  # Replace the file extension with .md
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(documents[0].text)
    print("Completed LlamaParse pdf to md conversion and appended suffix: " + suffix_append + " on input file_path: " + file_path)
    return md_file_path

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

