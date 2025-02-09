from agents.epic_storage_agent import store_historic_epics
from agents.epic_ingestion_agent import epic_ingestion_agent
from agents.historic_analysis_agent import historic_analysis_agent
from agents.epic_comparison_agent import epic_comparison_agent
from agents.refinement_agent import refinement_agent

import os
from dotenv import load_dotenv

load_dotenv()
BOARD_ID = os.getenv("JIRA_BOARD_ID")  # ✅ Load Board ID from .env

def orchestrate(epic_id, confluence_page_id):
    """Runs the full analysis pipeline."""
    
    # Step 1: Fetch & Store Historic Epics
    print("\n📥 Collecting historic epics...")
    store_historic_epics(BOARD_ID)  # ✅ Now references correct function

    # Step 2: Fetch Target Epic Data
    print("\n📥 Fetching target epic...")
    epic_data = epic_ingestion_agent(epic_id, confluence_page_id)
    print(f"✅ Retrieved {len(epic_data['issues'])} issues for EPIC-{epic_id}")

    # Step 3: Find Similar Past Epics
    print("\n🔍 Retrieving historic epics...")
    similar_epics = historic_analysis_agent(epic_data["issues"])  # ✅ Use `issues` not `confluence`
    print(f"✅ Found {len(similar_epics)} similar past epics")

    # Step 4: Compare Against Historic Epics
    print("\n⚖️ Analyzing differences...")
    comparison_results = epic_comparison_agent(epic_data, similar_epics)
    print("✅ Epic comparison complete.")

    # Step 5: Generate New Stories & Risks
    print("\n📌 Refining backlog...")
    refined_backlog = refinement_agent(comparison_results)
    
    # Log Final Output
    print("\n✅ Suggested Backlog Refinements:")
    print(refined_backlog)

# Run Orchestration
if __name__ == "__main__":
    orchestrate("EPIC-123", "CONFLUENCE-456")
