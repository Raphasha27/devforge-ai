from app.core.llm import call_llm

def triage_issue(issue_title: str, issue_body: str):
    """
    Classifies a GitHub issue into categories.
    """
    prompt = f"""
    You are a senior open-source maintainer.
    Triage the following issue:
    Title: {issue_title}
    Body: {issue_body}
    
    Return ONLY a single word from this list: [bug, feature, docs, security, invalid, question]
    """
    
    return call_llm(prompt).strip().lower()

def generate_maintainer_response(issue: dict):
    """
    Generates a professional and technical response to a user issue.
    """
    prompt = f"""
    You are a senior open-source maintainer.
    Generate a human-like, professional response to this issue:
    {issue['title']}
    
    Rules:
    - Be polite and helpful.
    - Ask for more info if needed.
    - If it's a bug, acknowledge and mention that a fix is being analyzed.
    - If it's a feature, mention if it aligns with the roadmap.
    - Keep it concise.
    """
    
    return call_llm(prompt)

def is_safe_to_automerge(diff: str):
    """
    Risk assessment for autonomous PR merging.
    """
    risky_keywords = ["password", "secret", "key", "auth", "payment", "database", "migration", "security"]
    
    if any(word in diff.lower() for word in risky_keywords):
        return False
        
    return True
