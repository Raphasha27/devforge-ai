from app.core.db import SessionLocal, DBRepo
import networkx as nx
from typing import List, Dict

class EcosystemBrain:
    """
    Ecosystem Intelligence Engine for DevForge v5.
    Manages relationships, dependencies, and impact analysis across all repositories.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self._sync_graph_from_db()

    def _sync_graph_from_db(self):
        """Loads all repos from DB to build the memory graph."""
        db = SessionLocal()
        repos = db.query(DBRepo).all()
        for repo in repos:
            self.graph.add_node(repo.name)
            deps = repo.metadata_json.get("dependencies", [])
            for dep in deps:
                self.graph.add_edge(repo.name, dep)
        db.close()

    def register_repo(self, repo_name: str, metadata: dict):
        """
        Adds a repository to the ecosystem and persists it to the database.
        """
        db = SessionLocal()
        existing = db.query(DBRepo).filter(DBRepo.name == repo_name).first()
        
        if existing:
            existing.metadata_json = metadata
            existing.health_score = metadata.get("health_score", 100)
        else:
            new_repo = DBRepo(
                name=repo_name,
                metadata_json=metadata,
                health_score=metadata.get("health_score", 100)
            )
            db.add(new_repo)
            
        db.commit()
        db.close()
        
        # Update memory graph
        self.graph.add_node(repo_name)
        for dep in metadata.get("dependencies", []):
            self.graph.add_edge(repo_name, dep)

    def get_active_repos(self) -> List[str]:
        """Returns a list of all repo names in the ecosystem."""
        return list(self.graph.nodes())

    def analyze_impact(self, changed_repo: str) -> List[str]:
        """
        Identifies which repositories are affected when a specific repo changes.
        Uses reverse traversal of the dependency graph.
        """
        if changed_repo not in self.graph:
            return []
            
        # Repos that depend on the changed repo
        affected = list(self.graph.predecessors(changed_repo))
        return affected

    def detect_ecosystem_patterns(self, all_repo_issues: Dict[str, List[str]]) -> Dict[str, int]:
        """
        Detects systemic issues across the entire ecosystem.
        """
        patterns = {}
        for repo, issues in all_repo_issues.items():
            for issue in issues:
                # Simple keyword-based pattern detection
                category = "general"
                if "performance" in issue.lower() or "slow" in issue.lower():
                    category = "performance"
                elif "security" in issue.lower() or "vulnerability" in issue.lower():
                    category = "security"
                elif "docs" in issue.lower() or "readme" in issue.lower():
                    category = "documentation"
                
                patterns[category] = patterns.get(category, 0) + 1
                
        return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))

    def get_release_order(self) -> List[str]:
        """
        Calculates the optimal release order using topological sort.
        Dependencies must be released/updated before dependents.
        """
        try:
            # Topological sort returns nodes in order such that for edge (u, v), u comes before v.
            # In our graph, edge (dependent -> dependency).
            # So we want dependencies first.
            return list(reversed(list(nx.topological_sort(self.graph))))
        except nx.NetworkXUnfeasible:
            # Cycle detected
            return list(self.graph.nodes())
