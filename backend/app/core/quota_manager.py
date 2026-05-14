import time

class QuotaManager:
    """
    Manages API quotas and costs for DevForge AI.
    Prevents runaway costs by throttling agent activity.
    """
    def __init__(self, daily_budget_usd: float = 10.0):
        self.daily_budget = daily_budget_usd
        self.current_spend = 0.0
        self.request_count = 0
        self.start_time = time.time()

    def record_request(self, est_cost: float):
        """Records an API request and its estimated cost."""
        self.current_spend += est_cost
        self.request_count += 1

    def is_within_quota(self) -> bool:
        """Checks if the system is within its daily budget."""
        # Simple reset after 24h
        if time.time() - self.start_time > 86400:
            self.current_spend = 0.0
            self.request_count = 0
            self.start_time = time.time()
            
        return self.current_spend < self.daily_budget

    def get_status(self):
        """Returns the current quota status."""
        return {
            "spend": round(self.current_spend, 4),
            "budget": self.daily_budget,
            "requests": self.request_count,
            "percent": round((self.current_spend / self.daily_budget) * 100, 2) if self.daily_budget > 0 else 0
        }

# Singleton instance
quota_manager = QuotaManager()
