from fastapi import APIRouter, HTTPException
from app.core.evolution_queue import EvolutionQueue, SuggestionStatus
from app.core.event_stream import EventStream
from app.core.audit import AuditLog

router = APIRouter()
queue = EvolutionQueue()
events = EventStream()
audit = AuditLog()

@router.get("/pending")
def list_pending():
    """List all AI suggestions awaiting approval."""
    return {"suggestions": queue.get_pending()}

@router.post("/approve/{suggestion_id}")
def approve_suggestion(suggestion_id: int):
    """Approve a suggestion for execution."""
    item = queue.update_status(suggestion_id, SuggestionStatus.APPROVED)
    if not item:
        raise HTTPException(status_code=404, detail="Suggestion not found")
        
    audit.log_action("human", "approve_suggestion", {"id": suggestion_id, "repo": item['repo']})
    events.emit("suggestion_approved", {"id": suggestion_id, "repo": item['repo']})
    
    return {"status": "approved", "item": item}

@router.post("/reject/{suggestion_id}")
def reject_suggestion(suggestion_id: int):
    """Reject and dismiss a suggestion."""
    item = queue.update_status(suggestion_id, SuggestionStatus.REJECTED)
    if not item:
        raise HTTPException(status_code=404, detail="Suggestion not found")
        
    audit.log_action("human", "reject_suggestion", {"id": suggestion_id, "repo": item['repo']})
    events.emit("suggestion_rejected", {"id": suggestion_id, "repo": item['repo']})
    
    return {"status": "rejected"}

@router.get("/events")
def get_live_events():
    """Get the live event stream."""
    return {"events": events.get_recent()}
