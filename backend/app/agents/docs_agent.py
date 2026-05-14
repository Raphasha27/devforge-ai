from app.core.llm import call_llm

def generate_viral_readme(product: dict, architecture: dict):
    """
    Generates a high-converting, viral-ready README for the repo.
    """
    prompt = f"""
    Write a HIGH-CONVERTING GitHub README for the following product:
    Product Name: {product['product_name']}
    Hook: {product['value_proposition']}
    Killer Feature: {product['killer_feature']}
    Usage: {", ".join(product['usage_flow'])}
    
    Architecture Details:
    Stack: {architecture['stack']}
    Commands: {architecture['commands']}
    
    Must include:
    - Cinematic Headline
    - Problem Statement (Developer Pain)
    - The Solution (How this tool wins)
    - Quick Install & Start
    - Visual/Interactive Demo description
    - Why it's different
    - Call to Action (Star, Fork, Contribute)
    
    Tone: Senior Engineer, Clean, Minimalist, Opinionated.
    """
    
    return call_llm(prompt)

def generate_seo_metadata(product: dict):
    """
    Generates SEO-optimized tags and descriptions for GitHub listing.
    """
    prompt = f"""
    Generate GitHub SEO metadata for: {product['product_name']}
    Description: {product['value_proposition']}
    
    Return ONLY a JSON object with:
    {{
        "description": "Max 160 chars optimized for search",
        "topics": ["list", "of", "relevant", "tags"],
        "display_title": "Optimized repo name"
    }}
    """
    import json
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {
            "description": product['value_proposition'][:160],
            "topics": ["developer-tools", "productivity", "cli"],
            "display_title": product['product_name'].lower().replace(" ", "-")
        }
