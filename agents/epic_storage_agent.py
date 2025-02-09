from tools.jira_tools import get_historic_epics
from models.vector_store import store_epic, check_if_epic_exists
import os
from dotenv import load_dotenv

load_dotenv()
JIRA_BOARD_ID = os.getenv("JIRA_BOARD_ID")

def store_historic_epics():
    """Fetches epics from a specific Jira board and stores them as embeddings, avoiding duplicates."""
    
    print(f"📥 Fetching all historic epics from Jira board {JIRA_BOARD_ID}...")
    all_epics = get_historic_epics()

    for epic in all_epics:
        store_epic(epic)

    print("✅ All historic epics processed.")

if __name__ == "__main__":
    store_historic_epics()
