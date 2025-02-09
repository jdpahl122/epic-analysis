from models.vector_store import query_similar_epics

def historic_analysis_agent(epic_text):
    """Finds similar past epics using PostgreSQL vector database."""
    print("🔍 Searching for similar past epics...")
    similar_epics = query_similar_epics(epic_text)
    
    return similar_epics
