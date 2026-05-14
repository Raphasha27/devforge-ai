from app.core.llm import call_llm
import json

def analyze_market_sentiment():
    """
    Simulates scanning technical forums (Reddit, Hacker News) to detect developer sentiment.
    """
    prompt = """
    Act as a Market Intelligence Analyst for DevForge AI.
    Simulate a scan of current developer sentiment across Hacker News and Reddit (r/programming).
    
    Identify:
    1. Overall developer 'vibe' (Bully, Bearish, Cautious).
    2. Hot topics (e.g., 'Rust hype', 'AI fatigue', 'Edge computing').
    3. Sentiment score (0-100, 100 is maximum excitement).
    
    Return ONLY a JSON object:
    {
        "vibe": "text",
        "hot_topics": ["list"],
        "sentiment_score": 85,
        "recommendation": "text"
    }
    """
    
    response = call_llm(prompt, json_mode=True)
    try:
        return json.loads(response)
    except:
        return {"vibe": "Stable", "hot_topics": ["General Dev"], "sentiment_score": 50, "recommendation": "Proceed"}
