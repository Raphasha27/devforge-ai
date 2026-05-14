from app.core.llm import call_llm
import json

def investigate_build_failure(repo_name: str, failed_logs: str):
    """
    Agent that analyzes build failure logs and proposes a structural fix.
    """
    prompt = f"""
    Analyze the following build failure log for '{repo_name}':
    ---
    {failed_logs}
    ---
    
    Propose a root cause and a fix.
    Return ONLY a JSON object:
    {{
        "root_cause": "text",
        "proposed_fix": "text",
        "confidence": 0-100
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {"root_cause": "Unknown", "proposed_fix": "Manual review required", "confidence": 0}
