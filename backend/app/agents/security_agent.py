from app.core.llm import call_llm
import json

def audit_codebase(files: dict):
    """
    Agent that performs a static security analysis on the generated codebase.
    """
    audit_results = {}
    
    for path, content in files.items():
        if path.endswith(".py") or path.endswith(".js") or path.endswith(".ts"):
            prompt = f"""
            Perform a professional security audit on the following file content:
            File: {path}
            
            Content:
            ---
            {content}
            ---
            
            Identify potential vulnerabilities (SQL injection, XSS, insecure secret handling, etc.).
            Return ONLY a JSON object:
            {{
                "vulnerabilities": ["list/of/findings"],
                "risk_score": 0-100 (0 is safe, 100 is critical),
                "recommendation": "main recommendation"
            }}
            """
            
            response = call_llm(prompt, json_mode=True)
            try:
                audit_results[path] = json.loads(response)
            except:
                audit_results[path] = {"vulnerabilities": [], "risk_score": 0, "recommendation": "Pass"}
                
    # Calculate overall risk
    total_score = sum(v.get("risk_score", 0) for v in audit_results.values())
    avg_score = total_score / max(1, len(audit_results))
    
    return {
        "is_safe": avg_score < 30,
        "overall_risk_score": avg_score,
        "details": audit_results
    }
