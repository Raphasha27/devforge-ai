def generate_ecosystem_badges(repo_name: str, health_score: float, security_score: float, action_status: str):
    """
    Generates dynamic Markdown badges for repository health and status.
    """
    # Color mapping for health
    health_color = "00FF9C" if health_score > 80 else "FFA500" if health_score > 50 else "FF4B4B"
    security_color = "00FF9C" if security_score > 80 else "FFA500" if security_score > 50 else "FF4B4B"
    
    # Color mapping for action
    action_color = "00D1FF" if action_status == "maintain" else "BD00FF"
    
    badges = [
        f"![Health Score](https://img.shields.io/badge/DevForge_Health-{int(health_score)}%25-{health_color}?style=flat-square)",
        f"![Security Score](https://img.shields.io/badge/Security_Score-{int(security_score)}%25-{security_color}?style=flat-square)",
        f"![Evolution Status](https://img.shields.io/badge/Evolution-{action_status.upper()}-{action_color}?style=flat-square)",
        "![Governance](https://img.shields.io/badge/Governance-Autonomous-lightgrey?style=flat-square)"
    ]
    
    return " ".join(badges)

def inject_badges_into_readme(readme_content: str, repo_name: str, health_score: float, security_score: float, action_status: str):
    """
    Injects or updates the DevForge health block in a README.
    """
    badges = generate_ecosystem_badges(repo_name, health_score, security_score, action_status)
    header_block = f"<!-- DEVFORGE_HEALTH_START -->\n{badges}\n<!-- DEVFORGE_HEALTH_END -->"
    
    if "<!-- DEVFORGE_HEALTH_START -->" in readme_content:
        # Update existing
        import re
        pattern = r"<!-- DEVFORGE_HEALTH_START -->.*?<!-- DEVFORGE_HEALTH_END -->"
        return re.sub(pattern, header_block, readme_content, flags=re.DOTALL)
    else:
        # Prepend to readme
        return header_block + "\n\n" + readme_content
