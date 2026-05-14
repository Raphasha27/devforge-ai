def quality_score(idea: dict):
    """
    Heuristic-based quality gate to prevent low-value repo generation.
    Returns a score from 0 to 100.
    """
    score = 0
    desc = idea.get("description", "").lower()
    name = idea.get("name", "").lower()
    
    # Positive signals
    if any(keyword in desc for keyword in ["cli", "automation", "workflow", "performance", "security"]):
        score += 30
    if any(keyword in desc for keyword in ["simple", "fast", "lightweight", "instant"]):
        score += 20
    if len(idea.get("tags", [])) >= 2:
        score += 10
        
    # Negative signals
    if len(desc) < 50:
        score -= 20
    if len(name) < 3:
        score -= 20
    if "todo" in desc or "example" in desc:
        score -= 30
        
    return max(0, min(100, score))

def should_publish(score: int):
    """
    Publishing threshold for the viral growth engine.
    """
    return score >= 75
