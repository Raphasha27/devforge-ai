import os
import httpx

class NotificationAgent:
    """
    Handles external notifications (Slack, Discord, Webhooks).
    """
    def __init__(self):
        self.webhook_url = os.getenv("NOTIFY_WEBHOOK_URL")

    async def notify(self, title: str, message: str, level: str = "info"):
        """
        Sends a notification to the configured webhook.
        """
        if not self.webhook_url:
            print(f"[NOTIFY] No webhook configured. Simulation: {title} - {message}")
            return
            
        payload = {
            "text": f"*{title}*\n{message}",
            "level": level
        }
        
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.webhook_url, json=payload)
            except Exception as e:
                print(f"[NOTIFY] Failed to send notification: {str(e)}")

# Singleton instance
notifier = NotificationAgent()
