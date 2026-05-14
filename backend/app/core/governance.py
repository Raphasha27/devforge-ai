from app.core.github import GithubPublisher
from app.core.evolution import EvolutionEngine, EvolutionAction
from app.core.ecosystem import EcosystemBrain
from app.agents.refactor_agent import generate_mutation_code
from app.agents.scanner_agent import scan_repo_intelligence
from app.agents.review_agent import review_pull_request
from app.agents.tech_debt_agent import scan_tech_debt
from app.agents.migration_agent import plan_stack_migration
from app.agents.changelog_agent import generate_viral_changelog
from app.agents.debug_agent import investigate_build_failure
from app.core.badges import inject_badges_into_readme
from app.core.evolution_queue import EvolutionQueue
from app.core.event_stream import EventStream
from app.core.policies import GovernancePolicy
from app.core.plm import ProductLifecycleManager, LifecycleAction
from app.core.consensus import swarm_consensus, ConsensusResult
from app.core.neural_memory import neural_memory
from app.core.collaboration import collaboration_feed

class GovernanceAgent:
    """
    Automated Governance & Evolution Agent.
    Orchestrates ecosystem health checks and triggers repo mutations.
    """
    def __init__(self):
        self.publisher = GithubPublisher()
        self.engine = EvolutionEngine()
        self.ecosystem = EcosystemBrain()
        self.queue = EvolutionQueue()
        self.events = EventStream()
        self.plm = ProductLifecycleManager()

    def run_ecosystem_audit(self, registered_repos: list, market_sentiment: dict = None):
        """
        Audits all registered repositories and triggers evolution if necessary.
        """
        audit_results = []
        market_sentiment = market_sentiment or {}
        
        for repo_name in registered_repos:
            # ... (steps 1-4 same)
            stats = self.publisher.get_repo_stats(repo_name)
            if "error" in stats: continue
            # 2. Process signals
            signals = self.engine.collect_signals(stats)
            
            # 3. Deep Intelligence Scan
            # Mocking current_files for scan
            current_files = {"src/main.py": "# Mock logic"} 
            intelligence = scan_repo_intelligence(repo_name, current_files)
            
            # 4. Decide evolution action (v2: could use intelligence too)
            action = self.engine.decide_evolution(signals)
            plan = self.engine.plan_mutation(repo_name, action)
            
            # 5. Emit Event
            self.events.emit("audit_performed", {
                "repo": repo_name,
                "action": action.value,
                "intelligence": intelligence
            })
            
            # 6. Policy Compliance Check
            compliance = GovernancePolicy.check_compliance(repo_name, intelligence)
            if not compliance["compliant"]:
                self.events.emit("policy_violation", {
                    "repo": repo_name,
                    "issues": compliance["issues"]
                })
                collaboration_feed.post_message("Governance", f"⚠️ Policy violation detected in {repo_name}!")
            
            # 7. Tech Debt Liquidation Check
            debt_report = scan_tech_debt(repo_name, current_files)
            if debt_report["debt_score"] > 50:
                self.events.emit("tech_debt_detected", {
                    "repo": repo_name,
                    "score": debt_report["debt_score"],
                    "plan": debt_report["liquidation_plan"]
                })
                collaboration_feed.post_message("CTO", f"High technical debt detected in {repo_name}. Liquidation plan ready.")

            # 8. Tech Stack Migration Check
            for legacy in GovernancePolicy.LEGACY_STACKS:
                if legacy in [s.lower() for s in intelligence.get("tech_stack", [])]:
                    self.events.emit("migration_initiated", {"repo": repo_name, "legacy": legacy})
                    mig_plan = plan_stack_migration(repo_name, intelligence["tech_stack"], GovernancePolicy.RECOMMENDED_STACKS[0])
                    self.events.emit("migration_plan_ready", {
                        "repo": repo_name,
                        "target": mig_plan["target"],
                        "steps": mig_plan["steps"]
                    })
                    collaboration_feed.post_message("Architect", f"Legacy stack ({legacy}) detected in {repo_name}. Migration plan to {mig_plan['target']} drafted.")
                    break

            # 9. Self-Correction Check (Build Repairs)
            if stats.get("failed_builds", 0) > 0:
                self.events.emit("build_repair_initiated", {"repo": repo_name})
                fix_proposal = investigate_build_failure(repo_name, "Build timed out or tests failed.") # Mock logs
                self.events.emit("build_repair_plan", {
                    "repo": repo_name,
                    "cause": fix_proposal["root_cause"],
                    "fix": fix_proposal["proposed_fix"]
                })
                collaboration_feed.post_message("System", f"🛠️ Build failure in {repo_name}! DebugAgent is investigating...")

            # 9. Product Lifecycle Management
            lifecycle_action, reason = self.plm.decide_lifecycle(repo_name, stats, market_sentiment)
            stage = self.plm.get_stage(stats)
            if lifecycle_action != LifecycleAction.MAINTAIN:
                self.events.emit("lifecycle_recommendation", {
                    "repo": repo_name,
                    "action": lifecycle_action.value,
                    "reason": reason
                })
                collaboration_feed.post_message("CEO", f"Lifecycle Alert for {repo_name}: Recommended {lifecycle_action.value.upper()}. Reason: {reason}")

            # 10. Record result
            audit_results.append({
                "repo": repo_name,
                "action": action.value,
                "plan": plan,
                "stats": stats,
                "stage": stage
            })
            
            # 8. Audit Pull Requests
            self.audit_pull_requests(repo_name)
            
            # 9. Execute maintenance or Queue for approval
            if action != EvolutionAction.MAINTAIN:
                if action in [EvolutionAction.SPLIT, EvolutionAction.MERGE]:
                    # High risk actions go to queue
                    self.queue.add_suggestion(repo_name, plan, risk_level="High")
                    print(f"[GOVERNANCE] High-risk action {action.value} queued for approval.")
                else:
                    # Low risk actions are executed immediately
                    self.execute_evolution_pr(repo_name, action, plan)
                
        return audit_results

    def audit_pull_requests(self, repo_name: str):
        """
        Scans for open pull requests and performs autonomous AI reviews.
        """
        prs = self.publisher.get_open_prs(repo_name)
        for pr in prs:
            # Simple check to avoid double-commenting
            # (In real v2, we would check if DevForge has already commented)
            print(f"[GOVERNANCE] Reviewing PR #{pr.number} for {repo_name}...")
            
            review = review_pull_request(
                repo_name=repo_name,
                pr_title=pr.title,
                pr_body=pr.body or "",
                diff_content="Mock diff content for v1" # In real, fetch PR diff
            )
            
            self.publisher.comment_on_pr(repo_name, pr.number, review)
            collaboration_feed.post_message("Security", f"Autonomous review posted on {repo_name} PR #{pr.number}")
            self.events.emit("pr_reviewed", {"repo": repo_name, "pr": pr.number})

    def execute_evolution_pr(self, repo_name: str, action: EvolutionAction, plan: str):
        """
        Executes a mutation by refactoring code after reaching Swarm Consensus.
        """
        print(f"[GOVERNANCE] Initiating Swarm Consensus for {repo_name}...")
        
        # 0. Swarm Vote (CEO, CTO, Architect)
        votes = [True, True, False] # Mocked votes: CEO(T), CTO(T), Architect(F)
        result = swarm_consensus.evaluate_action(votes)
        
        if result != ConsensusResult.APPROVED:
            collaboration_feed.post_message("Security", f"Swarm Consensus FAILED for {repo_name}. Aborting {action.value}.")
            self.events.emit("consensus_failed", {"repo": repo_name, "action": action.value})
            return {"status": "rejected", "reason": "No consensus"}

        collaboration_feed.post_message("System", f"Swarm Consensus REACHED for {repo_name}. Executing {action.value}...")
        
        try:
            # ... (mutation logic)
            # Record success in Neural Memory
            neural_memory.record_success(repo_name, action.value, plan)
            
            # Fetch current files (mocking for v1, in real it would use self.publisher.gh.get_repo(repo_name).get_contents(""))
            current_files = {
                "src/main.py": "# Core logic\ndef run(): pass",
                "README.md": f"# {repo_name}\nManaged by DevForge AI."
            }
            
            # Generate mutated code
            mutated_files = generate_mutation_code(repo_name, current_files, plan)
            
            # 1. Generate Viral Changelog
            changelog_data = generate_viral_changelog(repo_name, "2.0", [plan])
            changelog_content = f"# {changelog_data['title']}\n\n## TL;DR\n{changelog_data['tldr']}\n\n## Updates\n" + "\n".join([f"- {u}" for u in changelog_data['updates']])
            mutated_files["CHANGELOG.md"] = changelog_content
            self.events.emit("changelog_generated", {"repo": repo_name, "title": changelog_data['title']})

            # Inject Health Badges into README
            if "README.md" in mutated_files:
                # Mock scores based on metrics
                health_score = 85.0 
                security_score = 92.0
                mutated_files["README.md"] = inject_badges_into_readme(
                    mutated_files["README.md"], 
                    repo_name, 
                    health_score, 
                    security_score,
                    action.value
                )
            
            # Push to a dedicated evolution branch
            branch_name = f"devforge-evolution-{action.value}"
            self.publisher.push_files(
                repo_name=repo_name,
                files=mutated_files,
                commit_message=f"Ecosystem Evolution: {action.value}\n\nPlan: {plan}"
            )
            return {"status": "success", "branch": branch_name}
        except Exception as e:
            print(f"[GOVERNANCE] Mutation failed for {repo_name}: {str(e)}")
            return {"status": "failed", "error": str(e)}
