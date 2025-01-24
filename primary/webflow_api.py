# ===== START OF FILE secondary/webflow.py =====
# Library of functions and execution code to do Webflow tasks

import os
from dotenv import load_dotenv
import markdown
from webflow.client import Webflow
import requests

from primary.fileops import *

# ---API KEYS AND SECRETS---
load_dotenv(override=True)  # Load environment variables from .env file
WEBFLOW_API_KEY_FOF_ALL = os.environ["WEBFLOW_API_KEY_FOF_ALL"]

# ---START OF SYNCED CODE--- only code below will be synchronized with chalicelib.

# Initialize the Webflow API client
client = Webflow(access_token=WEBFLOW_API_KEY_FOF_ALL)

### WEBFLOW SITES
SITE_ID_FOF = "66f32336260d050c6e0fffa0"
def mrun_print_site_info():
    pass
#if __name__ == "__main__":
    cur_site_id = SITE_ID_FOF
    site_info = client.sites.get(site_id=cur_site_id)
    print(f"Site Info for site_id: {cur_site_id}")
    print(f"ID: {site_info.id}")
    print(f"Workspace ID: {site_info.workspace_id}")
    print(f"Created On: {site_info.created_on}")
    print(f"Display Name: {site_info.display_name}")
    print(f"Short Name: {site_info.short_name}")
    print(f"Last Published: {site_info.last_published}")
    print(f"Last Updated: {site_info.last_updated}")
    print(f"Preview URL: {site_info.preview_url}")
    print(f"Time Zone: {site_info.time_zone}")
    print(f"Custom Domains: {site_info.custom_domains}")

DEUTSCH_INTERVIEWS_VRBS_ID = "6711b684a9e995b7c0f06e17"
FDA_C19_TOWNHALLS_ID = "6780532037b7b191793c3544"

### WEBFLOW CMS
def webflow_cms_get_collection_details(collection_id, debug=False, verbose=True):
    """
    Get the full details of a collection from its ID.

    :param collection_id: str, the ID of the Webflow CMS collection.
    :param debug: bool, if True prints raw API response details.
    :param verbose: bool, if True prints formatted collection details.
    :return: dict, a dictionary containing the collection details or None if an error occurs.
    """
    try:
        # Construct the URL
        url = f"https://api.webflow.com/v2/collections/{collection_id}"
        
        # Set up headers
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        
        if debug: 
            print("Raw API response:")
            print(f"Status Code: {response.status_code}")
            print("Headers:")
            print(response.headers)
            print("Content:")
            print(response.text)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        collection_details = {
            "id": data.get("id"),
            "name": data.get("displayName"),
            "slug": data.get("slug"),
            "singularName": data.get("singularName"),
            "fields": data.get("fields", []),
            "createdOn": data.get("createdOn"),
            "lastUpdated": data.get("lastUpdated")
        }

        if verbose:
            print(f"Collection Details for {collection_details['name']}:")
            for key, value in collection_details.items():
                if key != "fields":
                    print(f"{key}: {value}")
                else:
                    filtered_fields = [f for f in value if f.get('slug') not in ['name', 'slug']]
                    print(f"Number of fields: {len(filtered_fields)}")
                    print("Fields:")
                    # Print header row
                    print(f"{'Field Name':<25} {'Type':<15} {'Status':<15} {'Slug'}")
                    print("-" * 80)  # Separator line
                    for field in filtered_fields:
                        field_type = field.get('type', 'Unknown')
                        field_name = field.get('displayName', 'Unnamed')
                        field_slug = field.get('slug', 'no-slug')
                        field_required = "Required" if field.get('isRequired') else "Optional"
                        print(f"\033[33m{field_name:<25}\033[0m {field_type:<15} {field_required:<15} {field_slug}")
                    print("-" * 80)  # Separator line

        return collection_details
    except requests.exceptions.RequestException as e:
        print(f"Error fetching collection details: {str(e)}")
        return None

def mrun_get_collection_details():
    pass
#if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    collection_details = webflow_cms_get_collection_details(cur_collection_id, verbose=True)

def webflow_cms_import_heading(collection_id, file_path, heading):
    """
    Imports a markdown heading and its content into a Webflow CMS collection.

    :param collection_id: str, the ID of the Webflow CMS collection to import into.
    :param file_path: str, the path to the markdown file to extract content from.
    :param heading: str, the heading to extract from the markdown file, including '#' characters.
    :return created_item_id: str, the ID of the newly created Webflow CMS item or None if heading not found.
    """
    # Get the markdown content for the specified heading
    markdown_text = get_heading(file_path, heading)

    if markdown_text is None:
        print(f"Heading '{heading}' not found in file '{file_path}'")
        return None

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text)

    # Create a title for the item based on the heading
    item_title = os.path.splitext(os.path.basename(file_path))[0] + '_' + heading.strip('#').strip()
    item_slug = item_title.lower().replace(' ', '-')

    new_item = {
        'fields': {
            'name': item_title,  # Required name field
            'slug': item_slug,   # Required slug field
            'transcript-vrb': html_content  # This is your custom rich text field
        }
    }

    # Create the item in the Webflow collection
    created_item = client.collections.create_item(collection_id=collection_id, data=new_item)
    print(f"Created new item with ID: {created_item['_id']}")

    return created_item['_id']

def webflow_cms_list_items(collection_id, include_archived=True, verbose=False):
    """
    Lists all items in a Webflow collection.

    :param collection_id: str, the ID of the Webflow CMS collection
    :param include_archived: bool, whether to include archived/trashed items
    :param verbose: bool, whether to print API response details
    :return: list of items or None if the request fails
    """
    try:
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        url = f'https://api.webflow.com/v2/collections/{collection_id}/items'
        if include_archived:
            url += '?archived=true'
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            items = response.json()['items']
            if verbose:
                for item in items:
                    archived_status = " (ARCHIVED)" if item.get('archived', False) else ""
                    print(f"ID: {item['id']}, Name: {item['fieldData'].get('name', 'N/A')}, "
                          f"Slug: {item['fieldData'].get('slug', 'N/A')}{archived_status}")
                print(f"\nTotal items: {len(items)}")
            return items
        else:
            if verbose:
                print(colored(f"Error listing items. Status code: {response.status_code}", "red"))
                print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        if verbose:
            print(colored(f"Error listing items: {str(e)}", "red"))
        return None
def mrun_webflow_cms_list_items():
    pass
if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    items = webflow_cms_list_items(cur_collection_id, verbose=True)

def webflow_cms_import_transcript_and_qa(collection_id, transcript_file_path, qa_suffix='_qa-qonly', verbose=False):
    """
    Imports a transcript and its associated URLs into a Webflow CMS collection.

    :param collection_id: str, the ID of the Webflow CMS collection to import into.
    :param transcript_file_path: str, the path to the markdown file containing the transcript.
    :param qa_suffix: str, unused parameter kept for backwards compatibility.
    :param verbose: bool, whether to print truncated field values.
    :return created_item_id: str, the ID of the newly created Webflow CMS item or None if error occurs.
    """
    # Get URLs and transcript text - extract just the URL string if it's a tuple
    pdf_url = read_metadata_field_from_file(transcript_file_path, 'link pdf')
    pdf_url = pdf_url[1] if isinstance(pdf_url, tuple) else pdf_url
    
    youtube_url = read_metadata_field_from_file(transcript_file_path, 'link youtube')
    youtube_url = youtube_url[1] if isinstance(youtube_url, tuple) else youtube_url
    
    #transcript_text = get_heading(transcript_file_path, '### transcript')
    transcript_text = 'This is dummy transcript text'
    
    if transcript_text is None:
        print(f"Transcript not found in file '{transcript_file_path}'")
        return None

    # Create a title and slug from the filename
    item_title = os.path.splitext(os.path.basename(transcript_file_path))[0]
    item_slug = item_title.lower().replace(' ', '-')

    # Restructure the data format to match v2 API requirements
    new_item = {
        'fieldData': {
            'name': item_title,
            'slug': item_slug,
            'md-mod-txt': transcript_text,
            'pdf-url': pdf_url if pdf_url else '',
            'youtube-url-3': youtube_url if youtube_url else ''
        }
    }

    if verbose:
        print("\nField values (truncated to 100 chars):")
        for field, value in new_item['fieldData'].items():
            truncated_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"{field}: {truncated_value}")

    try:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        # The v2 API expects a wrapper object with 'items' array
        request_body = {
            'items': [new_item]
        }
        
        response = requests.post(
            f'https://api.webflow.com/v2/collections/{collection_id}/items',
            headers=headers,
            json=request_body
        )
        
        if response.status_code == 200:
            created_item = response.json()
            print(f"Created new item with ID: {created_item['id']}")
            return created_item['id']
        else:
            print(f"Error creating item. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error creating item: {str(e)}")
        return None
def mrun_webflow_cms_import_transcript_and_qa():
    pass
#if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    transcript_file_path = 'data/floodlamp/reg/fda-townhalls/f5_fixnames/done_auto/2020-12-09_Virtual Town Hall 36_fixnames.md'
    webflow_cms_import_transcript_and_qa(cur_collection_id, transcript_file_path, verbose=True)
def webflow_cms_create_item(collection_id, field_data, collection_validation=True, verbose=False):
    """
    Creates a new item in a Webflow collection after validating the field data.

    :param collection_id: str, the ID of the Webflow CMS collection.
    :param field_data: dict, the data for all fields to be created.
    :param collection_validation: bool, whether to validate fields against collection schema
    :param verbose: bool, whether to print field validation and API response details.
    :return: str, the ID of the newly created item or None if validation/creation fails.
    """
    # Get collection details and validate fields only if collection_validation is True
    if collection_validation:
        collection_details = webflow_cms_get_collection_details(collection_id, verbose=False)
        if not collection_details:
            print("Failed to fetch collection details for validation")
            return None

        # Extract required fields from collection schema
        required_fields = {
            field.get('slug'): field.get('type') 
            for field in collection_details['fields'] 
            if field.get('isRequired')
        }
        
        # Validate required fields
        missing_fields = [field for field in required_fields.keys() if field not in field_data]
        if missing_fields:
            print(f"Error: Missing required fields: {', '.join(missing_fields)}")
            return None

    if verbose:
        print("\nField values (truncated to 100 chars):")
        for field, value in field_data.items():
            truncated_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"{field}: {truncated_value}")

    # Prepare request data
    new_item = {
        'fieldData': field_data
    }
    
    request_body = {
        'items': [new_item]
    }

    try:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        response = requests.post(
            f'https://api.webflow.com/v2/collections/{collection_id}/items',
            headers=headers,
            json=request_body
        )
        
        if response.status_code in [200, 202]:
            created_item = response.json()
            if verbose:
                print(colored(f"Successfully created item name: {created_item['items'][0]['fieldData']['name']}  ID: {created_item['items'][0]['id']}", "green"))
            return created_item['items'][0]['id']
        else:
            print(colored(f"Error creating item. Status code: {response.status_code}", "red"))
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(colored(f"Error creating item: {str(e)}", "red"))
        return None
def mtest_webflow_cms_create_item():
    pass
#if __name__ == "__main__":
    cur_collection_id = FDA_C19_TOWNHALLS_ID
    field_data = {
        'name': 'Test Item',
        'slug': 'test-item',
        'md-mod-txt': 'This is a test item',
        'pdf-url': 'https://example.com/test.pdf',
        'youtube-url-3': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    }
    webflow_cms_create_item(cur_collection_id, field_data, collection_validation=False, verbose=True)
def webflow_cms_update_item(collection_id, item_id, field_data, collection_validation=True, verbose=False):
    """
    Updates an existing item in a Webflow collection.

    :param collection_id: str, the ID of the Webflow CMS collection
    :param item_id: str, the ID of the item to update
    :param field_data: dict, the updated field data
    :param collection_validation: bool, whether to validate fields against collection schema
    :param verbose: bool, whether to print field validation and API response details
    :return: bool indicating success or failure
    """
    if collection_validation:
        collection_details = webflow_cms_get_collection_details(collection_id, verbose=False)
        if not collection_details:
            print("Failed to fetch collection details for validation")
            return False

    try:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {WEBFLOW_API_KEY_FOF_ALL}"
        }
        
        request_body = {
            "fieldData": field_data
        }
        
        response = requests.patch(
            f'https://api.webflow.com/v2/collections/{collection_id}/items/{item_id}',
            headers=headers,
            json=request_body
        )
        
        if response.status_code in [200, 202]:
            if verbose:
                print(f"Successfully updated item with ID: {item_id}")
            return True
        else:
            if verbose:
                print(f"Error updating item. Status code: {response.status_code}")
                print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        if verbose:
            print(f"Error updating item: {str(e)}")
        return False


# ===== END OF FILE secondary/webflow.py =====
