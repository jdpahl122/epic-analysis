import os
import numpy as np
import json
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def analyze_user_performance(user_email, issues):
    """Uses LLM to analyze a developer's performance based on past 6 months of work."""
    
    if not issues:
        return f"❌ No issues found for user {user_email} in the past 6 months."

    llm = OllamaLLM(model=os.getenv("OLLAMA_MODEL"))

    avg_completion_time = np.mean([
        (np.datetime64(issue["resolved"]) - np.datetime64(issue["created"])).astype(int)
        for issue in issues if issue["resolved"]
    ]) if any(issue["resolved"] for issue in issues) else "N/A"

    avg_story_points = np.mean([
        issue["story_points"] for issue in issues if issue["story_points"]
    ]) if any(issue["story_points"] for issue in issues) else "N/A"

    ticket_types = {issue["type"] for issue in issues}
    
    prompt = PromptTemplate(
        input_variables=["issues", "avg_completion_time", "avg_story_points", "ticket_types"],
        template="""
        You are a software engineering performance analyst.
        
        The following developer has completed tasks in the past 6 months:
        {issues}

        Their **average ticket completion time** is **{avg_completion_time} days**.
        Their **average story points per ticket** is **{avg_story_points}**.
        The ticket types they worked on include: {ticket_types}.

        Analyze their performance and answer:
        1. What is their perceived work difficulty based on ticket descriptions?
        2. Are they resolving issues faster or slower than expected?
        3. Are they working mostly on new features, bugs, or refactoring?
        4. Do they need improvement in any area?
        """
    )

    analysis = llm.invoke(
        prompt.format(
            issues=json.dumps(issues, indent=2),
            avg_completion_time=avg_completion_time,
            avg_story_points=avg_story_points,
            ticket_types=", ".join(ticket_types)
        )
    )

    return analysis
