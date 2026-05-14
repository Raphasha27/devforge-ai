import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

# IT Specialist Best Practice: Configure structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FraudDetectionEngine")

class FraudDetectionToolkit:
    """
    Enterprise-grade Fraud Detection Toolkit for Agentic Solutions.
    Provides heuristics and risk scoring for transactional and behavioral fraud detection.
    """

    def __init__(self, risk_threshold: int = 75):
        self.risk_threshold = risk_threshold
        # In a real environment, this would connect to Redis or a Database for statefulness
        self._action_history: Dict[str, List[datetime]] = {}

    def analyze_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entrypoint for agents to pass event payloads for fraud analysis.
        """
        logger.info(f"Analyzing event for potential fraud: {event_data.get('event_id', 'UNKNOWN')}")
        
        user_id = event_data.get("user_id")
        action_type = event_data.get("action_type")
        ip_address = event_data.get("ip_address")
        
        risk_score = 0
        flags = []

        # 1. Velocity Check (e.g., Too many actions in a short timeframe)
        if user_id and self._check_velocity(user_id):
            risk_score += 40
            flags.append("HIGH_VELOCITY_ANOMALY")

        # 2. Heuristic Pattern Matching (e.g., Suspicious locations or proxies)
        if ip_address and self._is_suspicious_ip(ip_address):
            risk_score += 50
            flags.append("SUSPICIOUS_IP_DETECTED")

        # 3. Payload Integrity Analysis
        if self._has_suspicious_payload(event_data):
            risk_score += 30
            flags.append("SUSPICIOUS_PAYLOAD_STRUCTURE")

        # Final Decision Logic
        is_fraudulent = risk_score >= self.risk_threshold
        
        if is_fraudulent:
            logger.warning(f"🚨 FRAUD DETECTED: Score {risk_score} | Flags: {flags}")
        else:
            logger.info(f"✅ Event clear. Risk Score: {risk_score}")

        return {
            "is_fraudulent": is_fraudulent,
            "risk_score": risk_score,
            "flags": flags,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def _check_velocity(self, user_id: str) -> bool:
        """Tracks action velocity to prevent brute-force or bot-driven spam."""
        now = datetime.utcnow()
        history = self._action_history.get(user_id, [])
        
        # Keep only actions from the last 60 seconds
        recent_actions = [t for t in history if now - t < timedelta(seconds=60)]
        recent_actions.append(now)
        
        self._action_history[user_id] = recent_actions
        
        # If more than 10 actions in 60 seconds, flag as anomalous
        return len(recent_actions) > 10

    def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Mock check against a known malicious IP or VPN/Proxy database."""
        # IT Specialist Note: Integrate with external Threat Intel APIs (e.g., GreyNoise, MaxMind)
        known_bad_ips = {"192.168.1.99", "10.0.0.5"} # Example mock data
        return ip_address in known_bad_ips

    def _has_suspicious_payload(self, data: Dict[str, Any]) -> bool:
        """Analyzes string payloads for injection attempts or malformed inputs."""
        suspicious_keywords = ["DROP TABLE", "SELECT * FROM", "<script>", "javascript:"]
        for key, value in data.items():
            if isinstance(value, str):
                if any(keyword in value.upper() for keyword in suspicious_keywords):
                    return True
        return False

# --- Agentic Tool Integration Wrapper ---
def run_fraud_analysis_tool(event_payload: Dict[str, Any]) -> str:
    """
    Wrapper function designed to be exposed as a tool for an LLM Agent.
    """
    toolkit = FraudDetectionToolkit()
    result = toolkit.analyze_event(event_payload)
    
    if result["is_fraudulent"]:
        return f"CRITICAL: Fraud detected! Risk Score: {result['risk_score']}. Reasons: {', '.join(result['flags'])}."
    return f"Clear. Risk Score: {result['risk_score']}."

if __name__ == "__main__":
    # Quick Test / Simulation
    toolkit = FraudDetectionToolkit()
    test_event = {
        "event_id": "evt_987654",
        "user_id": "user_123",
        "action_type": "update_billing",
        "ip_address": "192.168.1.99",
        "notes": "<script>alert('hack')</script>"
    }
    print(toolkit.analyze_event(test_event))
