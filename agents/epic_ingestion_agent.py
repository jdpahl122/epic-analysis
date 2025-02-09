from tools.jira_tools import get_epic_issues
from tools.confluence_tools import get_confluence_page

def epic_ingestion_agent(epic_id, confluence_page_id):
    """Fetches epic issues and related Confluence docs."""
    print(f"📥 Fetching issues for epic {epic_id}...")
    issues = get_epic_issues(epic_id)

    print(f"📥 Fetching Confluence documentation {confluence_page_id}...")
    confluence_text = get_confluence_page(confluence_page_id)

    return {
        "epic_id": epic_id,
        "issues": issues,
        "confluence": confluence_text
    }
