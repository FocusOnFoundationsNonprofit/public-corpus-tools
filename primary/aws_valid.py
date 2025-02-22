# ===== START OF FILE primary/aws-valid.py =====
# Library for setup and testing AWS API Gateway validation

import os
import sys
import re
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime, timedelta
from time import sleep
import requests
import io
import subprocess
from termcolor import colored
from contextlib import redirect_stdout
    
from primary.fileops import *
from primary.aws import *

# ---API KEYS AND SECRETS---
from dotenv import load_dotenv
load_dotenv(override=True)  # Load environment variables from .env file
JWT_TEST = os.environ['JWT_01-22']


# ---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

### AWS API GATEWAY VALIDATION
''' Categories of test requests:
clean_requests: Well-formed inputs that meet all schema and functional requirements.
schema_invalid_requests: Inputs that violate schema constraints but would still be acceptable by the function's logic if not for API Gateway validation (e.g., too long, but not empty).
function_invalid_requests: Inputs that break the function's own basic logic checks (e.g., missing or empty required fields).
'''
''' API GATEWAY IDs
deepgram-callback    lsehufc3n2
hash-store           wd3rapoqy7
hmac-hash            xusv8bpl49
qrag-llm             sz901mb96d
qrag-routing         us05oglu51
send-email           lvyznjx395
testapp              az3tpr2gv0
vrag-llm             n5yjgn8jak
'''
MAX_USER_NAME_LENGTH = 64  # sync with webflow-fof-site-body.js var maxUserNameLength
MAX_QUESTION_LENGTH = 500  # sync with webflow-fof-site-body.js var maxQuestionLength
MAX_FILE_NAME_LENGTH = 255  # sync with webflow-fof-site-body.js var maxFileNameLength
MAX_EMAIL_ADDRESS_LENGTH = 254  # sync with webflow-fof-site-body.js var maxEmailLength
MAX_PARAMETER_LENGTH = 50  # use as a default for internal parameters and variable names
MIN_NUM_CHUNKS = 2  # sync with min num-chunks-options in webflow-qrag-input-component-embed.html
MAX_NUM_CHUNKS = 20  # sync with max num-chunks-options in webflow-qrag-input-component-embed.html, think pinecone_retriever can go higher
LLM_MODEL_OPTIONS = ["gpt-4o", "gpt-4o-mini", "o3-mini", "deepseek-reasoner", "o3", "o1", "BLANK from qrag-routing lambda", "BLANK from qrag_routing_call"]
REMOVE_FIELD = "__REMOVE_FIELD__"  # # Define a sentinel value for field removal

# SKIPPED IMPLEMENTING THIS SCHEMA FOR API GATEWAY VALIDATION 12-16-24 RT
SCHEMA_DEEPGRAM_CALLBACK = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "DeepgramCallbackRequest",
    "type": "object",
    "properties": {
        "metadata": {
            "type": "object",
            "properties": {
                "request_id": {
                    "type": "string"
                }
            }
        }
    },
    "additionalProperties": True
}

API_ENDPOINT_HASH_STORE = "https://wd3rapoqy7.execute-api.us-west-2.amazonaws.com/api/hash-store"
SCHEMA_HASH_STORE = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "HashStoreRequest",
    "type": "object",
    "required": [
        "key",
        "userNiceName",
        "userIPAddress",
        "eventType"
    ],
    "properties": {
        "key": {
            "type": "string",
            "pattern": "^user_hash_log_[0-9]{4}-[0-9]{2}-[0-9]{2}\\.csv$"
        },
        "s3_path": {
            "type": "string"
        },
        "userNiceName": {
            "type": "string",
            "minLength": 1,
            "maxLength": MAX_USER_NAME_LENGTH
        },
        "userIPAddress": {
            "type": "string",
            "minLength": 7,
            "maxLength": 45  # Accommodates both IPv4 and IPv6
        },
        "inputUserEmail": {
            "type": "string",
            "maxLength": MAX_EMAIL_ADDRESS_LENGTH
        },
        "emailListSignupChecked": {
            "type": ["boolean", "null"]
        },
        "eventType": {
            "type": "string",
            "minLength": 1,
            "maxLength": MAX_PARAMETER_LENGTH
        },
        "privacyConsent": {
            "type": "string",  # allow to be any string and do not enforce date format at this point
            "minLength": 1,
            "maxLength": MAX_PARAMETER_LENGTH
        }
    },
    "additionalProperties": False
}
TEST_REQUESTS_HASH_STORE = {
    "clean_requests": [
        {   
            "description": "Full valid request",
            "request": {
                "key": "user_hash_log_2024-12-17.csv",
                "s3_path": "",
                "userNiceName": "TEST aws-valid", 
                "userIPAddress": "192.168.1.1",
                "inputUserEmail": "test@example.com",
                "emailListSignupChecked": True,
                "eventType": "test",
                "privacyConsent": "2024-12-17"
            }
        },
        {   
            "description": "No email address or signup checkbox",
            "request": {
                "key": "user_hash_log_2024-12-17.csv",
                "s3_path": "",
                "userNiceName": "TEST aws-valid", 
                "userIPAddress": "192.168.1.1",
                "inputUserEmail": "",
                "emailListSignupChecked": None,  # should be set to 'null' in the request
                "eventType": "test",
                "privacyConsent": "2024-12-17"
            }
        },
        {   
            "description": "All fields with maximum complexity",
            "request": {
                "userNiceName": "A" * MAX_USER_NAME_LENGTH,
                "userIPAddress": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                "inputUserEmail": "very.long.email+tag@really.long.domain.co.uk"
            }
        }
    ],
    
    "schema_invalid_requests": [
        {   
            "description": "Additional field added",
            "request": {
                "other_field": "some value"
            }
        },
        {   
            "description": "userNiceName too long",
            "request": {
                "userNiceName": "A" * (MAX_USER_NAME_LENGTH + 1)
            }
        },
        {   
            "description": "Invalid IP format",
            "request": {
                "userIPAddress": "bad.ip"
            }
        },
        {   
            "description": "Wrong type",
            "request": {
                "eventType": ["not", "a", "string"]
            }
        }
    ],
    
    "function_invalid_requests": [
        {   
            "description": "Missing required field",
            "request": {
                "userNiceName": REMOVE_FIELD
            }
        },
        {   
            "description": "Invalid key",
            "request": {
                "key": "invalid_filename.csv"
            }
        }
    ]
}

API_ENDPOINT_HMAC_HASH = "https://xusv8bpl49.execute-api.us-west-2.amazonaws.com/api/generate-hash"
SCHEMA_HMAC_HASH = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "HMACHashRequest", 
    "type": "object",
    "required": ["input_text"],
    "properties": {
        "input_text": {
            "type": "string",
            "minLength": 1,
            "maxLength": MAX_EMAIL_ADDRESS_LENGTH  # max lenth of userInputEmail
        }
    },
    "additionalProperties": False
}
TEST_REQUESTS_HMAC_HASH = {
    "clean_requests": [
        {   
            "description": "Basic valid email",
            "request": {
                "input_text": "test@example.com"
            }
        },
        {   
            "description": "Complex but valid email",
            "request": {
                "input_text": "user.name+tag@domain.co.uk"
            }
        }
    ],

    "schema_invalid_requests": [
        {   
            "description": "Additional field added",
            "request": {
                "other_field": "some value"
            }
        },
        {   
            "description": "Too long (255 chars, exceeds maxLength)",
            "request": {
                "input_text": "a" * 255
            }
        }
    ],

    "function_invalid_requests": [
        {   
            "description": "Wrong type",
            "request": {
                "input_text": 12345
            }
        },
        {   
            "description": "Null value",
            "request": {
                "input_text": None
            }
        },
        {   
            "description": "Empty string (fails minLength)",
            "request": {
                "input_text": ""
            }
        }
    ]
}

API_ENDPOINT_QRAG_ROUTING = "https://us05oglu51.execute-api.us-west-2.amazonaws.com/api/qrag-routing"
SCHEMA_QRAG_ROUTING = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "QRAGRoutingRequest", 
    "description": "Schema for validating QRAG routing requests",
    "type": "object",
    "required": [
        "user_question",
        "vector_index_name",
        "route_dict_name"
    ],
    "properties": {
        "user_question": {
            "type": "string",
            "description": "The user's question to be answered",
            "minLength": 1,
            "maxLength": MAX_QUESTION_LENGTH
        },
        "vector_index_name": {
            "type": "string", 
            "description": "Name of the vector index to search against"
        },
        "route_dict_name": {
            "type": "string",
            "description": "Name of the routing dictionary to use, must start with ROUTES_DICT_",
            "pattern": "^ROUTES_DICT_.*$"
        },
        "routes_bounds": {
            "type": "array",
            "description": "Array of two numbers between 0 and 1 defining the routing bounds",
            "items": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
            },
            "minItems": 2,
            "maxItems": 2
        },
        "user_id": {
            "type": "string",
            "description": "Unique identifier for the user making the request",
            "minLength": 1,
            "maxLength": MAX_USER_NAME_LENGTH
        },
        "qrag_version": {
            "type": "string",
            "description": "Version of the QRAG system being used"
        },
        "num_chunks": {
            "type": "integer",
            "description": "Number of text chunks to retrieve from the vector store",
            "minimum": MIN_NUM_CHUNKS,
            "maximum": MAX_NUM_CHUNKS
        },
        "start_date": {
            "type": "string",
            "pattern": "^(?:\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01]))$"
        },
        "end_date": {
            "type": "string",
            "pattern": "^(?:\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01]))$"
        },
        "hashedUserNiceName": {
            "type": "string",
            "description": "Hashed version of user's display name",
            "maxLength": 128
        },
        "hashedUserIPAddress": {
            "type": "string",
            "description": "Hashed version of user's IP address",
            "maxLength": 128
        },
        "hashedInputUserEmail": {
            "type": "string",
            "description": "Hashed version of user's email address",
            "maxLength": 128
        }
    },
    "additionalProperties": False
}
TEST_REQUESTS_QRAG_ROUTING = {
    "clean_requests": [
        {   
            "description": "Complete template request with all fields including hashed user data",
            "request": {
                "user_question": "Is this working from the aws-valid.py module?",
                "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
                "num_chunks": 2,
                "route_dict_name": "ROUTES_DICT_DEUTSCH_M1",
                "routes_bounds": [0.3, 0.9],
                "user_id": "test_user",
                "qrag_version": "2.0",
                "hashedUserNiceName": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
                "hashedUserIPAddress": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1",
                "hashedInputUserEmail": "c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0v1w2"
            }
        },
        {   
            "description": "Add start_date and end_date",
            "request": {
                "start_date": "1995-01-01",
                "end_date": "2024-12-23"
            }
        }
    ],

    "schema_invalid_requests": [
        {   
            "description": "Out of range - Values must be between 0 and 1",
            "request": {
                "routes_bounds": [-1, 2]
            }
        },
        {   
            "description": "Out of range num_chunks - Exceeds MAX_NUM_CHUNKS",
            "request": {
                "num_chunks": MAX_NUM_CHUNKS + 1
            }
        },
        {   
            "description": "Invalid hashedUserNiceName - Exceeds maxLength",
            "request": {
                "hashedUserNiceName": "a" * 129  # 129 characters, max is 128
            }
        },
        {   
            "description": "Invalid hashedUserIPAddress - Wrong type",
            "request": {
                "hashedUserIPAddress": ["not-a-string"]
            }
        },
        {   
            "description": "Invalid hashedInputUserEmail - Wrong type",
            "request": {
                "hashedInputUserEmail": 12345
            }
        }
    ],

    "function_invalid_requests": [
        {   
            "description": "Missing required field",
            "request": {
                "user_question": REMOVE_FIELD
            }
        },
        {   
            "description": "Invalid data types - Should be string",
            "request": {
                "user_question": 12345
            }
        },
        {   
            "description": "Empty required field - Function will not accept empty string",
            "request": {
                "user_question": ""
            }
        },
        {   
            "description": "Invalid data types - Should be string",
            "request": {
                "vector_index_name": ["invalid-type"]
            }
        },
        {   
            "description": "Invalid data types - Should be integer",
            "request": {
                "num_chunks": "3"
            }
        },
        {   
            "description": "Invalid routes_bounds array length - Should be exactly 2 items",
            "request": {
                "routes_bounds": [0.3, 0.5, 0.8]
            }
        },
    ]
}

API_ENDPOINT_QRAG_LLM = "https://sz901mb96d.execute-api.us-west-2.amazonaws.com/api/qrag-llm"
SCHEMA_QRAG_LLM = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "QRAGLLMRequest", 
    "type": "object",
    "required": ["metadata", "content"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["routes_info", "vector_index_name"],
            "properties": {
                "vector_index_name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": MAX_PARAMETER_LENGTH
                },
                "user_id": {
                    "type": "string",
                    "maxLength": MAX_USER_NAME_LENGTH
                },
                "bot_version": {
                    "type": "string",
                    "maxLength": MAX_PARAMETER_LENGTH
                },
                "timestamp": {
                    "type": "string",
                    "maxLength": MAX_PARAMETER_LENGTH
                },
                "large_context_filename": {
                    "type": ["string", "null"],  # Allow either string or null
                    "maxLength": MAX_FILE_NAME_LENGTH
                },
                "routes_info": {
                    "type": "object",
                    "properties": {
                        "routes_flow_name": {"type": "string"},
                        "upper_sim_bound": {"type": "number"},
                        "lower_sim_bound": {"type": "number"},
                        "max_sim": {"type": "string"},
                        "max_stars": {"type": "integer"},
                        "routes_dict_content": {"type": "object"}
                    },
                    "additionalProperties": True
                },
                "is_retry": {
                    "type": "boolean"
                }
            },
            "additionalProperties": True
        },
        "content": {
            "type": "object",
            "required": ["user_question", "prompt_initial", "quoted_qa"],
            "properties": {
                "user_question": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": MAX_QUESTION_LENGTH
                },
                "route_preamble": {"type": "string"},
                "prompt_initial": {"type": "string"},
                "quoted_qa": {"type": "string"},
                "ai_answer": {"type": "string"},
                "chunks": {
                    "type": "object",
                    "properties": {
                        "max_sim": {"type": "string"},
                        "max_stars": {"type": "integer"},
                        "chunks": {"type": "array"}
                    }
                }
            },
            "additionalProperties": False
        }
    }
}
TEST_REQUESTS_QRAG_LLM = {
    "clean_requests": [
        {   
            "description": "Complete matching Portal API Gateway test",
            "request": {
                "metadata": {
                    "timestamp": "2024-06-13T11:46:33.651753",
                    "user_id": "default", 
                    "vector_index_name": "deutsch-transcript-qrag-83f-20250202",
                    "bot_version": "2.0",
                    "routes_info": {
                        "routes_flow_name": "3 routes, separate route prompts",
                        "upper_sim_bound": 0.9,
                        "lower_sim_bound": 0.3,
                        "max_sim": "0.216",
                        "max_stars": 5,
                        "routes_dict_content": {
                            "routes_dict_name": "ROUTES_DICT_DEUTSCH_M1"
                        }
                    }
                },
                "content": {
                    "user_question": "What should I eat for lunch?",
                    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
                    "prompt_initial": "Given your knowledge of David Deutsch and his philosophy...",
                    "quoted_qa": "",
                    "ai_answer": "WAITING FOR LLM RESPONSE",
                    "chunks": {
                        "max_sim": "0.216",
                        "max_stars": 5,
                        "chunks": []
                    }
                }
            }
        },
        {
            "description": "Complete matching Portal API Gateway test with large context filename",
            "request": {
                "metadata": {
                    "large_context_filename": "deutsch_large_context_v1.md"
                }
            }
        },
        {   
            "description": "Test retry flag",
            "request": {
                "metadata": {
                    "is_retry": True
                }
            }
        }
    ],
    "schema_invalid_requests": [
        {
            "description": "Exceeds maxLength",
            "request": {
                "metadata": {
                    "timestamp": "A"*(MAX_PARAMETER_LENGTH + 1)
                }
            }
        },
        {   
            "description": "Empty required field",
            "request": {
                "content": {
                    "user_question": ""
                }
            }
        },
        {   
            "description": "Invalid data types in content",
            "request": {
                "content": {
                    "user_question": 12345
                }
            }
        }
    ],

    "function_invalid_requests": [
        {   
            "description": "Missing required top-level field", 
            "request": {
                "metadata": REMOVE_FIELD
            }
        },
        {   
            "description": "Missing required content field",
            "request": {
                "content": {
                    "user_question": REMOVE_FIELD
                }
            }
        },
        {   
            "description": "Invalid data types in metadata",
            "request": {
                "metadata": {
                    "vector_index_name": ["invalid-type"]
                }
            }
        },
        {
            "description": "Large context filename not in S3 folder",
            "request": {
                "metadata": {
                    "large_context_filename": "not-present-filename.md"
                }
            }
        }
    ]
}

API_ENDPOINT_SEND_EMAIL = "https://lvyznjx395.execute-api.us-west-2.amazonaws.com/api/send-email"
SCHEMA_SEND_EMAIL = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "SendEmailRequest",
    "type": "object",
    "required": ["to_address", "email_subject", "from_address"],
    "properties": {
        "to_address": {
            "type": "string",
            "format": "email",
            "maxLength": 254  # RFC 5321
        },
        "from_address": {
            "type": "string",
            "format": "email",
            "maxLength": 254
        },
        "email_subject": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
        },
        "email_body_plain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10000
        },
        "email_body_html": {
            "type": "string",
            "maxLength": 50000
        },
        "attachments": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["filename", "content"],
                "properties": {
                    "filename": {
                        "type": "string",
                        "pattern": "^[\\w\\-. ]+$",
                        "maxLength": 255
                    },
                    "content": {
                        "type": "string",
                        "pattern": "^[A-Za-z0-9+/=]+$"  # Base64 pattern
                    }
                }
            },
            "maxItems": 10
        }
    },
    "additionalProperties": False
}
TEST_REQUESTS_SEND_EMAIL = {
    "clean_requests": [
        {   
            "description": "Basic email without HTML or attachments",
            "request": {
                "to_address": "recipient@example.com",
                "from_address": "contact@focusonfoundations.org", 
                "email_subject": "Test Subject",
                "email_body_plain": "Hello, this is a test email."
            }
        },
        {   
            "description": "Full featured email with HTML and attachment",
            "request": {
                "email_subject": "Test with Attachments",
                "email_body_plain": "Please see attached file.",
                "email_body_html": "<p>Please see attached file.</p>",
                "attachments": [{
                    "filename": "test.txt",
                    "content": "SGVsbG8gV29ybGQ="  # Base64 encoded "Hello World"
                }]
            }
        }
    ],
    "schema_invalid_requests": [
        {   
            "description": "Subject too long (>200 chars)",
            "request": {
                "email_subject": "A" * 201
            }
        }
    ],
    "function_invalid_requests": [
        {   
            "description": "Missing required field",
            "request": {
                "to_address": REMOVE_FIELD
            }
        },
        {   
            "description": "Missing required field", 
            "request": {
                "from_address": REMOVE_FIELD
            }
        },
        {   
            "description": "Empty required field",
            "request": {
                "to_address": ""
            }
        },
        {   
            "description": "Invalid email format",
            "request": {
                "to_address": "not-an-email"
            }
        }
    ]
}

API_ENDPOINT_VRAG_LLM = "https://n5yjgn8jak.execute-api.us-west-2.amazonaws.com/api/vrag-llm"
SCHEMA_VRAG_LLM = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "VRAGLLMRequest",
    "type": "object",
    "required": [
        "user_question",
        "vector_index_name"
    ],
    "properties": {
        "user_question": {
            "type": "string",
            "minLength": 1,
            "maxLength": MAX_QUESTION_LENGTH
        },
        "vector_index_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": MAX_PARAMETER_LENGTH
        },
        "vrag_preamble": {
            "type": "string",
            "maxLength": 1000
        },
        "llm_model": {
            "type": "string",
            "enum": ["gpt-4o", "gpt-4o-mini"]
        },
        "user_id": {
            "type": "string",
            "maxLength": MAX_USER_NAME_LENGTH
        },
        "vrag_version": {
            "type": "string",
            "maxLength": MAX_PARAMETER_LENGTH
        },
        "num_chunks": {
            "type": "integer",
            "maximum": MAX_NUM_CHUNKS  # don't apply min number of chunks
        }
    },
    "additionalProperties": False
}
TEST_REQUESTS_VRAG_LLM = {
    "clean_requests": [
        {   
            "description": "Complete request with all optional fields",
            "request": {
                "user_question": "What is David Deutsch's view on artificial intelligence?",
                "vector_index_name": "dd-transcripts-vrag-80f-20240727",
                "vrag_preamble": "Given your knowledge of David Deutsch and his philosophy of deep optimism, as well as the QUOTED TEXT from Deutsch below, answer the USER QUESTION.",
                "num_chunks": 5,
                "llm_model": "gpt-4o-mini",
                "user_id": "test_user",
                "vrag_version": "1.0"
            }
        },
        # {   
        #     "description": "Test with minimum required fields",
        #     "request": {
        #         "user_question": "What is David Deutsch's view on artificial intelligence?",
        #         "vector_index_name": "dd-transcripts-vrag-80f-20240727"
        #     }
        # }
    ],

    "schema_invalid_requests": [
        {   
            "description": "Invalid llm_model value not in enum list",
            "request": {
                "llm_model": "gpt-3"
            }
        },
        # {   
        #     "description": "User question exceeds maximum length",
        #     "request": {
        #         "user_question": "A" * (MAX_QUESTION_LENGTH + 1)
        #     }
        # },
        # {   
        #     "description": "Invalid num_chunks value exceeding maximum",
        #     "request": {
        #         "num_chunks": MAX_NUM_CHUNKS + 1
        #     }
        # },
        # {   
        #     "description": "Empty required field",
        #     "request": {
        #         "user_question": ""
        #     }
        # },
        # {   
        #     "description": "Invalid data type for num_chunks - should be integer",
        #     "request": {
        #         "num_chunks": "5"
        #     }
        # }
    ],

    "function_invalid_requests": [
        {   
            "description": "Missing required user_question field",
            "request": {
                "user_question": REMOVE_FIELD
            }
        },
        # {   
        #     "description": "Missing required vector_index_name field",
        #     "request": {
        #         "vector_index_name": REMOVE_FIELD
        #     }
        # },
        # {   
        #     "description": "Invalid data type for user_question",
        #     "request": {
        #         "user_question": ["not", "a", "string"]
        #     }
        # }
    ]
}


# Define the mapping of Lambda functions to their suffix names
LAMBDA_GLOBALS_MAPPING = {
    #'deepgram-callback': 'DEEPGRAM_CALLBACK',  # No API Gateway Validation 12-21 RT
    'hash-store': 'HASH_STORE',
    'hmac-hash': 'HMAC_HASH',
    'qrag-llm': 'QRAG_LLM',
    'qrag-routing': 'QRAG_ROUTING',
    'send-email': 'SEND_EMAIL',
    'vrag-llm': 'VRAG_LLM'
}
LAMBDA_APIS_MAPPING = {
    'deepgram-callback': 'lsehufc3n2',
    'hash-store': 'wd3rapoqy7',
    'hmac-hash': 'xusv8bpl49', 
    'qrag-llm': 'sz901mb96d',
    'qrag-routing': 'us05oglu51',
    'send-email': 'lvyznjx395',
    'vrag-llm': 'n5yjgn8jak'
}
LAMBDA_JWT_REQUIRED = {
    'deepgram-callback': False,
    'hash-store': False,
    'hmac-hash': False,
    'qrag-llm': True,
    'qrag-routing': True,
    'send-email': True,
    'vrag-llm': True
}

def get_lambda_configurations():
    """
    Gather all Lambda-related global variables based on naming conventions.

    :return configurations: dict, dict of dicts with all configurations.
    """
    all_globals = globals()
    configurations = {}
    
    for lambda_name, suffix in LAMBDA_GLOBALS_MAPPING.items():
        # Look for API_ENDPOINT_{SUFFIX}, SCHEMA_{SUFFIX}, TEST_REQUESTS_{SUFFIX}
        endpoint_var = f"API_ENDPOINT_{suffix}"
        schema_var = f"SCHEMA_{suffix}"
        test_requests_var = f"TEST_REQUESTS_{suffix}"
        
        # Only include if all required variables exist
        if all(var in all_globals for var in [endpoint_var, schema_var, test_requests_var]):
            configurations[lambda_name] = {
                'endpoint': all_globals[endpoint_var],
                'schema': all_globals[schema_var],
                'test_requests': all_globals[test_requests_var]
            }
        else:
            print(f"Warning: Missing configuration variables for {lambda_name}")
            missing = [var for var in [endpoint_var, schema_var, test_requests_var] 
                      if var not in all_globals]
            print(f"  Missing variables: {missing}")
    
    return configurations
def create_complete_request(partial_request, template_request):
    """
    Create a complete request by filling in missing fields from a template.
    Special handling: If a field's value is REMOVE_FIELD, remove it from the final request.
    
    :param partial_request: dict, the request with some fields specified.
    :param template_request: dict, complete request to use as a template for missing fields.
    :return complete_request: dict, complete request with all fields, using template values for missing fields.
    """
    def update_dict(template, partial):
        """Recursively update template dict with partial dict values."""
        result = template.copy()
        for key, value in partial.items():
            if value == REMOVE_FIELD:
                result.pop(key, None)
            elif isinstance(value, dict) and key in template and isinstance(template[key], dict):
                # Recursively update nested dictionaries
                result[key] = update_dict(template[key], value)
            else:
                result[key] = value
        return result

    # Check if either has description/request structure
    partial_has_structure = isinstance(partial_request, dict) and set(partial_request.keys()) == {"description", "request"}
    template_has_structure = isinstance(template_request, dict) and set(template_request.keys()) == {"description", "request"}
    
    # If one has structure and other doesn't, that's an error
    if partial_has_structure != template_has_structure:
        raise ValueError("Both partial_request and template_request must have the same structure (either both with description/request or both without)")
    
    if partial_has_structure:
        # Process only the request portion
        complete_request_data = update_dict(template_request["request"], partial_request["request"])
        return {
            "description": partial_request["description"],
            "request": complete_request_data
        }
    else:
        # Original behavior for non-structured requests
        return update_dict(template_request, partial_request)
def mtest_create_complete_request():
    pass
#if __name__ == "__main__":
    template_request = TEST_REQUESTS_QRAG_LLM['clean_requests'][0]
    partial_request = TEST_REQUESTS_QRAG_LLM['schema_invalid_requests'][0]
    complete_request = create_complete_request(partial_request, template_request)
    expected_request = {   
            "description": "Invalid llm_model value - Not in enum list",  # Use partial request's description
            "request": {
                "metadata": {
                    "timestamp": "2024-06-13T11:46:33.651753",
                    "user_id": "default", 
                    "vector_index_name": "deutsch-transcript-qrag-78f-20240926",
                    "bot_version": "1.0",
                    "llm_model": "gpt-3",
                    "routes_info": {
                        "routes_flow_name": "3 routes, sim-star double, separate prompts",
                        "upper_sim_bound": 0.9,
                        "lower_sim_bound": 0.3,
                        "max_sim": "0.216",
                        "max_stars": 5,
                        "routes_dict_content": {
                            "routes_dict_name": "ROUTES_DICT_DEUTSCH_V3"
                        }
                    }
                },
                "content": {
                    "user_question": "What should I eat for lunch?",
                    "route_preamble": "Your question is not addressed in David Deutsch's interviews.",
                    "quoted_qa": "",
                    "ai_answer": "WAITING FOR LLM RESPONSE",
                    "chunks": {
                        "max_sim": "0.216",
                        "max_stars": 5,
                        "chunks": []
                    }
                }
            }
    }
    if complete_request == expected_request:
        print("Complete request matches expected request - TEST PASSES!!")
    else:
        print("Complete request does not match expected request - TEST FAILS!!")
        print("Complete Request:")
        print(json.dumps(complete_request, indent=4))
        print("Expected Request:")
        print(json.dumps(expected_request, indent=4))

#lambda_function='deepgram-callback'  
#lambda_function='hmac-hash'      # No JWT - PASS 12-21 0540
#lambda_function='hash-store'     # No JWT - PASS 12-21 0540
#lambda_function='send-email'     # JWT - PASS 12-21 0723
#lambda_function='qrag-routing'   # JWT - PASS 12-21 0540
lambda_function='qrag-llm'       # JWT - PASS 12-21 0642
#lambda_function='vrag-llm'       # JWT - PASS 12-21 0717
all_lambdas = ['deepgram-callback', 'hmac-hash', 'hash-store', 'send-email', 'qrag-routing', 'qrag-llm', 'vrag-llm']

def test_lambda_requests(lambda_function, stage='dev', direct_lambda=True, with_gateway=True, debug_prompt=False, output_file="web/test_back-end_validation.md", jwt_token=None):
    """
    Test requests for any Lambda function both directly and through API Gateway.

    :param lambda_function: str, base name of the Lambda function (e.g., 'hmac-hash').
    :param stage: str, deployment stage ('dev', 'prod', etc.).
    :param direct_lambda: bool, whether to test direct Lambda invocation.
    :param with_gateway: bool, whether to test through API Gateway.
    :param debug_prompt: bool, whether to prompt user to continue after each request.
    :param output_file: str, path to the output markdown file.
    :param jwt_token: str, optional JWT token for authenticated endpoints.
    :return: dict, test results.
    """
    # Create StringIO object to capture output
    from io import StringIO
    import sys
    output_buffer = StringIO()
    original_stdout = sys.stdout
    sys.stdout = output_buffer

    def write_to_both(message):
        """Helper function to write to both file and terminal"""
        output_buffer.write(message + "\n")
        sys.stdout = original_stdout
        print(message)
        sys.stdout = output_buffer

    # Validate that at least one testing path is enabled
    if not (direct_lambda or with_gateway):
        raise ValueError("At least one testing path must be enabled. "
                       "Set either direct_lambda=True or with_gateway=True")
    
    # Get all Lambda configurations
    lambda_configs = get_lambda_configurations()
    
    # Get AWS Lambda name with stage
    aws_lambda_name = f"{lambda_function}-{stage}"
    
    # Validate lambda_function exists in configurations
    if lambda_function not in lambda_configs:
        raise ValueError(f"No configuration found for Lambda function: {lambda_function}")
    
    # Get configuration for this specific Lambda
    config = lambda_configs[lambda_function]
    api_endpoint = config['endpoint']
    schema = config['schema']
    test_requests = config['test_requests']
    
    # Get template request from first clean request
    if not test_requests.get('clean_requests'):
        raise ValueError(f"No clean requests found for {lambda_function}")
    template_request = test_requests['clean_requests'][0]
    
    lambda_client = boto3.client('lambda')
    
    def invoke_lambda(request_data):
        """Direct Lambda invocation that simulates API Gateway event."""
        try:
            # Extract route from API endpoint URL
            api_endpoint_parts = api_endpoint.split('/')
            route = '/' + api_endpoint_parts[-1]  # Get the last part of the URL
            
            # Build headers with optional JWT
            headers = {
                "Content-Type": "application/json",
                "origin": "https://www.focusonfoundations.org"
            }
            if jwt_token:
                headers["Authorization"] = f"Bearer {jwt_token}"

            # Build a mock API Gateway event
            lambda_payload = {
                "resource": route,
                "path": route,
                "httpMethod": "POST",
                "headers": headers,
                "multiValueHeaders": {
                    "Content-Type": ["application/json"]
                },
                "queryStringParameters": None,
                "multiValueQueryStringParameters": None,
                "pathParameters": None,
                "stageVariables": None,
                "requestContext": {
                    "resourcePath": route,
                    "httpMethod": "POST",
                    "stage": stage,
                    "identity": {
                        "sourceIp": "127.0.0.1",
                        "userAgent": "custom-agent"
                    }
                },
                "body": json.dumps(request_data),
                "isBase64Encoded": False
            }

            response = lambda_client.invoke(
                FunctionName=aws_lambda_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(lambda_payload)
            )

            # Parse and debug the response
            response_payload = json.loads(response['Payload'].read())
            print("Lambda response payload:", json.dumps(response_payload, indent=2))
            
            return response_payload

        except Exception as e:
            print(f"Error invoking Lambda: {e}")
            return {"error": str(e)}

    def invoke_gateway(request_data):
        """API Gateway invocation"""
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            # Debug print
            print("Request being sent to API Gateway:")
            print(json.dumps(request_data, indent=2))
            
            if jwt_token:
                headers['Authorization'] = f'Bearer {jwt_token}'

            response = requests.post(
                api_endpoint,
                json=request_data,
                headers=headers,
                timeout=180  # Changed from 10 to 180 seconds
            )
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"error": f"Invalid JSON response: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def check_lambda_success(lambda_result):
        """Check if Lambda invocation was successful"""
        try:
            # Check if it's a direct Lambda response (contains statusCode and body)
            if "statusCode" in lambda_result:
                if lambda_result["statusCode"] != 200:
                    return False
                # Parse the body if it's a string
                body = (json.loads(lambda_result["body"]) 
                       if isinstance(lambda_result["body"], str) 
                       else lambda_result["body"])
                return body.get("status") == "Success"
            # Otherwise check if it's already parsed response
            return lambda_result.get("status") == "Success"
        except Exception as e:
            print(f"Error checking Lambda success: {e}")
            return False

    def check_gateway_success(gateway_result):
        """Check if Gateway invocation was successful"""
        try:
            return gateway_result.get("status") == "Success"
        except Exception as e:
            print(f"Error checking Gateway success: {e}")
            return False

    # Initialize results dictionary with only the categories present in test_requests
    results = {}
    for category in test_requests.keys():
        results[category] = []

    # Test each category that exists in test_requests
    now_datetime = get_current_datetime_filefriendly()
    write_to_both(f"\n\n## ====== Testing {lambda_function}  {now_datetime} ======")
    for category, request_list in test_requests.items():
        write_to_both(f"\n\n## ====== {category} for {lambda_function} ======")
        for i, partial_request in enumerate(request_list, 1):
            # Skip first clean request since it's our template
            if category == 'clean_requests' and i == 1:
                complete_request = partial_request
            else:
                complete_request = create_complete_request(partial_request, template_request)
            
            # Extract description if present, otherwise empty string
            description = ""
            if isinstance(partial_request, dict) and "description" in partial_request:
                description = partial_request["description"]
            elif isinstance(complete_request, dict) and "description" in complete_request:
                description = complete_request["description"]
                
            write_to_both(f"\n## {category:<25}Request {i}: {description}")
            write_to_both("Original: " + json.dumps(partial_request, indent=2))
            write_to_both("Complete: " + json.dumps(complete_request, indent=2))
            
            # Extract just the request data for the API calls
            request_data = complete_request.get("request", complete_request)
            
            lambda_result = None
            gateway_result = None
            
            if direct_lambda:
                write_to_both("\n### DIRECT LAMBDA INVOCATION")
                lambda_result = invoke_lambda(request_data)
                write_to_both("Result:")
                write_to_both(json.dumps(lambda_result, indent=2))
            
            if with_gateway:
                write_to_both("\n### API GATEWAY INVOCATION")
                gateway_result = invoke_gateway(request_data)
                write_to_both("Result:")
                write_to_both(json.dumps(gateway_result, indent=2))
            
            # Store results with success/error status
            results[category].append({
                "request": create_complete_request(partial_request, template_request),
                "lambda_result": {
                    "response": lambda_result,
                    "success": check_lambda_success(lambda_result) if lambda_result else None
                } if direct_lambda else None,
                "gateway_result": {
                    "response": gateway_result,
                    "success": check_gateway_success(gateway_result) if gateway_result else None
                } if with_gateway else None
            })
            
            if debug_prompt:
                user_continue_response = input("Press any key to continue or 'x' to exit...").strip().lower()
                if user_continue_response == 'x':
                    return results
            else:
                sleep(0.5)  # Rate limiting

    def summarize_results(results):
        """Summarize test results and expectations"""
        # Initialize summary
        summary = {category: {
            "total": 0,
            "lambda": {"success": 0, "error": 0},
            "gateway": {"success": 0, "error": 0}
        } for category in results.keys()}
        
        total_tests = 0
        failed_tests = 0
        
        write_to_both(f"\n## ===== API Gateway Validation Test Summary {lambda_function} =====")
        
        for category, requests in results.items():
            summary[category]["total"] = len(requests)
            total_tests += len(requests) * 2
            
            write_to_both(f"\n{category} ({summary[category]['total']} tests):")
            
            # Define expected behavior for each category
            expected_behaviors = {
                "clean_requests": {"lambda": "SUCCESS", "gateway": "SUCCESS"},
                "schema_invalid_requests": {"lambda": "SUCCESS", "gateway": "ERROR"},
                "function_invalid_requests": {"lambda": "ERROR", "gateway": "ERROR"}
            }
            
            # Get expected behavior for this category
            expected = expected_behaviors[category]
            
            # Lambda Results
            expected_lambda = "SUCCESS" if "clean" in category else "ERROR" if "function_invalid" in category else "SUCCESS"
            lambda_stats = summary[category]["lambda"]
            
            # Track successes/errors for summary stats
            for i, result in enumerate(requests, 1):
                if result["lambda_result"]:
                    if result["lambda_result"]["success"]:
                        lambda_stats["success"] += 1
                    else:
                        lambda_stats["error"] += 1
                    
                    # Compare against expected behavior for failure count
                    if ((result["lambda_result"]["success"] and expected["lambda"] == "ERROR") or 
                        (not result["lambda_result"]["success"] and expected["lambda"] == "SUCCESS")):
                        failed_tests += 1
                
                if result["gateway_result"]:
                    if result["gateway_result"]["success"]:
                        summary[category]["gateway"]["success"] += 1
                    else:
                        summary[category]["gateway"]["error"] += 1
                    
                    # Compare against expected behavior for failure count
                    if ((result["gateway_result"]["success"] and expected["gateway"] == "ERROR") or 
                        (not result["gateway_result"]["success"] and expected["gateway"] == "SUCCESS")):
                        failed_tests += 1
            
            # Display Lambda results
            lambda_passed = (
                (expected_lambda == "SUCCESS" and lambda_stats["success"] == summary[category]["total"]) or
                (expected_lambda == "ERROR" and lambda_stats["error"] == summary[category]["total"])
            )
            write_to_both(f"  Lambda Results: (expected {expected_lambda})  {'✓' if lambda_passed else '✗'}")
            for i, result in enumerate(requests, 1):
                if result["lambda_result"]:
                    status = "SUCCESS" if result["lambda_result"]["success"] else "ERROR"
                    write_to_both(f"    test {i}:  {status}")
                else:
                    write_to_both(f"    test {i}:  SKIPPED")
            
            # Display Gateway results
            expected_gateway = "SUCCESS" if "clean" in category else "ERROR"
            gateway_stats = summary[category]["gateway"]
            gateway_passed = (
                (expected_gateway == "SUCCESS" and gateway_stats["success"] == summary[category]["total"]) or
                (expected_gateway == "ERROR" and gateway_stats["error"] == summary[category]["total"])
            )
            write_to_both(f"  Gateway Results: (expected {expected_gateway})  {'✓' if gateway_passed else '✗'}")
            for i, result in enumerate(requests, 1):
                if result["gateway_result"]:
                    status = "SUCCESS" if result["gateway_result"]["success"] else "ERROR"
                    write_to_both(f"    test {i}:  {status}")
                else:
                    write_to_both(f"    test {i}:  SKIPPED")
        
        # Print final summary
        passed_tests = total_tests - failed_tests
        write_to_both(f"\nTest Results: {passed_tests} passed, {failed_tests} failed  {'✓' if failed_tests == 0 else '✗'}")

        return summary

    try:
        # Run tests and get summary
        summary = summarize_results(results)

        # Write captured output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("## API Gateway Validation Test Results\n\n")
            f.write(output_buffer.getvalue())
        
        return results

    finally:
        sys.stdout = original_stdout
        output_buffer.close()
def mrun_test_lambda_requests():
    pass
if __name__ == "__main__":
    jwt_token = None
    if LAMBDA_JWT_REQUIRED.get(lambda_function, False):
        jwt_token = JWT_TEST

    results = test_lambda_requests(lambda_function, direct_lambda=True, with_gateway=True, jwt_token=jwt_token)
    #print(colored("TESTING the green color", "green"))

def check_validation_setup(lambda_function, http_method='POST', verbose=False):
    """
    Check if API Gateway validation is set up for a Lambda function.

    :param lambda_function: str, name of the API Gateway
    :param http_method: str, HTTP method to check
    :param verbose: bool, if True prints entire method configuration
    :return validation_exists: bool, True if validation is set up, False otherwise
    """
    api_client = boto3.client('apigateway')
    rest_api_id, resource_id = get_api_gateway_ids(lambda_function, http_method, verbose=verbose)
    
    # Get method configuration
    method = api_client.get_method(
        restApiId=rest_api_id,
        resourceId=resource_id,
        httpMethod='POST'
    )
    
    if verbose:
        print("Method configuration:")
        print(json.dumps(method, indent=2))
    
    validator_id = method.get('requestValidatorId', 'None')
    model_name = method.get('requestModels', {}).get('application/json', 'None')
    
    print(f"\nAPI Gateway validation setup for {lambda_function}:")
    print(f"  Validator ID: {validator_id}")
    print(f"  Request Model: {model_name}")
    
    # Return True if both validator ID and model name exist and are not 'None'
    return validator_id != 'None' and model_name != 'None'
def mrun_check_validation_setup():
    pass
#if __name__ == "__main__":
    validation_exists = check_validation_setup(lambda_function)
    print(f"API Gateway validation exists for {lambda_function}: {validation_exists}")
    
    # OR TO CHECK ALL LAMBDAS:
    # for lambda_function in all_lambdas:
    #     validation_exists = check_validation_setup(lambda_function)
    #     print(f"API Gateway validation exists for {lambda_function}: {validation_exists}")

def create_request_model(rest_api_id, model_name, schema, description=None, prompt_overwrite=True):
    """
    Create or update a request model in API Gateway for request validation.
    
    :param rest_api_id: ID of the REST API
    :param model_name: Name for the model (e.g., 'QRAGRoutingRequest')
    :param schema: JSON schema as a dictionary
    :param description: Optional description of the model
    :param prompt_overwrite: If True, prompts user when model exists; if False, skips update
    :return: Model ID if successful, None otherwise
    """
    api_client = boto3.client('apigateway')
    
    try:
        # Check if model already exists
        try:
            existing_model = api_client.get_model(
                restApiId=rest_api_id,
                modelName=model_name
            )
            if prompt_overwrite:
                response = input(f"\nModel '{model_name}' already exists. Update it? (y/n): ")
                if response.lower() != 'y':
                    print("Skipping model update.")
                    return existing_model['id']
                    
                # Update existing model
                try:
                    api_client.update_model(
                        restApiId=rest_api_id,
                        modelName=model_name,
                        patchOperations=[
                            {
                                'op': 'replace',
                                'path': '/schema',
                                'value': json.dumps(schema)
                            },
                            {
                                'op': 'replace',
                                'path': '/description',
                                'value': description or f'Request validation model for {model_name}'
                            }
                        ]
                    )
                    print(f"Updated existing model '{model_name}'")
                    return existing_model['id']
                except ClientError as e:
                    print(f"Error updating existing model: {e}")
                    return None
            else:
                print(f"Model '{model_name}' already exists, skipping update.")
                return existing_model['id']
                
        except ClientError as e:
            if not 'NotFoundException' in str(e):
                raise
        
        # Create new model if it doesn't exist
        response = api_client.create_model(
            restApiId=rest_api_id,
            name=model_name,
            description=description or f'Request validation model for {model_name}',
            contentType='application/json',
            schema=json.dumps(schema)
        )
        print(f"Created model '{model_name}' for API {rest_api_id}")
        return response['id']
        
    except ClientError as e:
        print(f"Error creating model: {e}")
        return None
def update_method_validation(rest_api_id, resource_id, http_method, model_name):
    """
    Update an API method to enable request validation with the specified model.
    
    :param rest_api_id: ID of the REST API
    :param resource_id: ID of the API resource
    :param http_method: HTTP method (e.g., 'POST')
    :param model_name: Name of the request model to use
    :return: True if successful, False otherwise
    """
    api_client = boto3.client('apigateway')
    
    try:
        # First try to get existing validator
        validator_id = None
        try:
            validators = api_client.get_request_validators(restApiId=rest_api_id)
            for validator in validators.get('items', []):
                if validator['validateRequestBody']:
                    validator_id = validator['id']
                    print(f"Found existing request validator: {validator['name']}")
                    break
        except ClientError:
            pass

        # Create validator only if none exists
        if not validator_id:
            try:
                validator = api_client.create_request_validator(
                    restApiId=rest_api_id,
                    name='validate-body',
                    validateRequestBody=True,
                    validateRequestParameters=False
                )
                validator_id = validator['id']
                print("Created new request validator")
            except ClientError as e:
                print(f"Error creating validator: {e}")
                return False

        # First, update the method to ensure Content-Type is set up
        try:
            api_client.update_method(
                restApiId=rest_api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                patchOperations=[
                    {
                        'op': 'add',
                        'path': '/requestParameters/method.request.header.Content-Type',
                        'value': 'false'  # false means optional
                    }
                ]
            )
            print("Added Content-Type header parameter")
        except ClientError as e:
            if 'ConflictException' in str(e):
                print("Content-Type header parameter already exists")
            else:
                print(f"Warning: Could not update Content-Type header: {e}")

        # Now update the method with validator and model
        api_client.update_method(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/requestValidatorId',
                    'value': validator_id
                },
                {
                    'op': 'add',
                    'path': '/requestModels/application~1json',
                    'value': model_name
                }
            ]
        )
        print(f"Enabled request validation for {http_method} method using model '{model_name}'")
        return True
    except ClientError as e:
        print(f"Error updating method validation: {e}")
        return False
def setup_request_validation(lambda_function, http_method='POST'):
    """
    Set up request validation for an API Gateway endpoint.
    
    :param lambda_function: Name of the API Gateway
    :param http_method: HTTP method to validate
    :return: True if successful, False otherwise
    """
    # Get schema for this API using the LAMBDA_GLOBALS_MAPPING
    suffix = LAMBDA_GLOBALS_MAPPING.get(lambda_function)
    schema = globals().get(f"SCHEMA_{suffix}")
    if not schema:
        print(f"No schema defined for API: {lambda_function}")
        return False
    
    # Get API Gateway IDs
    rest_api_id, resource_id = get_api_gateway_ids(lambda_function, http_method)
    if not rest_api_id or not resource_id:
        print(f"Failed to get API Gateway IDs for {lambda_function}")
        return False
    
    # Create request model
    model_name = f"{lambda_function.replace('-', '')}Model"
    model_id = create_request_model(rest_api_id, model_name, schema)
    if not model_id:
        return False
    
    # Update method to use validation
    if not update_method_validation(rest_api_id, resource_id, http_method, model_name):
        return False
    
    # Create deployment to apply changes
    if not create_deployment(rest_api_id):
        return False
    
    print(f"Successfully set up request validation for {lambda_function}")
    return True
def mrun_setup_request_validation():
    pass
#if __name__ == "__main__":
    check_validation_setup(lambda_function)
    if setup_request_validation(lambda_function):
        user_continue_response = input("\n*** WAIT 30 SECONDS FOR CHANGE TO TAKE EFFECT *** - Then Press any key to continue or 'x' to exit...").strip().lower()
        if user_continue_response != 'x':
            # Use the same JWT logic as mrun_test_lambda_requests
            jwt_token = None
            if LAMBDA_JWT_REQUIRED.get(lambda_function, False):
                jwt_token = JWT_TEST
                
            test_lambda_requests(
                lambda_function, 
                direct_lambda=True, 
                with_gateway=True, 
                jwt_token=jwt_token
            )

# TODO: Not tested yet
def toggle_request_validation(lambda_function, http_method='POST'):
    """
    Toggle request validation on/off for an API Gateway endpoint and report the state.
    
    :param lambda_function: str, name of the API Gateway.
    :param http_method: str, HTTP method to modify.
    :return success: bool, True if successful, False otherwise.
    """
    api_client = boto3.client('apigateway')
    
    try:
        # Get API Gateway IDs
        rest_api_id, resource_id = get_api_gateway_ids(lambda_function, http_method)
        if not rest_api_id or not resource_id:
            print(f"Failed to get API Gateway IDs for {lambda_function}")
            return False
            
        # Get current method configuration
        method = api_client.get_method(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod=http_method
        )
        
        # Check if validation is currently enabled
        validation_enabled = ('requestValidatorId' in method and 
                            'requestModels' in method and 
                            'application/json' in method.get('requestModels', {}))
        
        if validation_enabled:
            # Disable validation by removing validator and model references
            patch_operations = [
                {
                    'op': 'remove',
                    'path': '/requestValidatorId'
                },
                {
                    'op': 'remove', 
                    'path': '/requestModels/application~1json'
                }
            ]
            
            api_client.update_method(
                restApiId=rest_api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                patchOperations=patch_operations
            )
            
            print(f"Request validation for {lambda_function} is now: DISABLED")
        else:
            # Get validator ID
            validators = api_client.get_request_validators(restApiId=rest_api_id)
            validator_id = next((v['id'] for v in validators.get('items', []) 
                              if v['validateRequestBody']), None)
            
            if not validator_id:
                print("No request validator found. Please run setup_request_validation first.")
                return False
                
            # Enable validation by adding validator and model references
            api_client.update_method(
                restApiId=rest_api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                patchOperations=[
                    {
                        'op': 'replace',
                        'path': '/requestValidatorId',
                        'value': validator_id
                    },
                    {
                        'op': 'replace',
                        'path': '/requestModels/application~1json',
                        'value': f"{lambda_function.replace('-', '')}Model"
                    }
                ]
            )
            print(f"Request validation for {lambda_function} is now: ENABLED")
        
        # Create deployment to apply changes
        if not create_deployment(rest_api_id):
            return False
            
        return True
        
    except ClientError as e:
        print(f"Error toggling validation: {e}")
        return False
def mrun_toggle_request_validation():
    pass
#if __name__ == "__main__":
    lambda_function = "hash-store"
    #toggle_request_validation(lambda_function)
    #test_lambda_requests(lambda_function, direct_lambda=True, with_gateway=True)

'''
IMPORTANT: the chalice deploy script: web/aws_chalice/chalicelib_mirror_deploy.sh
will read whether the API Gateway validation is enabled or disabled
then it will preserve that state by rerunning the setup_request_validation if enabled.
'''

# aws apigateway delete-model --rest-api-id xusv8bpl49 --model-name hmachashModel

# ===== END OF FILE primary/aws-valid.py =====
