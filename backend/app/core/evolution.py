from enum import Enum
from typing import Dict, List

class EvolutionAction(Enum):
    MAINTAIN = "maintain"
    REFACTOR = "refactor"
    EXPAND = "expand"
    SIMPLIFY = "simplify"
    SPLIT = "split"
    MERGE = "merge"

class EvolutionEngine:
    """
    The Evolution Brain of DevForge v7.
    Decides how repositories should mutate based on reality signals.
    """
    def __init__(self):
        self.history = []

    def collect_signals(self, repo_stats: dict) -> dict:
        """
        Processes raw metrics into actionable evolution signals.
        """
        return {
            "adoption_velocity": repo_stats.get("stars_delta", 0),
            "pain_index": repo_stats.get("open_issues", 0),
            "stability_index": 1.0 - (repo_stats.get("failed_builds", 0) / max(1, repo_stats.get("total_builds", 1))),
            "bloat_factor": repo_stats.get("lines_of_code", 0) / 1000.0
        }

    def decide_evolution(self, signals: dict) -> EvolutionAction:
        """
        Decision logic for repo mutation.
        """
        if signals["stability_index"] < 0.7:
            return EvolutionAction.REFACTOR
            
        if signals["adoption_velocity"] > 5 and signals["pain_index"] > 3:
            return EvolutionAction.EXPAND
            
        if signals["bloat_factor"] > 10:
            return EvolutionAction.SPLIT
            
        if signals["adoption_velocity"] < 1 and signals["pain_index"] == 0:
            return EvolutionAction.SIMPLIFY
            
        return EvolutionAction.MAINTAIN

    def plan_mutation(self, repo_name: str, action: EvolutionAction):
        """
        Generates a mutation plan for the engineering agents.
        """
        plans = {
            EvolutionAction.REFACTOR: "Identify complex functions and modularize code. Improve type safety.",
            EvolutionAction.EXPAND: "Add 2 new high-demand features requested in issues. Update CLI interface.",
            EvolutionAction.SIMPLIFY: "Remove unused dependencies and legacy code paths to reduce binary size.",
            EvolutionAction.SPLIT: "Extract core logic into a separate shared library and refactor original repo to use it.",
            EvolutionAction.MERGE: "Combine with overlapping repository to reduce maintenance overhead."
        }
        
        return plans.get(action, "Continue standard maintenance.")
