from tools.jira_tools import get_historic_epics
from models.vector_store import store_epic, check_if_epic_exists
import os
from dotenv import load_dotenv

load_dotenv()
JIRA_BOARD_ID = os.getenv("JIRA_BOARD_ID")  # ✅ Ensure we use the board ID

def store_historic_epics():
    """Fetches epics from a specific Jira board and stores them as embeddings, avoiding duplicates."""
    
    print(f"📥 Fetching all historic epics from Jira board {JIRA_BOARD_ID}...")
    all_epics = get_historic_epics()

    for epic in all_epics:
        epic_id = epic["epic_id"]

        if check_if_epic_exists(epic_id):
            print(f"✅ Epic {epic_id} already stored, skipping...")
            continue  # Skip already stored epics

        epic_text = f"{epic['summary']} {epic['issues']}"
        store_epic(epic_id, epic_text)
        print(f"📌 Stored epic {epic_id}")

    print("✅ All historic epics processed.")

if __name__ == "__main__":
    store_historic_epics()
