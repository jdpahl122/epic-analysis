from agents.historic_epic_collector import historic_epic_collector
from agents.epic_ingestion_agent import epic_ingestion_agent
from agents.historic_analysis_agent import historic_analysis_agent
from agents.epic_comparison_agent import epic_comparison_agent
from agents.refinement_agent import refinement_agent

BOARD_ID = "123"  # Replace with your actual board ID

def orchestrate(epic_id, confluence_page_id):
    """Runs the full analysis pipeline."""
    
    # Step 1: Fetch & Store Historic Epics
    print("\n📥 Collecting historic epics...")
    historic_epic_collector(BOARD_ID)

    # Step 2: Fetch Target Epic Data
    print("\n📥 Fetching target epic...")
    epic_data = epic_ingestion_agent(epic_id, confluence_page_id)

    # Step 3: Find Similar Past Epics
    print("\n🔍 Retrieving historic epics...")
    similar_epics = historic_analysis_agent(epic_data["confluence"])

    # Step 4: Compare Against Historic Epics
    print("\n⚖️ Analyzing differences...")
    comparison_results = epic_comparison_agent(epic_data, similar_epics)

    # Step 5: Generate New Stories & Risks
    print("\n📌 Refining backlog...")
    refined_backlog = refinement_agent(comparison_results)

    print("\n✅ Suggested Backlog Refinements:\n", refined_backlog)

# Run Orchestration
if __name__ == "__main__":
    orchestrate("EPIC-123", "CONFLUENCE-456")
