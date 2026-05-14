from app.core.llm import call_llm
import json

def process_ceo_directive(directive: str):
    """
    Agent that translates a Human CEO directive into actionable tasks for the swarm.
    """
    prompt = f"""
    Act as the Chief of Staff for DevForge AI.
    The Human CEO has issued the following directive:
    "{directive}"
    
    Break this down into specific tasks for the following agents:
    - CEO Agent (Strategy)
    - CTO Agent (Standards/Infrastructure)
    - Architect Agent (Code structure/Refactors)
    - Growth Agent (Marketing/SEO)
    
    Return ONLY a JSON object:
    {{
        "priority": "High/Medium/Low",
        "delegation": {{
            "ceo": "task",
            "cto": "task",
            "architect": "task",
            "growth": "task"
        }},
        "estimated_impact": "text"
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {"priority": "Medium", "delegation": {}, "estimated_impact": "Unknown"}
