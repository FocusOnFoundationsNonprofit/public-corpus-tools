from chalice import Chalice, Response
import json
import os

from chalicelib.rag import qrag_llm_call, print_qrag_display_text
from chalicelib.aws import upload_file_to_s3
from chalicelib.llm import simple_openai_chat_completion_request
from chalicelib.rag_prompts_routes import *
from chalicelib.vectordb import generate_embedding
from chalicelib.fileops import get_current_datetime_filefriendly


app = Chalice(app_name='qrag-llm')
app.api.cors = True  # Enable CORS for all routes

@app.route('/qrag-llm', methods=['POST'], cors=True)
def handle_qrag_llm():
    raw_request_data = app.current_request.raw_body.decode('utf-8')
    print("Raw request data:", raw_request_data)
    try:
        received_request_data = app.current_request.json_body
        print("Received request data:", received_request_data)
        
        # Define paths
        json_prefix = 'qrag-exch_'
        json_file_path = '/tmp/' + json_prefix + get_current_datetime_filefriendly() + '.json'

        # Call the function to get the AI response
        print("\nCalling qrag_llm...")
        response_json_object = qrag_llm_call(received_request_data)

        print("\nPrinting JSON object with print_qrag_display_text...")
        print_qrag_display_text(response_json_object)

        print("\nWriting JSON to file...")
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        with open(json_file_path, 'w') as json_file:
            json.dump(response_json_object, json_file, indent=4)

        print("\nUploading JSON to S3...")
        upload_file_to_s3(json_file_path, bucket='fofsecure', s3_path='s3-qrag-deutsch-v3')

        print("Returning JSON response...")
        return Response(body={'status': 'Success', 'response': response_json_object}, status_code=200)
    
    except Exception as e:
        print("Error while processing request:", e)  # Log any exceptions
        return Response(body={'error': str(e)}, status_code=500)

# TO REDEPLOY WITH MIRROR SCRIPT
'''
cd /Users/randytrue/Documents/Code/corpus-tools/web/aws_chalice/qrag-llm; ../chalicelib_mirror_deploy.sh
'''

# API ENDPOINT: https://sz901mb96d.execute-api.us-west-2.amazonaws.com/api/qrag-llm

# SKIP CURL TEST BECAUSE JSON IS BIG

# TEST WITH PORTAL API GATEWAY (NOT IN LAMBDA FUNCTION VIEW)
# Headers:
'''
Content-Type:application/json
'''

# Request body:
{
    "metadata": {
        "timestamp": "2024-06-13T11:46:33.651753",
        "user_id": "default",
        "index_name": "deutsch-transcript-qrag",
        "bot_version": "1.0",
        "llm_model": "gpt-4o",
        "routes_info": {
            "routes_flow_name": "3 routes, sim-star double, separate prompts",
            "upper_sim_bound": 0.9,
            "lower_sim_bound": 0.3,
            "max_sim": "0.216",
            "max_stars": 5,
            "routes_dict_content": {
                "routes_dict_name": "ROUTES_DICT_DEUTSCH_V3",
                "prompt_initial_good_match": "Given your knowledge of David Deutsch and his philosophy of deep optimism, as well as the QUOTED QUESTIONS AND ANSWERS from Deutsch below, to answer the USER QUESTION below.\n",
                "route_preamble_good_match": "There is a good match of your question in David Deutsch's interviews. See his QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with David Deutsch's philosophy and your exact question.",
                "prompt_initial_partial_match": "Given your knowledge of David Deutsch and his philosophy of deep optimism, as well as the QUOTED QUESTIONS AND ANSWERS from Deutsch below, to answer the USER QUESTION below.\n",
                "route_preamble_partial_match": "There is a partial match of your question in David Deutsch's interviews. See his QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with David Deutsch's philosophy and your exact question.",
                "prompt_initial_no_match": "Given your knowledge of David Deutsch and his philosophy of deep optimism, answer the USER QUESTION below.\n",
                "route_preamble_no_match": "Your question is not addressed in David Deutsch's interviews. No QUOTED QUESTIONS AND ANSWERS are therefore provided but here is an AI ANSWER that synthesizes David Deutsch's philosophy and your question.",
                "quoted_qa_single": "QUOTED QUESTION: {top_sim_question}\nQUOTED SOURCE: {top_sim_source}\nQUOTED TIMESTAMP: {top_sim_timestamp}\nQUOTED ANSWER: {top_sim_answer}\n{top_sim_display}\n\n",
                "quoted_qa_double": "QUOTED QUESTION 1: {top_stars_question}\nQUOTED SOURCE 1: {top_stars_source}\nQUOTED TIMESTAMP 1: {top_stars_timestamp}\nQUOTED ANSWER 1: {top_stars_answer}\n{top_stars_display}\n\nQUOTED QUESTION 2: {top_sim_question}\nQUOTED SOURCE 2: {top_sim_source}\nQUOTED TIMESTAMP 2: {top_sim_timestamp}\nQUOTED ANSWER 2: {top_sim_answer}\n{top_sim_display}\n\n",
                "user_ai_qa": "USER QUESTION: {user_question}\n\nAI ANSWER: "
            }
        }
    },
    "content": {
        "user_question": "What should I eat for lunch?",
        "route_preamble": "Your question is not addressed in David Deutsch's interviews. No QUOTED QUESTIONS AND ANSWERS are therefore provided but here is an AI ANSWER that synthesizes David Deutsch's philosophy and your question.",
        "quoted_qa": "",
        "ai_answer": "WAITING FOR LLM RESPONSE",
        "chunks": {
            "max_sim": "0.216",
            "max_stars": 5,
            "chunks": [
                {
                    "question": "How should one think about choices to pursue what one finds interesting and fun versus helping the world?",
                    "source": "2021-01-09_Knowledge and Reality OurKarlPopper - Meeting David Deutsch_qafixed.md",
                    "timestamp": "[1:12:40](https://www.youtube.com/watch?v=Qrt0XXg0QKM&t=4360)",
                    "answer": "__I don't think it's a good idea to try and save the world in the sense of subordinating one's own values to what one thinks the world's values are.__",
                    "stars": 5,
                    "sim": "0.216"
                },
                {
                    "question": "What is your advice on advice?",
                    "source": "2022-01-30_Lunar Society podcast - AI America Fun and Bayes_qafixed.md",
                    "timestamp": "[1:20:19](https://www.youtube.com/watch?v=EVwjofV5TgU&t=4819)",
                    "answer": "I try very hard not to give advice. Because it's not a good relationship to be with somebody to give them advice. ",
                    "stars": 5,
                    "sim": "0.196"
                }
            ]
        }
    }
}

