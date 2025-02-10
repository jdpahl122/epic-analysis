import numpy as np
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_user_performance(user_email, issues):
    """Analyzes user performance based on ticket complexity, completion speed, and work scope."""
    
    if not issues:
        return f"⚠️ No Jira issues found for {user_email} in the last 6 months."

    # Calculate average resolution time
    resolved_issues = [i for i in issues if i["resolution_time"] is not None]
    avg_resolution_time = (
        np.mean([i["resolution_time"] for i in resolved_issues])
        if resolved_issues else "N/A"
    )

    # Categorize work type (new features, bug fixes, maintenance)
    new_feature_keywords = ["feature", "implement", "add", "deploy"]
    maintenance_keywords = ["fix", "patch", "update", "migrate"]
    
    new_features = []
    maintenance = []
    unresolved_issues = []
    
    for issue in issues:
        title = issue["summary"].lower()
        
        if any(keyword in title for keyword in new_feature_keywords):
            new_features.append(issue)
        elif any(keyword in title for keyword in maintenance_keywords):
            maintenance.append(issue)
        else:
            unresolved_issues.append(issue)

    # Summarize issue breakdown
    issue_summary = f"""
    📌 **User Performance Report for {user_email}**
    
    - **Total Issues Assigned:** {len(issues)}
    - **Issues Resolved:** {len(resolved_issues)}
    - **Average Resolution Time:** {avg_resolution_time} days
    - **New Feature Work:** {len(new_features)}
    - **Maintenance/Bug Fix Work:** {len(maintenance)}
    - **Unresolved Issues:** {len(unresolved_issues)}
    """

    # Generate insights using LLM
    prompt = f"""
    Based on this analysis:
    
    {issue_summary}

    Analyze:
    1. How efficiently the user is resolving tickets.
    2. Whether their tasks appear more complex or simple.
    3. Any patterns in delays or blockers.
    4. Recommendations for improving their workflow.
    """

    llm = Ollama(model=os.getenv("OLLAMA_MODEL"))
    response = llm.invoke(prompt)
    
    return f"{issue_summary}\n\n🔍 **Analysis & Recommendations:**\n{response}"
