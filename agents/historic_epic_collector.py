from tools.jira_tools import get_board_epics, get_epic_issues
from models.vector_store import store_epic

def historic_epic_collector(board_id):
    """Fetches all historic epics from Jira, processes, and stores them."""
    
    print(f"📥 Fetching epics from board {board_id}...")
    epics = get_board_epics(board_id)

    if not epics:
        print("✅ No new epics to process.")
        return
    
    for epic in epics:
        epic_id = epic["id"]
        epic_name = epic["name"]
        
        print(f"📥 Processing epic {epic_id}: {epic_name}")
        
        # Get issues linked to this epic
        issues = get_epic_issues(epic_id)
        issue_details = "\n".join([f"- {issue['fields']['summary']}" for issue in issues])

        # Prepare full text for embedding
        full_text = f"Epic: {epic_name}\nIssues:\n{issue_details}"
        
        # Store in vector DB
        store_epic(epic_id, full_text)

    print("✅ Historic epics processing complete.")
