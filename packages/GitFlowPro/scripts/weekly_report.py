import os
import requests
from datetime import datetime, timedelta

GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("REPO_NAME")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def github_api(url):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def main():
    since = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"

    open_issues = github_api(f"https://api.github.com/repos/{REPO}/issues?state=open")
    open_pulls = github_api(f"https://api.github.com/repos/{REPO}/pulls?state=open")
    commits = github_api(f"https://api.github.com/repos/{REPO}/commits?since={since}")

    workflows = github_api(f"https://api.github.com/repos/{REPO}/actions/runs?per_page=20")
    workflow_runs = workflows.get("workflow_runs", [])

    failed_runs = [w for w in workflow_runs if w.get("conclusion") == "failure"]
    success_runs = [w for w in workflow_runs if w.get("conclusion") == "success"]

    report = f"""
📊 GitFlowPro Weekly GitHub Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Repo: {REPO}

📌 Open Issues: {len(open_issues)}
📌 Open PRs: {len(open_pulls)}
🧾 Commits (7 days): {len(commits)}

⚙️ Recent Workflow Runs: {len(workflow_runs)}
✅ Successful Runs: {len(success_runs)}
❌ Failed Runs: {len(failed_runs)}

Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    print(report)

    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": report})


if __name__ == "__main__":
    main()
