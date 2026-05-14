import json
from app.core.llm import call_llm

def productize_idea(idea: dict):
    """
    Converts a raw repo idea into a full-fledged developer product concept.
    Focuses on adoption, virality, and clear value proposition.
    """
    prompt = f"""
    You are a high-level open-source product strategist.
    Project: {idea['name']}
    Original Idea: {idea['description']}
    
    Turn this into a developer-facing PRODUCT.
    
    Return ONLY a JSON object with:
    {{
        "product_name": "Final branding name",
        "value_proposition": "Killer one-line hook",
        "target_audience": "Specific dev persona",
        "killer_feature": "Why this stands out from competitors",
        "usage_flow": ["step 1", "step 2", "step 3"],
        "viral_hook": "Why developers will share this tool"
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {
            "product_name": idea['name'],
            "value_proposition": idea['description'],
            "target_audience": "General Developers",
            "killer_feature": "Simplicity and speed",
            "usage_flow": ["Install", "Run"],
            "viral_hook": "Instant utility with zero config"
        }
