import os
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

def epic_comparison_agent(epic_data, similar_epics):
    """Compares target epic against historic data to find gaps."""
    
    llm = Ollama(model=os.getenv("OLLAMA_MODEL"))

    prompt = PromptTemplate(
        input_variables=["epic", "historical"],
        template="Analyze the following epic:\n{epic}\n\nCompare it with past epics:\n{historical}\n\nIdentify missing requirements, dependencies, and risks."
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run({"epic": epic_data, "historical": similar_epics})

    return result
