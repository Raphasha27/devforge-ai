import logging
from datetime import datetime

class AuditLog:
    """
    Persistence-ready audit logger for all DevForge actions.
    Ensures absolute transparency of AI behavior.
    """
    def __init__(self, log_file: str = "devforge_audit.log"):
        self.logger = logging.getLogger("DevForgeAudit")
        self.logger.setLevel(logging.INFO)
        
        # Simple file handler
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_action(self, actor: str, action: str, details: dict):
        """
        Logs a specific action taken by an agent or human.
        """
        log_entry = {
            "actor": actor,
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.info(str(log_entry))
        print(f"[AUDIT] {actor} performed {action}")
