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

# These vector db wrapper functions are used manually and are not called by the rag_bots functions. (RT 6-10-2024)
# Pinecone indexes can be seen in the pinecone.io portal > go to Serverless in UL - login sends email to fofgeneral20


### VECTOR DB SUPPORT
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

# TODO review the timestamp lines
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

# don't use - manually delete in pinecone portal before overwriting
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


### VECTOR DB CREATION
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


