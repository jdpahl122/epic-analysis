import numpy as np
from models.vector_store import embed_text

def historic_analysis_agent(confluence_text):
    """Find similar epics based on the given epic's Confluence description."""

    if not confluence_text:
        raise ValueError("❌ ERROR: Confluence text is empty or None. Check the API response!")

    # Generate an embedding for the target text
    query_embedding = np.array(embed_text(confluence_text))

    from models.vector_store import query_similar_epics  # Lazy import to avoid circular dependency
    similar_epics = query_similar_epics(query_embedding)

    return similar_epics
