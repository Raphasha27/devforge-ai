import pytest
from app.core.evolution import EvolutionEngine, EvolutionAction

def test_evolution_decision():
    engine = EvolutionEngine()
    # Mock high activity signals
    signals = {
        "stars_delta": 20,
        "issues_count": 5,
        "forks_count": 2
    }
    action = engine.decide_evolution(signals)
    assert action in [EvolutionAction.REFINE, EvolutionAction.SPLIT]

def test_badge_generation():
    from app.core.badges import generate_ecosystem_badges
    badges = generate_ecosystem_badges("test-repo", 90.0, 95.0, "maintain")
    assert "Health Score" in badges
    assert "90%" in badges
    assert "Security Score" in badges
