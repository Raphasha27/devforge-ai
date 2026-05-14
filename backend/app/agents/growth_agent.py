from app.core.llm import call_llm
import json

def generate_growth_campaign(product_name: str, value_prop: str, tech_stack: list):
    """
    Agent that dreams up viral growth campaigns for ecosystem products.
    Generates SEO keywords, Twitter threads, and Product Hunt descriptions.
    """
    prompt = f"""
    Act as a Viral Growth Hacker for DevForge AI.
    The product '{product_name}' has been launched.
    Value Proposition: {value_prop}
    Tech Stack: {tech_stack}
    
    Generate a viral growth campaign:
    1. A 'Product Hunt' style tagline.
    2. A 5-tweet viral thread script.
    3. High-impact SEO keywords.
    4. A 'Reddit' community target list.
    
    Return ONLY a JSON object:
    {{
        "tagline": "text",
        "twitter_thread": ["list"],
        "seo_keywords": ["list"],
        "reddit_targets": ["list"],
        "viral_hook": "text"
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {"tagline": "The future of dev tools.", "twitter_thread": ["Thread..."], "seo_keywords": ["AI"], "viral_hook": "Efficiency."}
