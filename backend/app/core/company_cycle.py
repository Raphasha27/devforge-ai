from app.agents.ceo_agent import generate_ceo_strategy
from app.agents.cto_agent import get_architectural_standards, generate_roadmap
from app.core.trend_engine import get_trending_signals
from app.core.pipeline import run_devforge_pipeline, ecosystem
from app.core.governance import GovernanceAgent
from app.core.collaboration import collaboration_feed
from app.core.notifications import notifier
from app.agents.sentiment_agent import analyze_market_sentiment
from app.core.performance import performance_tracker
from app.agents.growth_agent import generate_growth_campaign
from app.agents.market_strategist import find_blue_ocean_markets

class DevForgeCompany:
    """
    Company Simulation Engine (v6).
    Coordinates CEO, CTO, and PM to drive autonomous engineering cycles.
    """
    def __init__(self):
        self.current_strategy = {}
        self.current_sentiment = {}
        self.blue_ocean_markets = []
        self.standards = {}
        self.roadmap = []
        self.governance = GovernanceAgent()

    async def execute_business_cycle(self):
        """
        Runs a full company cycle from strategy to execution.
        """
        # 0. Intel: Market Sentiment Analysis
        collaboration_feed.post_message("CEO", "Scanning developer forums for market sentiment...")
        self.current_sentiment = analyze_market_sentiment()
        collaboration_feed.post_message("CEO", f"Market Vibe: {self.current_sentiment['vibe']} ({self.current_sentiment['sentiment_score']}/100)")

        # 0.5 Discovery: Blue Ocean Market Scanning
        collaboration_feed.post_message("CEO", "Analyzing technical gaps for Blue Ocean opportunities...")
        discovery = find_blue_ocean_markets()
        self.blue_ocean_markets = discovery.get("markets", [])
        for m in self.blue_ocean_markets:
            collaboration_feed.post_message("CEO", f"New Market Discovered: {m['name']} (Gap: {m['gap']})")
            self.governance.events.emit("market_discovered", m)

        # 1. CEO: Market Analysis & Strategy
        collaboration_feed.post_message("CEO", "Initiating market trend analysis for this cycle.")
        await notifier.notify("Cycle Start", "DevForge Business Cycle has been initiated.")
        signals = get_trending_signals()
        self.current_strategy = generate_ceo_strategy(signals)
        collaboration_feed.post_message("CEO", f"Strategy finalized: focusing on {', '.join(self.current_strategy['focus_areas'][:2])}...")
        
        # 2. CTO: Technical Standards
        collaboration_feed.post_message("CTO", "Updating architectural standards based on new directive.")
        self.standards = get_architectural_standards(self.current_strategy)
        
        # 3. PM: Roadmap Generation
        collaboration_feed.post_message("System", "Building project roadmap...")
        roadmap_data = generate_roadmap(self.current_strategy)
        self.roadmap = roadmap_data.get("roadmap", [])
        
        # 4. Engineering & Launch
        execution_results = []
        for task in self.roadmap:
            if task['priority'] == 'High':
                collaboration_feed.post_message("Architect", f"Starting build for: {task['item']}")
                # Execute pipeline for high priority tasks
                result = run_devforge_pipeline(task['item'])
                execution_results.append(result)
                if result.get("status") == "success":
                    collaboration_feed.post_message("System", f"Successfully launched {result['product']['product_name']} 🚀")
                    performance_tracker.record_launch(True)
                    performance_tracker.increment_mrr(100)
                    
                    # 4.1 Growth Hacking
                    collaboration_feed.post_message("Growth", f"Launching viral campaign for {result['product']['product_name']}...")
                    campaign = generate_growth_campaign(
                        result['product']['product_name'], 
                        result['product']['value_proposition'],
                        result.get('files_generated', [])
                    )
                    self.governance.events.emit("growth_campaign_launched", {
                        "repo": result['product']['product_name'],
                        "campaign": campaign
                    })
                else:
                    collaboration_feed.post_message("Security", f"Build REJECTED for {task['item']}: {result.get('reason')}")
                    performance_tracker.record_launch(False)
                
        # 5. Ecosystem Governance & Evolution
        collaboration_feed.post_message("Governance", "Starting ecosystem health audit...")
        active_repos = ecosystem.get_active_repos()
        evolution_results = self.governance.run_ecosystem_audit(active_repos, self.current_sentiment)
        
        for e in evolution_results:
            if e['action'] != 'maintain':
                collaboration_feed.post_message("Governance", f"Triggering {e['action']} for {e['repo']}")
                performance_tracker.record_evolution(25) # Mock impact score
                
        return {
            "strategy": self.current_strategy,
            "roadmap": self.roadmap,
            "results": execution_results,
            "evolution": evolution_results
        }
