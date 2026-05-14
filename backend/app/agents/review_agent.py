from app.core.llm import call_llm
import json

def review_pull_request(repo_name: str, pr_title: str, pr_body: str, diff_content: str):
    """
    AI Agent that performs an autonomous peer review on pull requests.
    Checks for architectural alignment and security best practices.
    """
    prompt = f"""
    You are a Senior Staff Engineer at DevForge AI.
    Review the following Pull Request for the repository '{repo_name}':
    
    Title: {pr_title}
    Description: {pr_body}
    
    Diff Snippet:
    ---
    {diff_content[:2000]}
    ---
    
    Provide a professional, helpful review comment. 
    Focus on:
    1. Architectural alignment.
    2. Potential security flaws.
    3. Code quality and standards.
    
    If everything looks great, start with 'LGTM! 🚀'.
    Return ONLY the comment text.
    """
    
    comment = call_llm(prompt)
    return comment
