import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_user_issues(user_email):
    """Fetches Jira issues assigned to a user in the past 6 months."""
    
    since_date = (datetime.today() - timedelta(days=180)).strftime("%Y-%m-%d")
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    
    jql_query = f'assignee="{user_email}" AND updated >= "{since_date}" ORDER BY created DESC'
    params = {"jql": jql_query, "maxResults": 100, "fields": "summary,created,updated,resolutiondate,labels,issuetype,timetracking"}

    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN), params=params, headers={"Accept": "application/json"})

    if response.status_code != 200:
        print(f"❌ Jira API Error {response.status_code}: {response.text}")
        return []

    issues = response.json().get("issues", [])
    processed_issues = []

    for issue in issues:
        fields = issue.get("fields", {})
        processed_issues.append({
            "id": issue["id"],
            "key": issue["key"],
            "summary": fields.get("summary", "No summary"),
            "created": fields.get("created", ""),
            "updated": fields.get("updated", ""),
            "resolved": fields.get("resolutiondate", None),
            "labels": fields.get("labels", []),
            "type": fields.get("issuetype", {}).get("name", "Unknown"),
            "story_points": fields.get("customfield_10016", None),  # Adjust for your Jira config
        })

    return processed_issues
