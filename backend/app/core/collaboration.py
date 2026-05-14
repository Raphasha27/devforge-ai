from app.core.db import SessionLocal, DBMessage

class CollaborationEngine:
    """
    Simulates internal agent communication (Slack-style).
    Transforms technical audit logs into human-readable collaboration messages.
    """
    def __init__(self):
        self.agent_profiles = {
            "CEO": "👔",
            "CTO": "💻",
            "Architect": "🏗️",
            "Security": "🛡️",
            "Governance": "⚖️",
            "System": "🤖"
        }

    def post_message(self, actor: str, text: str, channel: str = "general"):
        """
        Posts a message to the internal collaboration feed (Persisted).
        """
        db = SessionLocal()
        db_msg = DBMessage(
            actor=actor,
            emoji=self.agent_profiles.get(actor, "🤖"),
            text=text,
            channel=channel
        )
        db.add(db_msg)
        db.commit()
        db.refresh(db_msg)
        db.close()
        return db_msg

    def get_feed(self, limit: int = 50):
        """
        Returns the latest collaboration messages from the database.
        """
        db = SessionLocal()
        messages = db.query(DBMessage).order_by(DBMessage.timestamp.desc()).limit(limit).all()
        db.close()
        return messages

# Singleton instance
collaboration_feed = CollaborationEngine()
