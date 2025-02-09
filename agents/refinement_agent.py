import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

def refinement_agent(comparison_results):
    """Extracts missing backlog items, dependencies, and risks."""
    
    prompt = f"""
    Based on this analysis:
    
    {comparison_results}
    
    Provide:
    1. A list of missing user stories.
    2. Any missing requirements.
    3. Potential pitfalls and risks.
    """

    llm = Ollama(model=os.getenv("OLLAMA_MODEL"))
    response = llm.invoke(prompt)
    
    return response
