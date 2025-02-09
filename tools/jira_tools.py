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
    """Fetches epics from a specific Jira board and excludes already stored ones."""
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{JIRA_BOARD_ID}/epic"
    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN), headers={"Accept": "application/json"})

    if response.status_code != 200:
        print(f"Jira API Error: {response.status_code}")
        return []

    all_epics = response.json().get("values", [])
    new_epics = []

    for epic in all_epics:
        epic_id = str(epic["id"])
        if check_if_epic_exists(epic_id):
            print(f"✅ Epic {epic_id} already exists. Skipping.")
            continue

        # Fetch detailed information about the epic
        epic_details = get_epic_details(epic_id)

        # Fetch all child issues of this epic
        child_issues = get_epic_issues(epic_id)

        new_epics.append({
            "epic_id": epic_id,
            "key": epic_details["key"],
            "name": epic_details["name"],
            "summary": epic_details["summary"],
            "description": epic_details["description"],
            "issues": child_issues  # Store issues as a list
        })

    return new_epics

def get_epic_details(epic_id):
    """Fetches a single epic's full details."""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{epic_id}"
    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN), headers={"Accept": "application/json"})

    if response.status_code != 200:
        print(f"Jira API Error (Epic Details): {response.status_code}")
        return {"key": "", "name": "", "summary": "", "description": ""}

    data = response.json()

    # Extract the description (may be a dict in Atlassian Document Format)
    raw_description = data["fields"].get("description", "")
    
    if isinstance(raw_description, dict):  # If it's ADF, extract plain text
        description_text = extract_adf_text(raw_description)
    else:
        description_text = raw_description  # If it's already plain text

    return {
        "key": data["key"],
        "name": data["fields"].get("customfield_10002", ""),
        "summary": data["fields"].get("summary", ""),
        "description": description_text  # Store extracted text
    }

def get_epic_issues(epic_id):
    """Fetches all issues related to an epic."""
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/epic/{epic_id}/issue"
    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN), headers={"Accept": "application/json"})

    if response.status_code != 200:
        print(f"Jira API Error (Epic Issues): {response.status_code}")
        return []

    issues = response.json().get("issues", [])
    return [
        {
            "id": issue["id"],
            "key": issue["key"],
            "summary": issue["fields"].get("summary", ""),
            "description": issue["fields"].get("description", ""),
            "status": issue["fields"]["status"]["name"],
            "assignee": issue["fields"]["assignee"]["displayName"] if issue["fields"].get("assignee") else "Unassigned"
        }
        for issue in issues
    ]

def extract_adf_text(adf_description):
    """Extract plain text from Atlassian Document Format (ADF) description."""
    if not isinstance(adf_description, dict):
        return str(adf_description)  # Return as-is if not ADF
    
    text_content = []

    def extract_content(content):
        """Recursively extract text from ADF JSON structure."""
        if isinstance(content, list):
            for item in content:
                extract_content(item)
        elif isinstance(content, dict):
            if content.get("type") == "text" and "text" in content:
                text_content.append(content["text"])
            if "content" in content:
                extract_content(content["content"])

    extract_content(adf_description.get("content", []))

    return "\n".join(text_content)  # Join all extracted text
