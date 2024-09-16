import sys
import os
from chalice import Chalice, Response

from chalicelib.rag import qrag_routing_call, print_qrag_display_text
from chalicelib.llm import simple_openai_chat_completion_request
from chalicelib.rag_prompts_routes import *
from chalicelib.vectordb import generate_embedding
from chalicelib.fileops import get_current_datetime_filefriendly

# not currently used langchain-layer arn:aws:lambda:us-west-2:957789311461:layer:langchain-layer:1

app = Chalice(app_name='qrag-routing')
app.api.cors = True

# last updated 7-19-24 RT code body to not hardcode route and index - see cursor chat history from 7-17-24
@app.route('/qrag-routing', methods=['POST'], cors=True)
def handle_qrag_routing():
    print("qrag-routing lambda func - last updated to include default parameters")
    print("Current Working Directory:", os.getcwd())
    print("Directory Contents /var/task/chalicelib:", os.listdir('/var/task/chalicelib'))

    try:
        received_request_data = app.current_request.json_body
        print("Received request data:", received_request_data)
        
        # Extract parameters from the request
        user_question = received_request_data['user_question']
        vector_index_name = received_request_data['vector_index_name']
        route_dict_name = received_request_data['route_dict_name']
        routes_bounds = received_request_data.get('routes_bounds', [0.3, 0.9])
        llm_model = received_request_data.get('llm_model', 'gpt-4o')
        user_id = received_request_data.get('user_id', 'default')
        qrag_version = received_request_data.get('qrag_version', '1.0')

        route_dict = globals().get(route_dict_name)  # Get the actual dictionary from the global namespace

        if not route_dict:
            return Response(body={'error': f'Invalid route dictionary: {route_dict_name}'}, status_code=400)

        if not all([user_question, route_dict, vector_index_name]):
            return Response(body={'error': 'Missing required parameters'}, status_code=400)
        
        # Call your custom multi-route retrieval augmented generation pipeline
        print("\nCalling qrag_routing...")
        response_json_object = qrag_routing_call(user_question, vector_index_name, route_dict, routes_bounds, llm_model, user_id, qrag_version)

        print("\nPrinting with print_qrag_display_text...")
        print_qrag_display_text(response_json_object)

        print("Returning JSON response...")
        return Response(body={'status': 'Success', 'response': response_json_object}, status_code=200)
    
    except Exception as e:
        print("Error while processing request:", e)
        return Response(body={'error': str(e)}, status_code=500)

# TO REDEPLOY WITH MIRROR SCRIPT
'''
cd /Users/randytrue/Documents/Code/corpus-tools/web/aws_chalice/qrag-routing; ../chalicelib_mirror_deploy.sh
'''

# API ENDPOINT: https://sz901mb96d.execute-api.us-west-2.amazonaws.com/api/qrag-routing

# TEST WITH CURL
# curl -X POST https://us05oglu51.execute-api.us-west-2.amazonaws.com/api/qrag-routing -H "Content-Type: application/json" -d '{"question": "What do you think about using curl commands to test AWS lambda functions?"}'

# TEST WITH PORTAL API GATEWAY (NOT IN LAMBDA FUNCTION VIEW)
# Headers:
'''
Content-Type:application/json
'''

# Request body:
'''
{
  "user_question": "Is this working from the Portal API Gateway Test tab?",
  "vector_index_name": "deutsch-transcript-qrag",
  "route_dict_name": "ROUTES_DICT_DEUTSCH_V3"
}
'''
