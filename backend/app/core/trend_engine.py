import json
from app.core.llm import call_llm

def get_trending_signals():
    """
    Mines real developer demand signals using AI-driven industry analysis.
    """
    prompt = """
    Analyze the current open-source landscape (Developer Tools, AI, Infrastructure, Security).
    Identify 3 high-potential technical domains that are currently underserved but have high demand.
    
    Examples:
    - "WASM-based cloud edge runtimes"
    - "Zero-trust dependency proxy"
    - "AI-native CLI for git history archaeology"
    
    Return ONLY a JSON list of strings.
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return [
            "developer productivity CLI tools",
            "CI/CD pipeline automation helpers",
            "security scanning and dependency audit utilities"
        ]
