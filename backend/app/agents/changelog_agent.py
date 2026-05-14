from app.core.llm import call_llm
import json

def generate_viral_changelog(repo_name: str, version: str, changes: list):
    """
    Agent that generates a high-impact, viral changelog for ecosystem updates.
    """
    prompt = f"""
    Act as a Technical Product Marketer for DevForge AI.
    The repository '{repo_name}' has been updated to version {version}.
    
    Changes:
    {changes}
    
    Generate a viral changelog:
    1. A catchy title (e.g., 'The Neural Upgrade').
    2. A 'TL;DR' for developers.
    3. High-energy bullet points for each change.
    4. A 'Viral Hook' for social media.
    
    Return ONLY a JSON object:
    {{
        "title": "text",
        "tldr": "text",
        "updates": ["list"],
        "viral_hook": "text"
    }}
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {"title": "Update", "tldr": "New features added.", "updates": changes, "viral_hook": "Check it out!"}
