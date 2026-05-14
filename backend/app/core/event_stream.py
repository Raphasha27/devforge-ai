from datetime import datetime
from typing import List, Dict

class EventStream:
    """
    Live Event Stream Engine for DevForge v8.
    Captures all ecosystem activities in real-time.
    """
    def __init__(self):
        self.events: List[Dict] = []

    def emit(self, event_type: str, payload: dict):
        """
        Emits a new event into the stream.
        """
        event = {
            "id": len(self.events) + 1,
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.events.append(event)
        # Keep only the last 1000 events to manage memory
        if len(self.events) > 1000:
            self.events = self.events[-1000:]
            
        print(f"[EVENT] {event_type}: {payload.get('repo', 'N/A')}")

    def get_recent(self, limit: int = 50) -> List[Dict]:
        """
        Retrieves the most recent events.
        """
        return self.events[-limit:]
