from app.core.llm import call_llm
import json

def plan_stack_migration(repo_name: str, current_stack: list, target_stack: str):
    """
    Agent that plans a structural migration from a legacy stack to a recommended one.
    """
    prompt = f"""
    The repository '{repo_name}' is currently using: {current_stack}.
    We need to migrate it to: {target_stack}.
    
    Provide a multi-step migration plan.
    Identify:
    1. Files to be renamed/migrated.
    2. Dependencies to be swapped.
    3. Potential breaking changes.
    
    Return ONLY a JSON object:
    {{
        "target": "{target_stack}",
        "steps": ["list"],
        "complexity": "Low/Medium/High",
        "estimated_hours": 0
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {"target": target_stack, "steps": ["Manual migration required"], "complexity": "High"}
