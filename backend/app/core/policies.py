class GovernancePolicy:
    """
    Defines the 'Rules of the Road' for the DevForge Ecosystem.
    """
    STRICT_TYPESCRIPT = True
    MAX_REPOS_PER_DOMAIN = 5
    MIN_HEALTH_SCORE = 70
    AUTO_FIX_SECURITY = True
    FORBIDDEN_DEPENDENCIES = ["insecure-lib-xyz"]
    LEGACY_STACKS = ["flask", "javascript"]
    RECOMMENDED_STACKS = ["fastapi", "typescript"]

    @classmethod
    def check_compliance(cls, repo_name: str, intelligence: dict):
        """
        Checks if a repository complies with current policies.
        """
        issues = []
        stack = [s.lower() for s in intelligence.get("tech_stack", [])]
        
        # Policy: Legacy Stack
        for legacy in cls.LEGACY_STACKS:
            if legacy in stack:
                issues.append(f"Legacy stack detected: {legacy}. Migration recommended.")
        
        # Policy: Max repos
        # (Simplified check)
        
        # Policy: Forbidden deps
        for dep in intelligence.get("inferred_dependencies", []):
            if dep in cls.FORBIDDEN_DEPENDENCIES:
                issues.append(f"Forbidden dependency found: {dep}")
                
        return {
            "compliant": len(issues) == 0,
            "issues": issues
        }
