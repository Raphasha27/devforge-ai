from app.core.llm import call_llm
import json

def scan_tech_debt(repo_name: str, files: dict):
    """
    Agent that scans for technical debt, legacy patterns, and 'TODO' comments.
    Generates a liquidation plan to improve codebase health.
    """
    debt_items = []
    
    # Simple keyword scanning combined with LLM analysis
    for path, content in files.items():
        if "TODO" in content or "FIXME" in content or "HACK" in content:
            debt_items.append({"path": path, "type": "Comment Debt"})
            
    prompt = f"""
    Analyze these file structures for the repository '{repo_name}':
    {list(files.keys())}
    
    Identify technical debt such as:
    1. Inconsistent naming conventions.
    2. Overly complex functions (smell).
    3. Missing documentation.
    4. Outdated patterns.
    
    Return a list of debt items and a 'Liquidation Strategy'.
    Return ONLY JSON:
    {{
        "debt_score": 0-100,
        "items": ["list"],
        "liquidation_plan": "text"
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        data = json.loads(response)
        return data
    except:
        return {"debt_score": 10, "items": debt_items, "liquidation_plan": "Continue monitoring."}
