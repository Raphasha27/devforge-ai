import json
from app.core.llm import call_llm

def generate_market_idea(signal: str):
    """
    Agent that analyzes a market signal and generates a high-demand tool idea.
    """
    prompt = f"""
    You are a senior open-source product manager.
    Analyze this developer market signal: "{signal}"
    
    Generate a HIGH-DEMAND developer tool idea that solves a real pain point.
    
    Rules:
    - Must be useful daily or weekly.
    - Must be simple enough to be an MVP but powerful enough to be starred.
    - Target: CLI tools, API utilities, or DevOps helpers.
    
    Return ONLY a JSON object with:
    {{
        "name": "Catchy and professional name",
        "description": "One sentence elevator pitch",
        "why_people_will_use_it": "Deep dive into the pain point it solves",
        "tags": ["tag1", "tag2"],
        "target_audience": "e.g. Backend Engineers, DevOps, etc."
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {
            "name": f"{signal.replace(' ', '-')}-tool",
            "description": f"A powerful utility for {signal}",
            "why_people_will_use_it": "It saves time and automates manual tasks.",
            "tags": ["automation", "dev-tools"],
            "target_audience": "Developers"
        }
