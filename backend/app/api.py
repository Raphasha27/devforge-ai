from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import json
from app.core.company_cycle import DevForgeCompany
from app.core.github_projects import GitHubProjectsClient
from app.agents.project_agent import ProjectAgent
from app.core.trend_engine import get_trending_signals
from app.core.pipeline import run_devforge_pipeline
from app.core.collaboration import collaboration_feed
from app.core.performance import performance_tracker
from app.core.neural_memory import neural_memory
from app.core.quota_manager import quota_manager
from app.agents.directive_agent import process_ceo_directive

router = APIRouter()
company = DevForgeCompany()
projects_client = GitHubProjectsClient()
project_agent = ProjectAgent()

class RepoRequest(BaseModel):
    topic: str

@router.get("/projects/{login}")
async def get_projects(login: str):
    """Fetch GitHub Projects for a user."""
    return await projects_client.get_user_projects(login)

@router.post("/projects/sync/{login}")
async def sync_projects(login: str, roadmap: list):
    """Sync DevForge roadmap to GitHub Projects."""
    return await project_agent.sync_roadmap_to_github(login, roadmap)

@router.get("/trending")
def get_trends():
    """Get latest developer demand signals."""
    return {"signals": get_trending_signals()}

@router.post("/generate")
def generate_repo(request: RepoRequest):
    """Trigger the full DevForge pipeline for a specific topic."""
    result = run_devforge_pipeline(request.topic)
    return result

@router.post("/company-cycle")
async def run_company_cycle():
    """Run the DevForge Company Simulation (v6)."""
    result = await company.execute_business_cycle()
    return result

@router.post("/autopilot")
def run_autopilot(background_tasks: BackgroundTasks):
    """Run DevForge in fully autonomous mode for the next set of trending signals."""
    signals = get_trending_signals()
    for signal in signals:
        background_tasks.add_task(run_devforge_pipeline, signal)
    return {"status": "autopilot_started", "signals": signals}

@router.get("/collaboration")
def get_collaboration():
    """Get the internal agent collaboration feed."""
    return {"messages": collaboration_feed.get_feed()}

@router.get("/governance/pending")
def get_pending_actions():
    """Get all high-risk actions pending human approval."""
    return {"pending": company.governance.queue.get_pending()}

@router.post("/governance/approve/{suggestion_id}")
def approve_action(suggestion_id: int):
    """Approve a pending high-risk action."""
    # In a real scenario, this would trigger the actual execution.
    # For v1, we just update the status.
    from app.core.evolution_queue import SuggestionStatus
    item = company.governance.queue.update_status(suggestion_id, SuggestionStatus.APPROVED)
    return {"status": "approved", "item": item}

@router.get("/events")
def get_events():
    """Get the live ecosystem event stream."""
    return {"events": company.governance.events.get_recent()}

@router.get("/ecosystem/graph")
def get_ecosystem_graph():
    """Get the visual dependency graph of the ecosystem."""
    nodes = [{"id": n} for n in company.governance.ecosystem.graph.nodes()]
    links = [{"source": u, "target": v} for u, v in company.governance.ecosystem.graph.edges()]
    return {"nodes": nodes, "links": links}

@router.get("/market-sentiment")
def get_market_sentiment():
    """Get the latest developer market sentiment intelligence."""
    return company.current_sentiment

@router.get("/performance")
def get_performance():
    """Get the autonomous company performance scorecard."""
    return performance_tracker.get_scorecard()

@router.get("/quota")
def get_quota():
    """Get the live API quota and cost status."""
    return quota_manager.get_status()

@router.get("/ecosystem/markets")
def get_ecosystem_markets():
    """Get the discovered 'Blue Ocean' market opportunities."""
    return company.blue_ocean_markets

@router.get("/neural-memory")
def get_neural_memory():
    """Get the persistent neural patterns and intelligence."""
    return neural_memory.patterns

class DirectiveRequest(BaseModel):
    directive: str

@router.post("/swarm/directive")
async def issue_directive(request: DirectiveRequest):
    """Issue a high-level directive to the swarm (Human CEO only)."""
    plan = process_ceo_directive(request.directive)
    collaboration_feed.post_message("CEO", f"🚨 HUMAN DIRECTIVE RECEIVED: {request.directive}")
    collaboration_feed.post_message("System", f"Delegating tasks: {json.dumps(plan['delegation'])}")
    company.governance.events.emit("ceo_directive_issued", {"directive": request.directive, "plan": plan})
    return {"status": "delegated", "plan": plan}
