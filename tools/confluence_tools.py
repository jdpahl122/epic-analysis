import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# ✅ Correct environment variable names
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_EMAIL = os.getenv("JIRA_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not CONFLUENCE_API_TOKEN:
    raise ValueError("❌ ERROR: CONFLUENCE_API_TOKEN is missing. Check your .env file!")

if not CONFLUENCE_EMAIL:
    raise ValueError("❌ ERROR: CONFLUENCE_EMAIL is missing. Check your .env file!")

def get_confluence_page(page_id):
    """Fetches a Confluence page's content by ID."""
    url = f"{CONFLUENCE_BASE_URL}/wiki/rest/api/content/{page_id}?expand=body.view"

    # ✅ Encode credentials for Basic Auth
    auth_string = f"{CONFLUENCE_EMAIL}:{CONFLUENCE_API_TOKEN}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Accept": "application/json"
    }

    print(f"🔍 Fetching Confluence page: {url}")

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print("❌ ERROR: Authentication failed! Check your API token and email.")
        return None

    if response.status_code != 200:
        print(f"❌ Confluence API Error {response.status_code}: {response.text}")
        return None

    data = response.json()
    page_content = data.get("body", {}).get("view", {}).get("value", None)

    if not page_content:
        print("⚠️ Warning: Confluence page returned empty content!")

    return page_content
