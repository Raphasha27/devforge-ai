from app.agents.idea_agent import generate_market_idea
from app.agents.product_agent import productize_idea
from app.agents.architect_agent import build_architecture, generate_codebase
from app.agents.docs_agent import generate_viral_readme, generate_seo_metadata
from app.agents.security_agent import audit_codebase
from app.core.validators import quality_score, should_publish
from app.core.ecosystem import EcosystemBrain

ecosystem = EcosystemBrain()

def run_devforge_pipeline(signal: str):
    """
    The full DevForge v5 Pipeline: Signal -> Product -> Code -> Viral Launch -> Ecosystem Sync.
    """
    # 1. Idea Generation
    idea = generate_market_idea(signal)
    
    # 2. Validation & Quality Gate
    score = quality_score(idea)
    if not should_publish(score):
        return {"status": "rejected", "score": score, "reason": "Low utility score"}
        
    # 3. Productization
    product = productize_idea(idea)
    
    # 4. Architecture & Engineering
    architecture = build_architecture(product)
    codebase = generate_codebase(architecture, product)
    
    # 5. Security Audit Gate
    security_report = audit_codebase(codebase)
    if not security_report["is_safe"]:
        return {
            "status": "failed", 
            "reason": "Security vulnerability detected", 
            "risk_score": security_report["overall_risk_score"]
        }
    
    # 6. Viral Packaging (README & SEO)
    readme = generate_viral_readme(product, architecture)
    seo = generate_seo_metadata(product)
    
    # 6. Ecosystem Registration
    ecosystem.register_repo(product['product_name'], {
        "description": product['value_proposition'],
        "dependencies": architecture.get("dependencies", [])
    })
    
    return {
        "status": "success",
        "score": score,
        "product": product,
        "architecture": architecture,
        "readme": readme,
        "seo": seo,
        "security_report": security_report,
        "files_generated": list(codebase.keys())
    }
