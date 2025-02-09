import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_confluence_page(page_id):
    """Fetch Confluence page content."""
    url = f"{CONFLUENCE_BASE_URL}/wiki/rest/api/content/{page_id}?expand=body.view"
    headers = {"Authorization": f"Bearer {CONFLUENCE_API_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.json()["body"]["view"]["value"]
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text()
    
    return None
