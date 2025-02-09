import os
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def refinement_agent(comparison_results):
    """Extracts missing backlog items, dependencies, and risks."""

    llm = OllamaLLM(model=os.getenv("OLLAMA_MODEL"))  # ✅ Updated Ollama usage

    # ✅ Use PromptTemplate for better formatting
    prompt = PromptTemplate(
        input_variables=["comparison_results"],
        template="""
        Based on the following analysis:

        {comparison_results}

        Provide a structured JSON output containing:
        - "missing_stories": A list of missing user stories.
        - "missing_requirements": A list of any missing requirements.
        - "potential_risks": A list of potential pitfalls and risks.

        Ensure the output is a valid JSON object.
        """
    )

    try:
        # ✅ Use `invoke()` instead of passing raw string
        response = llm.invoke(prompt.format(comparison_results=comparison_results))

        return response
    except Exception as e:
        print(f"❌ Refinement Agent Error: {e}")
        return None
