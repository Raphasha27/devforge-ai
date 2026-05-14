import os
import json
import requests
from datetime import datetime
from scripts.audit_logger import log_event

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

def count_approvals(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
    r = gh_get(url, token)
    if r.status_code >= 300:
        return 0
    reviews = r.json()
    approved_users = set()
    for rev in reviews:
        if rev.get("state") == "APPROVED":
            approved_users.add(rev.get("user", {}).get("login"))
    return len(approved_users)

def classify_risk(changed_files, policy):
    scoring = policy["risk_scoring"]
    for f in changed_files:
        for p in scoring["high"]:
            if f.startswith(p) or f == p:
                return "risk:high", [f"High-risk change detected: {f}"]
    for f in changed_files:
        for p in scoring["medium"]:
            if f.startswith(p) or f == p:
                return "risk:medium", [f"Medium-risk change detected: {f}"]
    return "risk:low", ["Low-risk change set detected"]

def detect_blocked_keywords(repo, pr_number, token, blocked_keywords):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    r = gh_get(url, token)
    if r.status_code >= 300:
        return []
    findings = []
    files = r.json()
    for f in files:
        patch = f.get("patch") or ""
        for keyword in blocked_keywords:
            if keyword in patch:
                findings.append({
                    "file": f.get("filename"),
                    "keyword": keyword,
                    "reason": "Blocked keyword detected in patch"
                })
    return findings

def save_report(report):
    os.makedirs("governance/reports", exist_ok=True)
    with open("governance/reports/policy_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

def main():
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("REPO")
    pr_number = os.getenv("PR_NUMBER")
    if not token or not repo or not pr_number:
        raise SystemExit("Missing env vars: GITHUB_TOKEN, REPO, PR_NUMBER")
    policy = load_policy()
    files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    files_resp = gh_get(files_url, token)
    if files_resp.status_code >= 300:
        raise SystemExit(f"GitHub API error: {files_resp.text}")
    changed_files = [f["filename"] for f in files_resp.json()]
    risk_label, reasons = classify_risk(changed_files, policy)
    approvals_required = policy["approval_policy"].get(risk_label, 1)
    approvals_found = count_approvals(repo, pr_number, token)
    blocked_findings = detect_blocked_keywords(repo, pr_number, token, policy.get("blocked_keywords", []))
    status = "PASS"
    failures = []
    if approvals_found < approvals_required:
        status = "FAIL"
        failures.append(f"Insufficient approvals. Required={approvals_required}, Found={approvals_found}")
    if blocked_findings:
        status = "FAIL"
        failures.append("Blocked keywords detected in patch.")
    report = {
        "policy_version": policy["version"],
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "repo": repo,
        "pr_number": pr_number,
        "status": status,
        "risk_label": risk_label,
        "reasons": reasons,
        "approvals_required": approvals_required,
        "approvals_found": approvals_found,
        "changed_files": changed_files,
        "blocked_findings": blocked_findings,
        "failures": failures
    }
    save_report(report)
    if status == "PASS":
        log_event("policy_passed_v3", report)
        print("POLICY PASS")
        raise SystemExit(0)
    log_event("policy_failed_v3", report)
    print("POLICY FAIL:", failures)
    raise SystemExit(1)

if __name__ == "__main__":
    main()
