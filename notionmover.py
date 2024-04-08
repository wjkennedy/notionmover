import os
import requests
import re
from markdown import markdown
from base64 import b64encode

# Confluence API Setup
base_url = 'https://yoursite.atlassian.net/wiki'
username = 'you@example.com'
api_token = 'YOURTOKENHERE'
auth = b64encode(f"{username}:{api_token}".encode()).decode("utf-8")


def clean_name(name):
    """Remove UUID-like strings from names."""
    # Regular expression to identify UUID-like patterns
    uuid_pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.IGNORECASE)
    # Remove UUIDs
    cleaned_name = uuid_pattern.sub("", name).strip()
    # Remove any residual hyphens or underscores from start and end after UUID removal
    cleaned_name = re.sub(r'^[-_]+|[-_]+$', '', cleaned_name).strip()
    return cleaned_name


def create_confluence_space(space_key, space_name, description=""):
    """Create a new Confluence space."""

    url = f"{base_url}/rest/api/space"
    print(f"{url}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth}'
    }
    payload = {
        'key': space_key,
        'name': space_name,
        'description': {'plain': {'value': description, 'representation': 'plain'}}
    }
    print(f"{payload}")
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to create space: {response.text}")
    return response.json()

def create_confluence_page(space_key, title, content, parent_id=None):
    """Create a new Confluence page in the specified space."""
    url = f"{base_url}/rest/api/content"
    print(f"{url}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth}'
    }
    payload = {
        'type': 'page',
        'title': title,
        'space': {'key': space_key},
        'body': {
            'storage': {
                'value': content,
                'representation': 'storage'
            }
        },
        'ancestors': [{'id': parent_id}] if parent_id else []
    }
    print(f"{payload}")
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to create page: {response.text}")
    return response.json()

def upload_attachment(page_id, file_path):
    """Upload an attachment to a Confluence page."""
    url = f"{base_url}/rest/api/content/{page_id}/child/attachment"
    print(f"{url}")
    headers = {
        'X-Atlassian-Token': 'no-check',
        'Authorization': f'Basic {auth}'
    }
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, headers=headers, files=files)
    if response.status_code != 200:
        raise Exception(f"Failed to upload attachment: {response.text}")
    return response.json()

def process_directory(root_dir):
    """Process each directory and file under the root directory for space and page creation."""
    for root, dirs, files in os.walk(root_dir):
        raw_space_key = os.path.basename(root).upper().replace(" ", "_")
        raw_space_name = os.path.basename(root)

        # Clean the space key and name
        space_key = clean_name(raw_space_key)
        space_name = clean_name(raw_space_name)

        space = create_confluence_space(space_key, space_name)

        page_created = False
        page_id = None

        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".md"):
                html_content = markdown(open(file_path, 'r').read())
                raw_page_title = os.path.splitext(os.path.basename(file))[0]

                # Clean the page title
                page_title = clean_name(raw_page_title)

                page = create_confluence_page(space_key, page_title, html_content)
                page_id = page['id']
                page_created = True

            if not page_created:
                # Create a default page if no markdown file has created a page yet
                default_content = "This page is created as a placeholder for attachments."
                page = create_confluence_page(space_key, "Default Page", default_content)
                page_id = page['id']
                page_created = True

            if not file.endswith(".md"):
                # Upload non-markdown files as attachments to the created or default page
                upload_attachment(page_id, file_path)


# Example usage
root_directory = "./raw"
process_directory(root_directory)

