from primary.fileops import *
from primary.llm import *
from primary.rag import *
from rag_prompts_routes import *

if True:
    pass
# if __name__ == "__main__":    
    cur_file_path = ""

### BOT FUNCTIONS
def mtest_qrag_routing_call():
    pass
# if __name__ == "__main__":    
    cur_user_question = 'What is the meaning of life?'  # q1 PARTIAL MATCH
    cur_json_path = 'tests/test_manual_files/rag/qrag_routing_q1.json'

    # cur_user_question = 'What should I eat for lunch?'  # q2 NO MATCH
    # cur_json_path = 'tests/test_manual_files/rag/qrag_routing_q2.json'

    # cur_user_question = 'What are computers and computation at a deep level?'  # q3 GOOD MATCH
    # cur_json_path = 'tests/test_manual_files/rag/qrag_routing_q3.json'

    # FOR CREATING JSON
    cur_json_obj = qrag_routing_call(cur_user_question, ROUTES_DICT_DEUTSCH_V3, 'deutsch-transcript-qrag')
    write_json_file_from_object(cur_json_obj, cur_json_path, overwrite='yes')

    # FOR PRINTING TO CONSOLE 
    print_qrag_display_text(cur_json_obj)
    print("\n\n")

    #print(get_qrag_display_dict(cur_json_obj))

def mtest_qrag_2step():
    pass
#if __name__ == "__main__":
    cur_user_question1 = 'What is the meaning of life?'  # q1 PARTIAL MATCH
    cur_user_question2 = 'What should I eat for lunch?'  # q2 NO MATCH
    cur_user_question3 = 'What are computers and computation at a deep level?'  # q3 GOOD MATCH
    qrag_2step(cur_user_question2,ROUTES_DICT_DEUTSCH_V3,'deutsch-transcript-qrag')

def mtest_vrag_llm_call():
    pass
if __name__ == "__main__":
    cur_user_question1 = "What is the meaning of life?"
    cur_user_question2 = "What is the Mathematician's Misconception?"
    cur_json_object = vrag_llm_call(cur_user_question1, 'dd-transcripts-vrag-80f-20240727')
    print_vrag_display_text(cur_json_object, show_prompt=False)


# NOT WORKING - See CHAT LOGGING comments
def mtest_run_batch_questions_on_bot_list(): 
    pass
#if __name__ == "__main__":    
    #run_batch_questions_on_bot_list('FDA_townhall_test1.md', FDA_TOWNHALL_TEST_QUESTIONS, [BOT_DICT_TOWNHALL_VRAG_V1])
    # run_batch_questions_on_bot_list('Deutsch_qraq_v1_t2.md', DEUTSCH_Q_LIST_T2, [BOT_DICT_DEUTSCH_QRAG_V1])
