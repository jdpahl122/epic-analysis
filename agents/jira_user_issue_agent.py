import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_user_issues(user_email):
    """Fetches Jira issues assigned to a user in the past 6 months and tracks time spent in 'In Progress'."""
    
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    
    jql_query = f'assignee="{user_email}" AND created >= "{six_months_ago}" ORDER BY created DESC'
    
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        params={"jql": jql_query, "maxResults": 100, "fields": "summary,status,created,resolutiondate"}
    )
    
    if response.status_code != 200:
        print(f"❌ Jira API Error: {response.status_code} - {response.text}")
        return []

    issues = response.json().get("issues", [])
    
    formatted_issues = []
    for issue in issues:
        issue_id = issue["id"]
        created = datetime.strptime(issue["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
        resolved = issue["fields"].get("resolutiondate")
        
        # Fetch status transition timestamps
        in_progress_time, resolved_time = get_status_transition_times(issue_id)

        resolution_time = None
        time_in_progress = None

        if resolved_time:
            resolved_dt = datetime.strptime(resolved_time, "%Y-%m-%dT%H:%M:%S.%f%z")
            resolution_time = (resolved_dt - created).days  # Total time to resolution
        
        if in_progress_time and resolved_time:
            in_progress_dt = datetime.strptime(in_progress_time, "%Y-%m-%dT%H:%M:%S.%f%z")
            time_in_progress = (resolved_dt - in_progress_dt).days  # Time spent actively working

        formatted_issues.append({
            "id": issue_id,
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "status": issue["fields"]["status"]["name"],
            "created": created.strftime("%Y-%m-%d"),
            "in_progress": in_progress_time,
            "resolved": resolved_time if resolved_time else "Unresolved",
            "resolution_time": resolution_time,  # Days from open to resolved
            "time_in_progress": time_in_progress  # Days actively worked on
        })

    return formatted_issues


def get_status_transition_times(issue_id):
    """Fetches the timestamps for when an issue moved to 'In Progress' and when it was resolved."""
    
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_id}?expand=changelog"
    
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )

    if response.status_code != 200:
        print(f"❌ Jira API Error (Changelog): {response.status_code} - {response.text}")
        return None, None

    issue_data = response.json()
    changelog = issue_data.get("changelog", {}).get("histories", [])

    in_progress_time = None
    resolved_time = None

    for change in changelog:
        for item in change.get("items", []):
            if item.get("field") == "status":
                new_status = item.get("toString")
                timestamp = change["created"]

                if new_status.lower() == "in progress":
                    in_progress_time = timestamp
                elif new_status.lower() in ["resolved", "done"]:
                    resolved_time = timestamp

    return in_progress_time, resolved_time
