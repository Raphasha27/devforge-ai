from app.core.llm import call_llm
import json

def find_blue_ocean_markets():
    """
    Agent that identifies 'Blue Ocean' technical markets—high value, low competition niches.
    """
    prompt = """
    Act as a Master Market Strategist for DevForge AI.
    Analyze the current developer tool landscape and identify 3 'Blue Ocean' markets.
    These should be underserved, emerging, or hidden technical domains.
    
    Examples: 'WASM-based Edge Proxy', 'Zero-Trust DB Connector', 'Local-first PWA Framework for IoT'.
    
    For each market, provide:
    1. Market Name.
    2. Why it's underserved.
    3. Potential 'Product Alpha' idea.
    4. Dominance Score (0-100).
    
    Return ONLY a JSON object:
    {
        "markets": [
            {
                "name": "text",
                "gap": "text",
                "alpha_idea": "text",
                "dominance_potential": 85
            }
        ],
        "strategic_recommendation": "text"
    }
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {"markets": [], "strategic_recommendation": "Maintain core products."}
