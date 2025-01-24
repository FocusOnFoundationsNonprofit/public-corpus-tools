# ===== START OF FILE primary/rag.py =====
# Library of functions and execution code to do RAG tasks

import os
from datetime import datetime
from pinecone import Pinecone
from termcolor import colored

from primary.vectordb import generate_embedding
from primary.llm import simple_openai_chat_completion_request
from primary.rag_prompts_routes import *


# ---API KEYS AND SECRETS---
from dotenv import load_dotenv
load_dotenv(override=True)  # Load environment variables from .env file
OPENAI_API_KEY = os.environ["OPENAI_API_KEY_LOCAL"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY_LOCAL"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
 

# ---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

DEFAULT_LLM_MODEL = 'gpt-4o'

### RETRIEVAL
def pinecone_retriever(query, vector_index_name, num_chunks, date_range=None):
    """ 
    Retrieves relevant question chunks from a Pinecone index based on the input question.

    :param query: string of the input question to search for.
    :param vector_index_name: string of the name of the Pinecone index to query.
    :param num_chunks: integer specifying the number of chunks to retrieve.
    :param date_range: optional list of two dates [start_date, end_date] in ISO format (e.g., ['2021-01-01', '2021-12-31']).
    :return: tuple containing fetched question chunks and a dictionary of retrieved IDs with their scores.
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


### VRAG
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
    
def vrag_llm_call(user_question, vector_index_name, num_chunks, vrag_preamble=VRAG_PREAMBLE_V1, llm_model=DEFAULT_LLM_MODEL, user_id='default', vrag_version="1.0"):
    """
    Initiates a chat session using vector retrieval augmented generation (VRAG) with a specified question,
    prompt template, and index name. Returns a JSON object with the results.

    :param user_question: string of the question to initiate the chat with.
    :param vector_index_name: string of the name of the pinecone index to use for retrieval.
    :param num_chunks: integer specifying the number of chunks to retrieve.
    :param vrag_preamble: string of the preamble used to format the chat prompt.
    :param llm_model: string of the language model to use.
    :param user_id: string of the user identifier.
    :param bot_version: string of the bot version.
    :return: dictionary containing the chat response and metadata.
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
 

### QRAG
def sort_chunks_by_stars(fetched_qa_chunks, retrieved_ids_scores, num_chunks):
    """
    Sorts chunks primarily by star rating and then by similarity score, returning the top `num_chunks`.
    Converts 'STARS' to integer and sets to 0 if blank.

    :param fetched_qa_chunks: dictionary of fetched question chunks from Pinecone.
    :param retrieved_ids_scores: dictionary of retrieved IDs with their similarity scores.
    :param num_chunks: integer specifying the number of chunks to return.
    :return: list of sorted chunks.
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

def sort_chunks_by_sim(fetched_qa_chunks, retrieved_ids_scores, num_chunks):
    """
    Sorts chunks primarily by similarity score and returns the top `num_chunks`.
    Converts 'STARS' to integer and sets to 0 if blank, but doesn't use it for sorting.

    :param fetched_qa_chunks: dictionary of fetched question chunks from Pinecone.
    :param retrieved_ids_scores: dictionary of retrieved IDs with their similarity scores.
    :param num_chunks: integer specifying the number of chunks to return.
    :return: list of sorted chunks.
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

def parse_chunks(chunks, simscores):
    """ 
    Parses a list of chunks and returns a list of dictionaries containing formatted chunk information.
    Maps QA block fields (CLARIFIED_QUESTION/ANSWER) to standard QUESTION/ANSWER fields.

    :param chunks: list of chunk metadata dictionaries.
    :param simscores: dictionary of similarity scores keyed by chunk id.
    :return: list of parsed chunk dictionaries.
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

def qrag_routing_call(user_question, vector_index_name, num_chunks, routes_dict, date_range=None, routes_bounds=[0.3, 0.9], 
                      llm_model=DEFAULT_LLM_MODEL, user_id='default', user_context=None, qrag_version="1.0"):
    """
    Routes a user question through a question retrieval augmented generation (QRAG) process.

    :param user_question: str, the question asked by the user.
    :param vector_index_name: str, name of the vector index to search.
    :param num_chunks: int, number of chunks to retrieve and process.
    :param routes_dict: dict, containing routing information and templates.
    :param date_range: optional list of two dates [start_date, end_date] in ISO format (e.g., ['2021-01-01', '2021-12-31']).
    :param routes_bounds: list, lower and upper similarity bounds for routing.
    :param llm_model: str, name of the language model to use.
    :param user_id: str, identifier for the user.
    :param qrag_version: str, version of the QRAG system.
    :return response: dict, containing metadata and content of the QRAG response.
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
    json_object['content']['llm_prompt'] = llm_prompt  # Optionally include the prompt

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

def qrag_2step(user_question, routes_dict, vector_index_name, num_chunks=2, verbose=True):
    """ 
    Performs a two-step question-answering process using QRAG (Question Retrieval Augmented Generation).

    :param user_question: string of the user's input question.
    :return: None
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

# ===== END OF FILE primary/rag.py =====