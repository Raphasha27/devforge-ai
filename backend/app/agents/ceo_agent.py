import json
from app.core.llm import call_llm

def generate_ceo_strategy(market_signals: list):
    """
    CEO Agent: High-level strategic decision maker.
    Analyzes market signals and decides the company's direction.
    """
    prompt = f"""
    You are the CEO of DevForge AI, an open-source product company.
    Current Market Signals: {market_signals}
    
    Decide the strategic priorities for the next cycle.
    
    Return ONLY a JSON object with:
    {{
        "focus_areas": ["priority 1", "priority 2"],
        "resource_allocation": {{ "new_products": 0.4, "maintenance": 0.6 }},
        "strategic_goals": ["goal 1", "goal 2"],
        "risk_assessment": "Summary of technical or market risks"
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {{
            "focus_areas": ["Productivity Tools", "DevOps Automation"],
            "resource_allocation": {{ "new_products": 0.5, "maintenance": 0.5 }},
            "strategic_goals": ["Increase developer adoption", "Stabilize core utilities"],
            "risk_assessment": "Market saturation in some CLI niches"
        }}

def decide_product_survival(portfolio_metrics: list):
    """
    CEO Agent: Decides which products to keep, kill, or pivot.
    """
    prompt = f"""
    You are the CEO of DevForge AI.
    Portfolio Performance: {portfolio_metrics}
    
    Decide which products to continue investing in and which to sunset.
    
    Return ONLY a JSON object with:
    {{
        "keep": ["list of product names"],
        "sunset": ["list of product names"],
        "pivot": [{{ "name": "product", "new_direction": "description" }}]
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {{ "keep": [], "sunset": [], "pivot": [] }}
