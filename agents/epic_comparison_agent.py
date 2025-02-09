import os
from langchain.chains import LLMChain
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def epic_comparison_agent(epic_data, similar_epics):
    """Compares target epic against historic data to find gaps."""

    llm = OllamaLLM(model=os.getenv("OLLAMA_MODEL"))  # ✅ Updated Ollama usage

    # ✅ Improved prompt with structured output request
    prompt = PromptTemplate(
        input_variables=["epic", "historical"],
        template="""
        You are an experienced Agile consultant analyzing a software development epic.
        
        Below is the **target epic** that needs analysis:
        {epic}
        
        Here are **historically similar epics**:
        {historical}
        
        Perform a detailed comparison and output your findings in **structured JSON format**:
        - "missing_requirements": A list of missing functional or technical requirements.
        - "missing_stories": A list of suggested additional user stories.
        - "potential_risks": A list of potential risks or pitfalls.

        Ensure the response is a **valid JSON object**.
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        # ✅ Use `invoke()` instead of the deprecated `run()`
        result = chain.invoke({"epic": epic_data, "historical": similar_epics})

        return result
    except Exception as e:
        print(f"❌ Epic Comparison Agent Error: {e}")
        return None
