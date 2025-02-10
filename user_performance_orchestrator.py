from agents.jira_user_issue_agent import get_user_issues
from agents.user_performance_analysis_agent import analyze_user_performance

USER_EMAIL = "developer@example.com"  # Change this to analyze a specific user

def user_performance_orchestrate(user_email):
    """Runs the analysis for a specific user's performance over the past 6 months."""
    
    print(f"\n📥 Fetching Jira issues for {user_email} in the past 6 months...")
    user_issues = get_user_issues(user_email)

    print("\n🔍 Analyzing user performance...")
    user_performance_report = analyze_user_performance(user_email, user_issues)
    
    print("\n📝 User Performance Report:\n", user_performance_report)

if __name__ == "__main__":
    user_performance_orchestrate(USER_EMAIL)
