# ===== START OF FILE primary/rag_mtests.py =====
# Library for manual testing of rag functions

from primary.fileops import *
from primary.llm import *
from primary.rag import *
from rag_prompts_routes import *

if True:
    pass
# if __name__ == "__main__":    
    cur_file_path = ""

# CUR_VECTOR_INDEX_NAME = 'pv-evac-qrag-2f-20241024'
# CUR_ROUTES_DICT = ROUTES_DICT_PV_EVAC_V1
# CUR_QUERY = "What is the PSVD school evacuation plan?"
# CUR_NUM_CHUNKS = 5
# CUR_JSON_PATH = 'tests/test_manual_files/rag/qrag_routing_pv_evac_q1.json'

CUR_VECTOR_INDEX_NAME = 'fda-townhalls-qrag-4f-20250114'
CUR_ROUTES_DICT = ROUTES_DICT_FDA_TOWNHALLS_V1
CUR_QUERY = "What is the FDA's response to the COVID-19 pandemic?"
CUR_NUM_CHUNKS = 5


### RETRIEVAL
def mtest_pinecone_retriever():
    pass
if __name__ == "__main__":
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(CUR_QUERY, CUR_VECTOR_INDEX_NAME, num_chunks=CUR_NUM_CHUNKS)
    # print("Fetched chunks:")
    # print(fetched_chunks)
    print("Retrieved IDs and scores:")
    for id, score in retrieved_ids_scores.items():
        print(f"{id}: {score}")
    
    print(colored("Retrieving chunks with date range", "yellow"))
    date_range = ["2020-03-01", "2020-03-29"]
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(CUR_QUERY, CUR_VECTOR_INDEX_NAME, num_chunks=CUR_NUM_CHUNKS, date_range=date_range)
    print(f"Retrieved IDs and scores with date range of {date_range}:")
    for id, score in retrieved_ids_scores.items():
        print(f"{id}: {score}")
    

### VRAG
def mtest_vrag_llm_call():
    pass
#if __name__ == "__main__":
    cur_user_question1 = "What is the meaning of life?"
    cur_user_question2 = "What is the Mathematician's Misconception?"
    cur_json_object = vrag_llm_call(cur_user_question1, 'dd-transcripts-vrag-80f-20240727', 5)
    print_vrag_display_text(cur_json_object, show_prompt=False)

### QRAG
def mtest_sort_chunks_by_stars():
    pass
#if __name__ == "__main__":
    cur_query = "What is the meaning of life?"
    cur_num_chunks = 10  # Number of chunks to retrieve and sort
    fetched_qa_chunks, retrieved_ids_scores = pinecone_retriever(cur_query, CUR_VECTOR_INDEX_NAME, num_chunks=cur_num_chunks)
    sorted_chunks = sort_chunks_by_stars(fetched_qa_chunks, retrieved_ids_scores, num_chunks=cur_num_chunks)
    print("Sorted Chunks by Stars:")
    for idx, chunk in enumerate(sorted_chunks):
        print(f"Chunk {idx+1}:")
        print(f"ID: {chunk['id']}")
        print(f"Stars: {chunk['STARS']}")
        print(f"Similarity Score: {chunk['sim_score']}")
        print(f"Question: {chunk.get('QUESTION', '')}")
        print(f"Answer: {chunk.get('ANSWER', '')}")
        print("-" * 40)
def mtest_sort_chunks_by_sim():
    pass
#if __name__ == "__main__":
    cur_query = "What is the meaning of life?"
    cur_num_chunks = 10  # Number of chunks to retrieve and sort
    fetched_qa_chunks, retrieved_ids_scores = pinecone_retriever(cur_query, CUR_VECTOR_INDEX_NAME, num_chunks=cur_num_chunks)
    sorted_chunks = sort_chunks_by_sim(fetched_qa_chunks, retrieved_ids_scores, num_chunks=cur_num_chunks)
    print("Sorted Chunks by Similarity:")
    for idx, chunk in enumerate(sorted_chunks):
        print(f"Chunk {idx+1}:")
        print(f"ID: {chunk['id']}")
        print(f"Stars: {chunk['STARS']}")
        print(f"Similarity Score: {chunk['sim_score']}")
        print(f"Question: {chunk.get('QUESTION', '')}")
        print(f"Answer: {chunk.get('ANSWER', '')}")
        print("-" * 40)
def mtest_parse_chunks():
    pass
#if __name__ == "__main__":
    cur_query = "What is the meaning of life?"
    cur_num_chunks = 5
    fetched_chunks, retrieved_ids_scores = pinecone_retriever(cur_query, CUR_VECTOR_INDEX_NAME, num_chunks=cur_num_chunks)
    selected_chunks = sort_chunks_by_sim(fetched_chunks, retrieved_ids_scores, num_chunks=cur_num_chunks)
    parsed_chunks = parse_chunks(selected_chunks, retrieved_ids_scores)
    print("Parsed Chunks:")
    for idx, chunk in enumerate(parsed_chunks):
        print(f"Chunk {idx+1}:")
        print(f"Source: {chunk['source']}")
        print(f"Timestamp: {chunk['timestamp']}")
        print(f"Question: {chunk['question']}")
        print(f"Answer: {chunk['answer']}")
        print(f"Stars: {chunk['stars']}")
        print(f"Similarity Score: {chunk['sim']}")
        print(f"Display: {chunk['display']}")
        print("-" * 40)
def mtest_qrag_routing_call():
    pass
#if __name__ == "__main__":
    cur_json_obj = qrag_routing_call(
        user_question=CUR_QUERY,
        vector_index_name=CUR_VECTOR_INDEX_NAME,
        num_chunks=CUR_NUM_CHUNKS,
        routes_dict=CUR_ROUTES_DICT
    )
    # Optionally write to a JSON file
    write_json_file_from_object(cur_json_obj, CUR_JSON_PATH, overwrite='yes')

    # FOR PRINTING TO CONSOLE
    # print("Route Preamble:")
    # print(cur_json_obj['content']['route_preamble'])
    # print("\nQuoted QA:")
    # print(cur_json_obj['content']['quoted_qa'])
    # print("\nChunks Metadata:")
    # for chunk in cur_json_obj['content']['chunks']['chunks']:
    #     print(chunk)
    # print("\nAI Answer:")
    # print(cur_json_obj['content']['ai_answer'])
    print_qrag_display_text(cur_json_obj)
    print(f"OPENAI_API_KEY preview: {OPENAI_API_KEY[:12]}...")
def mtest_qrag_llm_call():
    pass
#if __name__ == "__main__":
    # Assuming you have already run mtest_qrag_routing_call and have cur_json_obj
    # Alternatively, you can recreate cur_json_obj here
    cur_json_obj = qrag_routing_call(
        user_question=CUR_QUERY,
        vector_index_name=CUR_VECTOR_INDEX_NAME,
        num_chunks=CUR_NUM_CHUNKS,
        routes_dict=CUR_ROUTES_DICT
    )
    # Now make the LLM call
    cur_json_obj = qrag_llm_call(cur_json_obj)
    print("LLM Prompt:")
    print(cur_json_obj['content'].get('llm_prompt', ''))
    print("\nAI Answer:")
    print(cur_json_obj['content']['ai_answer'])
def mtest_qrag_2step():
    pass
#if __name__ == "__main__":
    # cur_user_question1 = 'What is the meaning of life?'  # q1 PARTIAL MATCH
    # cur_user_question2 = 'What should I eat for lunch?'  # q2 NO MATCH
    # cur_user_question3 = 'What are computers and computation at a deep level?'  # q3 GOOD MATCH
    qrag_2step(CUR_QUERY, CUR_ROUTES_DICT, CUR_VECTOR_INDEX_NAME)


# NOT WORKING - See CHAT LOGGING comments
def mtest_run_batch_questions_on_bot_list(): 
    pass
#if __name__ == "__main__":    
    #run_batch_questions_on_bot_list('FDA_townhall_test1.md', FDA_TOWNHALL_TEST_QUESTIONS, [BOT_DICT_TOWNHALL_VRAG_V1])
    # run_batch_questions_on_bot_list('Deutsch_qraq_v1_t2.md', DEUTSCH_Q_LIST_T2, [BOT_DICT_DEUTSCH_QRAG_V1])



# cur_user_question = 'What should I eat for lunch?'  # q2 NO MATCH
# cur_json_path = 'tests/test_manual_files/rag/qrag_routing_oct1_q2.json'
# cur_user_question = 'What are computers and computation at a deep level?'  # q3 GOOD MATCH
# cur_json_path = 'tests/test_manual_files/rag/qrag_routing_oct1_q3.json'

# ===== END OF FILE primary/rag_mtests.py =====
