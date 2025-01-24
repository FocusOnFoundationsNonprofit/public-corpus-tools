# ===== START OF FILE hmac-hash/app.py =====
# file_path: web/aws_chalice/hmac-hash/app.py
# contains: python code for AWS Lambda Function 
#           deployed with Chalice using chalicelib_mirror_deploy.sh bash script

import sys
import os
from chalice import Chalice, Response
from chalicelib.aws import USERS_HMAC_SECRET_KEY, generate_hmac_hash

app = Chalice(app_name='hmac-hash')
app.api.cors = True

# Define allowed origins as a set
ALLOWED_ORIGINS = {
    'https://www.focusonfoundations.org',
    'https://floodlamp-8c9d00d6ef3e90c375de806594d04.webflow.io'
}

@app.route('/generate-hash', methods=['POST'], cors=True)
def handle_generate_hash():
    print("hmac-hash lambda func - last updated 12-20-24 RT ")
    
    # Get the origin from the request
    request_origin = app.current_request.headers.get('origin', '')
    
    # Set the CORS headers based on the request origin
    cors_headers = {
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Only add the origin if it's in our allowed list
    if request_origin in ALLOWED_ORIGINS:
        cors_headers['Access-Control-Allow-Origin'] = request_origin

    try:
        received_request_data = app.current_request.json_body
        print("Received request data:", received_request_data)
        
        # Extract input text from the request
        input_text = received_request_data.get('input_text')

        if not input_text:
            return Response(body={'error': 'Missing input_text parameter'}, status_code=400, headers=cors_headers)
        
        # Generate HMAC hash
        hash_string = generate_hmac_hash(input_text, USERS_HMAC_SECRET_KEY)

        print("Returning JSON response...")
        return Response(body={'status': 'Success', 'hash': hash_string}, status_code=200, headers=cors_headers)
    
    except Exception as e:
        print("Error while processing request:", e)
        return Response(body={'error': str(e)}, status_code=500, headers=cors_headers)

# TO REDEPLOY WITH MIRROR SCRIPT
'''
cd /Users/randytrue/Documents/Code/corpus-tools/web/aws_chalice/hmac-hash
../chalicelib_mirror_deploy.sh
'''

# TEST WITH CURL WITHOUT API KEY
# curl -X POST https://xusv8bpl49.execute-api.us-west-2.amazonaws.com/api/generate-hash -H "Content-Type: application/json" -d '{"input_text": "test@example.com"}'

# TEST WITH CURL WITH API KEY
# curl -X POST https://xusv8bpl49.execute-api.us-west-2.amazonaws.com/api/generate-hash -H "Content-Type: application/json" -H "x-api-key: bfua9..." -d '{"input_text": "test@example.com"}'

# TEST WITH PORTAL API GATEWAY (NOT IN LAMBDA FUNCTION VIEW)
# Headers:
'''
Content-Type:application/json
Origin:https://www.focusonfoundations.org
'''

# Request body:
'''
{
  "input_text": "test@example.com"
}
'''

# ===== END OF FILE hmac-hash/app.py =====
