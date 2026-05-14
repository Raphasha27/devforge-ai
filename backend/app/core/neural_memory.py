import json

class NeuralMemory:
    """
    Simulates Ruflo's RuVector layer for persistent agent intelligence.
    Stores 'Winning Patterns' and 'Failure Modes'.
    """
    def __init__(self, storage_path: str = "neural_patterns.json"):
        self.storage_path = storage_path
        self.patterns = self._load()

    def _load(self):
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except:
            return {"success_patterns": [], "failure_modes": []}

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.patterns, f, indent=4)

    def record_success(self, repo: str, action: str, pattern: str):
        """Records a successful pattern for future retrieval."""
        self.patterns["success_patterns"].append({
            "repo": repo,
            "action": action,
            "pattern": pattern,
            "timestamp": "now"
        })
        self._save()

    def get_relevant_patterns(self, action: str):
        """Retrieves patterns relevant to the current action."""
        return [p for p in self.patterns["success_patterns"] if p["action"] == action]

# Singleton instance
neural_memory = NeuralMemory()
