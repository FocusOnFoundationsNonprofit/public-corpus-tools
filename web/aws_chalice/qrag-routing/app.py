# ===== START OF FILE qrag-routing/app.py =====
# in AWS Chalice for Lambda Function

import sys
import os
import json
from chalice import Chalice, Response

from chalicelib.rag import qrag_routing_call
# from chalicelib.llm import simple_openai_chat_completion_request
from chalicelib.rag_prompts_routes import *
from chalicelib.vectordb import generate_embedding
from chalicelib.fileops import get_current_datetime_filefriendly, write_json_file_from_json_data, pretty_print_json_data

from chalicelib.aws import verify_jwt

# not currently used langchain-layer arn:aws:lambda:us-west-2:957789311461:layer:langchain-layer:1

app = Chalice(app_name='qrag-routing')
app.api.cors = True

# Define allowed origins as a set
ALLOWED_ORIGINS = {
    'https://www.focusonfoundations.org',
    'https://floodlamp-8c9d00d6ef3e90c375de806594d04.webflow.io',
    'http://localhost:8000'
}

@app.route('/qrag-routing', methods=['POST'], cors=True)
def handle_qrag_routing():
    print("qrag-routing lambda func - last updated 2025-02-15 1704 added error handling for empty user question")
    
    # Enhanced request logging
    request_headers = app.current_request.headers
    request_origin = request_headers.get('origin', 'No origin provided')
    print(f"Request Origin: {request_origin}")
    print(f"Request Headers: {json.dumps(dict(request_headers), default=str)}")
    print("Current Working Directory:", os.getcwd())
    print("Directory Contents /var/task/chalicelib:", os.listdir('/var/task/chalicelib'))

    # Get the origin and set up CORS headers
    cors_headers = {
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    
    # Enhanced CORS logging
    if request_origin in ALLOWED_ORIGINS:
        cors_headers['Access-Control-Allow-Origin'] = request_origin
        print(f"Origin '{request_origin}' is allowed.")
    else:
        print(f"Origin '{request_origin}' is NOT in allowed list: {ALLOWED_ORIGINS}")

    raw_request_data = app.current_request.raw_body.decode('utf-8', errors='replace')
    print("Raw request data:", raw_request_data)
    
    try:
        # Enhanced JWT verification logging
        auth_header = app.current_request.headers.get('Authorization')
        if not auth_header:
            error_msg = "ERROR: No Authorization header present"
            print(error_msg)
            return Response(
                body={'error': 'Missing Authorization header'},
                status_code=401,
                headers=cors_headers
            )
        if not auth_header.startswith('Bearer '):
            error_msg = "ERROR: Authorization header does not start with 'Bearer '"
            print(error_msg)
            return Response(
                body={'error': 'Invalid Authorization header format'},
                status_code=401,
                headers=cors_headers
            )

        token = auth_header.split(' ')[1]
        print("Attempting to verify JWT token...")
        claims = verify_jwt(token)
        
        if not claims:
            error_msg = "ERROR: JWT verification failed (Invalid or expired token)"
            print(error_msg)
            return Response(
                body={'error': 'Invalid or expired JWT token'},
                status_code=401,
                headers=cors_headers
            )
        print("JWT verification successful. Claims:", claims)

        # Continue with existing functionality
        received_request_data = app.current_request.json_body
        print("Received request data:", received_request_data)
        
        if not received_request_data:
            error_msg = "ERROR: Empty JSON body"
            print(error_msg)
            return Response(
                body={'error': error_msg},
                status_code=400,
                headers=cors_headers
            )

        # Enhanced required fields validation
        required_fields = ['user_question', 'vector_index_name', 'route_dict_name']
        missing_fields = [field for field in required_fields if field not in received_request_data]
        if missing_fields:
            error_msg = f"ERROR: Missing required fields: {missing_fields}"
            print(error_msg)
            return Response(
                body={'error': f'Missing required parameters: {", ".join(missing_fields)}'},
                status_code=400,
                headers=cors_headers
            )

        # Extract parameters from the request
        user_question = received_request_data['user_question']
        vector_index_name = received_request_data['vector_index_name']
        route_dict_name = received_request_data['route_dict_name']
        routes_bounds = received_request_data.get('routes_bounds', [0.3, 0.9])
        user_id = received_request_data.get('user_id', 'default')
        qrag_version = received_request_data.get('qrag_version', '2.0')
        num_chunks = received_request_data.get('num_chunks', 2)  # Default to 2 if not provided
        
        # After extracting parameters from the request
        user_question = received_request_data['user_question']
        if not user_question or not user_question.strip():
            error_msg = "ERROR: User question cannot be empty"
            print(error_msg)
            return Response(
                body={'error': error_msg},
                status_code=400,
                headers=cors_headers
            )

        # Validate route_dict exists in globals
        route_dict = globals().get(route_dict_name)
        if not route_dict:
            error_msg = f"ERROR: Invalid route dictionary: {route_dict_name}"
            print(error_msg)
            return Response(
                body={'error': error_msg},
                status_code=400,
                headers=cors_headers
            )

        # Extract and validate date range if provided
        start_date = received_request_data.get('start_date')
        end_date = received_request_data.get('end_date')
        
        if start_date or end_date:
            import re
            date_pattern = r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'
            
            if not (start_date and end_date):
                return Response(
                    body=json.dumps({'error': 'Both start_date and end_date must be provided together'}),
                    status_code=400,
                    headers=cors_headers
                )
            
            if not (re.match(date_pattern, start_date) and re.match(date_pattern, end_date)):
                return Response(
                    body=json.dumps({'error': 'Dates must be in YYYY-MM-DD format'}),
                    status_code=400,
                    headers=cors_headers
                )

        # Create date_range list if valid dates were provided
        date_range = [start_date, end_date] if (start_date and end_date) else None

        # Extract user context from request
        user_context = {
            'hashedNiceName': received_request_data.get('hashedUserNiceName'),
            'hashedIPAddress': received_request_data.get('hashedUserIPAddress'),
            'hashedEmail': received_request_data.get('hashedInputUserEmail')
        } if any(key in received_request_data for key in [
            'hashedUserNiceName', 
            'hashedUserIPAddress', 
            'hashedInputUserEmail'
        ]) else None

        # Call your custom multi-route retrieval augmented generation pipeline
        print("\nCalling qrag_routing...")
        response_json_object = qrag_routing_call(
            user_question,
            vector_index_name,
            num_chunks,
            route_dict,
            date_range,
            routes_bounds,
            user_id,
            user_context,  # Pass the user context as an optional parameter
            qrag_version
        )

        print("\nPrinting JSON object with pretty_print_json_data...")
        pretty_print_json_data(response_json_object, print_values=True)

        print("Returning JSON response...")
        return Response(
            body=json.dumps({'status': 'Success', 'response': response_json_object}),
            status_code=200,
            headers=cors_headers
        )
    
    except json.JSONDecodeError as e:
        error_msg = f"ERROR: Invalid JSON in request body: {str(e)}"
        print(error_msg)
        return Response(
            body={'error': 'Invalid JSON format'},
            status_code=400,
            headers=cors_headers
        )
    except Exception as e:
        error_type = type(e).__name__
        error_details = str(e)
        print(f"ERROR: Unexpected error: {error_details} (type: {error_type})")
        return Response(
            body={'error': str(e)},
            status_code=500,
            headers=cors_headers
        )

# TO REDEPLOY WITH MIRROR SCRIPT
'''
cd /Users/randytrue/Documents/Code/corpus-tools/web/aws_chalice/qrag-routing
../chalicelib_mirror_deploy.sh
'''

# TEST WITH CURL WITH JWT
# curl -X POST https://us05oglu51.execute-api.us-west-2.amazonaws.com/api/qrag-routing -H "Content-Type: application/json" -H "Authorization: Bearer eyJh..." -d '{"user_question": "Is this test working with JWT?", "vector_index_name": "deutsch-transcript-qrag-78f-20240926", "num_chunks": 3, "route_dict_name": "ROUTES_DICT_DEUTSCH_V4", "routes_bounds": [0.3, 0.9], "llm_model": "gpt-4o", "user_id": "test_user", "qrag_version": "1.0"}'
'''
curl -X POST https://us05oglu51.execute-api.us-west-2.amazonaws.com/api/qrag-routing \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Origin: https://www.focusonfoundations.org" \
  -d '{"user_question": "test", "vector_index_name": "deutsch-transcript-qrag-78f-20240926", "route_dict_name": "ROUTES_DICT_DEUTSCH_V4", "num_chunks": 2}'
'''

# TEST WITH CURL WITHOUT API KEY OR JWT
# curl -X POST https://us05oglu51.execute-api.us-west-2.amazonaws.com/api/qrag-routing -H "Content-Type: application/json" -d '{"user_question": "Is this test working from the Curl with API key?", "vector_index_name": "deutsch-transcript-qrag-78f-20240926", "num_chunks": 3, "route_dict_name": "ROUTES_DICT_DEUTSCH_V4", "routes_bounds": [0.3, 0.9], "llm_model": "gpt-4o", "user_id": "test_user", "qrag_version": "1.0"}'

# TEST WITH CURL WITH API KEY
# curl -X POST https://us05oglu51.execute-api.us-west-2.amazonaws.com/api/qrag-routing -H "Content-Type: application/json" -H "x-api-key: Fhhs7..." -d '{"user_question": "Is this test working from the Curl with API key?", "vector_index_name": "deutsch-transcript-qrag-78f-20240926", "num_chunks": 3, "route_dict_name": "ROUTES_DICT_DEUTSCH_V4", "routes_bounds": [0.3, 0.9], "llm_model": "gpt-4o", "user_id": "test_user", "qrag_version": "1.0"}'

# TEST WITH PORTAL API GATEWAY (NOT IN LAMBDA FUNCTION VIEW)
# Headers:
'''
Content-Type:application/json,
Origin:https://www.focusonfoundations.org,
Authorization:Bearer your_jwt_token_here
'''

# Request body for PV Evac:
'''
{
  "user_question": "Is this PV Evac QRAG working from the Portal API Gateway Test tab with CORS restricted to fof domain?",
  "vector_index_name": "pv-evac-qrag-2f-20241024",
  "num_chunks": 3,
  "route_dict_name": "ROUTES_DICT_PV_EVAC_V1",
  "routes_bounds": [0.3, 0.9],
  "llm_model": "gpt-4o",
  "user_id": "test_user",
  "qrag_version": "1.0",
  "hashedUserNiceName": "abc123...hash_value_here",
  "hashedUserIPAddress": "def456...hash_value_here",
  "hashedInputUserEmail": "ghi789...hash_value_here"
}
'''

# Request body for Deutsch:
'''
{
  "user_question": "Is this Deutsch QRAG working from the Portal API Gateway Test tab with CORS restricted to fof domain?",
  "vector_index_name": "deutsch-transcript-qrag-78f-20240926",
  "num_chunks": 3,
  "route_dict_name": "ROUTES_DICT_DEUTSCH_V4",
  "routes_bounds": [0.3, 0.9],
  "llm_model": "gpt-4o",
  "user_id": "test_user",
  "qrag_version": "1.0",
  "hashedUserNiceName": "abc123...hash_value_here",
  "hashedUserIPAddress": "def456...hash_value_here",
  "hashedInputUserEmail": "ghi789...hash_value_here"
}
'''

# ===== END OF FILE qrag-routing/app.py =====



