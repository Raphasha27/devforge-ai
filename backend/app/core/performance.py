from app.core.db import SessionLocal, DBRepo
from datetime import datetime
import json

class PerformanceTracker:
    """
    Tracks ROI, Success Rates, and Agent Efficiency for DevForge v12.
    """
    def __init__(self):
        self.metrics = {
            "total_launches": 0,
            "security_rejections": 0,
            "refactor_impact": 0,
            "estimated_mrr": 0.0 # Mocked 'Revenue'
        }

    def record_launch(self, success: bool, reason: str = ""):
        """Records a build/launch event."""
        if success:
            self.metrics["total_launches"] += 1
            self.metrics["estimated_mrr"] += 49.0 # Mocked $49/mo per product
        else:
            self.metrics["security_rejections"] += 1

    def increment_mrr(self, amount: float):
        """Manually increments the estimated MRR."""
        self.metrics["estimated_mrr"] += amount

    def record_evolution(self, impact_score: int):
        """Records the technical impact of a mutation."""
        self.metrics["refactor_impact"] += impact_score

    def get_scorecard(self):
        """Returns the current performance scorecard."""
        return self.metrics

# Singleton instance
performance_tracker = PerformanceTracker()
