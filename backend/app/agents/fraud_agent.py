import json
from app.core.llm import call_llm
from app.core.fraud_detection import FraudDetectionToolkit

class FraudAnalysisAgent:
    """
    RAG-powered AI Agent for Fraud Detection.
    It takes an event, uses the FraudDetectionToolkit to gather raw heuristic signals,
    'retrieves' relevant organizational context, and uses Generative AI to make a final 
    fraud assessment and recommended action plan.
    """
    
    def __init__(self):
        self.toolkit = FraudDetectionToolkit()
        
    def _retrieve_context(self, user_id: str, ip_address: str) -> str:
        """
        Mocks a RAG retrieval process. In production, this would query a VectorDB 
        (like Pinecone or Chroma) for past fraud incidents, known threat actors, or 
        historical user behavior patterns.
        """
        # Mocking retrieved vector context
        retrieved_docs = [
            f"Doc 1: User {user_id} was previously flagged for high velocity credential stuffing.",
            f"Doc 2: IPs matching {ip_address} subnet have been associated with recent proxy abuse.",
            "Doc 3: Standard organizational policy requires manual review for risk scores > 60."
        ]
        return "\n".join(retrieved_docs)

    def analyze_and_act(self, event_payload: dict) -> dict:
        """
        The main agentic loop: 
        1. Run heuristics (Toolkit)
        2. Retrieve context (RAG)
        3. Generate analysis and action (LLM)
        """
        # Step 1: Get raw heuristic signals from the toolkit
        toolkit_results = self.toolkit.analyze_event(event_payload)
        
        # Step 2: Retrieve RAG context based on event data
        user_id = event_payload.get("user_id", "unknown")
        ip = event_payload.get("ip_address", "unknown")
        context = self._retrieve_context(user_id, ip)
        
        # Step 3: Use Generative AI to synthesize findings and decide on an action
        prompt = f"""
        Act as an Expert Fraud Intelligence Analyst. You are evaluating a potential security incident.
        
        ### 1. Toolkit Signals (Heuristics)
        - Risk Score: {toolkit_results['risk_score']}
        - Is Fraudulent: {toolkit_results['is_fraudulent']}
        - Flags: {', '.join(toolkit_results['flags']) if toolkit_results['flags'] else 'None'}
        
        ### 2. Retrieved Historical Context (RAG)
        {context}
        
        ### 3. Event Payload
        ```json
        {json.dumps(event_payload, indent=2)}
        ```
        
        Based on the heuristic signals, the historical RAG context, and the raw event payload, 
        provide a comprehensive fraud assessment.
        
        Return ONLY a JSON object with the following schema:
        {{
            "final_assessment": "Detailed explanation of the risk.",
            "confidence_level": "High/Medium/Low",
            "recommended_action": "BLOCK | FLAG_FOR_REVIEW | ALLOW",
            "justification": "Why this action is recommended based on the data."
        }}
        """
        
        llm_response = call_llm(prompt, json_mode=True)
        
        try:
            ai_decision = json.loads(llm_response)
        except json.JSONDecodeError:
            ai_decision = {
                "final_assessment": "Failed to parse LLM response.",
                "confidence_level": "Low",
                "recommended_action": "FLAG_FOR_REVIEW",
                "justification": "Failsafe triggered due to LLM error."
            }
            
        # Combine toolkit results with AI generative insights
        return {
            "event_id": event_payload.get("event_id"),
            "heuristic_results": toolkit_results,
            "ai_analysis": ai_decision
        }

if __name__ == "__main__":
    # Test the agent execution
    agent = FraudAnalysisAgent()
    test_event = {
        "event_id": "tx_99912",
        "user_id": "usr_772",
        "action_type": "checkout",
        "ip_address": "192.168.1.99",
        "notes": "urgent request <script>steal_cookie()</script>"
    }
    
    result = agent.analyze_and_act(test_event)
    print(json.dumps(result, indent=2))
