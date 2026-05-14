from enum import Enum
from typing import Dict

class ProductStage(Enum):
    INCUBATION = "incubation"
    SCALING = "scaling"
    MATURE = "mature"
    EOL = "eol" # End of Life

class LifecycleAction(Enum):
    MAINTAIN = "maintain"
    ARCHIVE = "archive"
    PIVOT = "pivot"

class ProductLifecycleManager:
    """
    Manages the lifecycle stages of products in the DevForge ecosystem.
    Decides when to scale, pivot, or archive a repository.
    """
    def decide_lifecycle(self, repo_name: str, stats: dict, sentiment: dict):
        """
        Decision engine based on market sentiment and repo performance.
        """
        score = stats.get("stars_delta", 0) * 2 - stats.get("open_issues", 0)
        
        if sentiment.get("sentiment_score", 50) < 30 and score < 5:
            return LifecycleAction.ARCHIVE, "Low market interest and low repository engagement."
            
        if sentiment.get("sentiment_score", 50) > 80 and score > 20:
            return LifecycleAction.PIVOT, "High market hype detected. Recommending a pivot to capture new trends."
            
        return LifecycleAction.MAINTAIN, "Performance is stable."

    def get_stage(self, stats: dict):
        """Infers the current stage of the product."""
        stars = stats.get("stars_delta", 0)
        if stars > 100: return ProductStage.MATURE.value
        if stars > 20: return ProductStage.SCALING.value
        return ProductStage.INCUBATION.value
