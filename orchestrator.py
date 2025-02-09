from agents.epic_ingestion_agent import epic_ingestion_agent
from agents.historic_analysis_agent import historic_analysis_agent
from agents.epic_comparison_agent import epic_comparison_agent
from agents.refinement_agent import refinement_agent

TEST_EPIC_ID = "DENG-2536"  # Replace with target epic ID
TEST_CONFLUENCE_PAGE_ID = "23247159297"  # Replace with actual page ID

def orchestrate(epic_id, confluence_page_id):
    """Runs the analysis pipeline for a specific epic."""
    
    # Step 1: Fetch Target Epic Data
    print("\n📥 Fetching target epic...")
    epic_data = epic_ingestion_agent(epic_id, confluence_page_id)

    # Step 2: Find Similar Past Epics
    print("\n🔍 Retrieving similar historic epics...")
    similar_epics = historic_analysis_agent(epic_data["confluence"])

    # Step 3: Compare Against Historic Epics
    print("\n⚖️ Analyzing differences...")
    comparison_results = epic_comparison_agent(epic_data, similar_epics)

    # Step 4: Generate New Stories & Risks
    print("\n📌 Refining backlog...")
    refined_backlog = refinement_agent(comparison_results)

    print("\n✅ Suggested Backlog Refinements:\n", refined_backlog)

# Run Orchestration on a specific epic
if __name__ == "__main__":
    orchestrate(TEST_EPIC_ID, TEST_CONFLUENCE_PAGE_ID)
