import os
import requests
from dotenv import load_dotenv
from models.vector_store import check_if_epic_exists

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BOARD_ID = os.getenv("JIRA_BOARD_ID")

def get_historic_epics():
    """Fetches epics from a specific Jira board, excluding already stored ones."""
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{JIRA_BOARD_ID}/epic"
    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN))

    if response.status_code != 200:
        print(f"Jira API Error: {response.status_code}")
        return []

    all_epics = response.json().get("values", [])
    new_epics = []

    for epic in all_epics:
        epic_id = epic["id"]

        if check_if_epic_exists(epic_id):  # ✅ Now correctly imported
            print(f"✅ Epic {epic_id} already exists. Skipping.")
            continue  # Skip already stored epics

        issues = get_epic_issues(epic_id)
        new_epics.append({"epic_id": epic_id, "summary": epic["summary"], "issues": issues})

    return new_epics

def get_epic_issues(epic_id):
    """Fetches all issues related to an epic."""
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/epic/{epic_id}/issue"
    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN))

    if response.status_code != 200:
        print(f"Jira API Error: {response.status_code}")
        return []

    return response.json().get("issues", [])
