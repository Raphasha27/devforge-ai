import json
from app.core.llm import call_llm

def get_architectural_standards(strategy: dict):
    """
    CTO Agent: Enforces technical standards across the company's ecosystem.
    """
    prompt = f"""
    You are the CTO of DevForge AI.
    Company Strategy: {strategy['focus_areas']}
    
    Define the architectural standards for current projects to ensure ecosystem consistency.
    
    Return ONLY a JSON object with:
    {{
        "preferred_stack": "e.g. Python 3.12, Typer, Pydantic",
        "testing_standards": "e.g. 80% coverage minimum",
        "documentation_rules": "e.g. Docstrings for all public methods",
        "security_policy": "e.g. No raw SQL, use prepared statements"
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {{ "preferred_stack": "Python", "testing_standards": "pytest", "documentation_rules": "markdown" }}

def generate_roadmap(strategy: dict):
    """
    Product Manager Agent: Converts strategy into an actionable roadmap.
    """
    prompt = f"""
    You are the Product Manager of DevForge AI.
    CEO Strategy: {strategy['focus_areas']}
    
    Generate a roadmap of features and new products.
    
    Return ONLY a JSON object with:
    {{
        "roadmap": [
            {{ "item": "Feature/Product Name", "priority": "High/Medium/Low", "target_date": "Cycle 1", "description": "What it is" }}
        ]
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {{ "roadmap": [] }}
