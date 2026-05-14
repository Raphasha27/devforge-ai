from app.core.db import SessionLocal, DBSuggestion

class SuggestionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"

class EvolutionQueue:
    """
    Queue Manager for AI-generated evolution suggestions.
    Ensures human-in-the-loop control for all changes.
    """
    def add_suggestion(self, repo: str, suggestion_text: str, risk_level: str = "Low"):
        """
        Adds a new suggestion to the pending queue (Persisted).
        """
        db = SessionLocal()
        db_item = DBSuggestion(
            repo=repo,
            suggestion=suggestion_text,
            risk=risk_level,
            status=SuggestionStatus.PENDING.value
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        db.close()
        return db_item

    def update_status(self, suggestion_id: int, status: SuggestionStatus):
        """
        Updates the status of a suggestion in the database.
        """
        db = SessionLocal()
        item = db.query(DBSuggestion).filter(DBSuggestion.id == suggestion_id).first()
        if item:
            item.status = status.value
            db.commit()
            db.refresh(item)
        db.close()
        return item

    def get_pending(self) -> List[Dict]:
        """
        Returns all pending suggestions from the database.
        """
        db = SessionLocal()
        items = db.query(DBSuggestion).filter(DBSuggestion.status == SuggestionStatus.PENDING.value).all()
        db.close()
        return items
