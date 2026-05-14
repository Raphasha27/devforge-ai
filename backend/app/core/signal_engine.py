def compute_repo_health(repo_data: dict):
    """
    Computes a health score based on real GitHub signals.
    """
    stars = repo_data.get("stargazers_count", 0)
    issues = repo_data.get("open_issues_count", 0)
    forks = repo_data.get("forks_count", 0)
    watchers = repo_data.get("watchers_count", 0)
    updated_at = repo_data.get("updated_at", "")
    
    # Heuristic scoring
    score = (stars * 10) + (forks * 20) + (watchers * 5)
    
    # Penalize for many open issues
    score -= (issues * 15)
    
    # Normalize or cap the score
    normalized_score = max(0, min(100, score / 10))
    
    return {
        "repo": repo_data.get("name"),
        "health_score": normalized_score,
        "metrics": {
            "stars": stars,
            "issues": issues,
            "forks": forks
        },
        "status": "healthy" if normalized_score > 70 else "needs_attention" if normalized_score > 40 else "critical"
    }
