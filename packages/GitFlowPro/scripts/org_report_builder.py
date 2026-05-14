import os
import json
import requests
from datetime import datetime

try:
    import yaml
except ImportError:
    raise SystemExit("Missing dependency: pyyaml. Add it to requirements.txt")

POLICY_PATH = "governance/v3/policies/policy.yml"

def load_policy():
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def gh_get(url, token):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    return requests.get(url, headers=headers)

def classify_repo_risk(repo_name, policy):
    return "risk:medium"

def governance_score(workflow_count, security_alerts):
    score = 100
    if workflow_count == 0: score -= 30
    if security_alerts > 0: score -= min(50, security_alerts * 10)
    return max(0, score)

def main():
    token = os.getenv("GH_TOKEN")
    org = os.getenv("ORG_NAME")
    if not token or not org:
        raise SystemExit("Missing GH_TOKEN or ORG_NAME")
    policy = load_policy()
    repos_url = f"https://api.github.com/orgs/{org}/repos?per_page=100"
    repos_resp = gh_get(repos_url, token)
    if repos_resp.status_code >= 300:
        raise SystemExit(f"GitHub API error: {repos_resp.text}")
    repos = repos_resp.json()
    report_repos = []
    high = med = low = 0
    for repo in repos:
        repo_full = f"{org}/{repo['name']}"
        workflows_resp = gh_get(f"https://api.github.com/repos/{repo_full}/actions/workflows", token)
        workflow_count = workflows_resp.json().get("total_count", 0) if workflows_resp.status_code < 300 else 0
        alerts_resp = gh_get(f"https://api.github.com/repos/{repo_full}/code-scanning/alerts", token)
        alerts_count = len(alerts_resp.json()) if alerts_resp.status_code < 300 else 0
        risk = classify_repo_risk(repo_full, policy)
        if risk == "risk:high": high += 1
        elif risk == "risk:medium": med += 1
        else: low += 1
        approvals_required = policy["approval_policy"].get(risk, 1)
        score = governance_score(workflow_count, alerts_count)
        report_repos.append({
            "repo": repo_full,
            "risk_label": risk,
            "required_approvals": approvals_required,
            "workflow_count": workflow_count,
            "security_alerts": alerts_count,
            "governance_score": score
        })
    os.makedirs("reports/org", exist_ok=True)
    final_report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "org": org,
        "summary": {
            "total_repos": len(report_repos),
            "low_risk_repos": low,
            "medium_risk_repos": med,
            "high_risk_repos": high
        },
        "repos": report_repos
    }
    with open("reports/org/org_report.json", "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2)
    print("Org report saved: reports/org/org_report.json")

if __name__ == "__main__":
    main()
