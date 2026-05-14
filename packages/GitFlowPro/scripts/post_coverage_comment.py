import os
import json
import requests
import sys

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO_NAME")
PR_NUMBER = os.getenv("PR_NUMBER")

if not GITHUB_TOKEN or not REPO or not PR_NUMBER:
    print("⚠️ Missing environment variables. Skipping coverage comment.")
    sys.exit(0)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def load_coverage(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data.get("totals", {}).get("percent_covered", None)
    except Exception:
        return None


def github_get(url):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def github_post(url, payload):
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()


def github_patch(url, payload):
    r = requests.patch(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()


def upsert_comment(body: str):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    try:
        comments = github_get(url)

        for c in comments:
            if c.get("body", "").startswith("## 📊 Coverage Report (RepoPilot)"):
                comment_id = c["id"]
                update_url = f"https://api.github.com/repos/{REPO}/issues/comments/{comment_id}"
                github_patch(update_url, {"body": body})
                print("🔁 Updated coverage comment.")
                return

        github_post(url, {"body": body})
        print("🆕 Created coverage comment.")
    except Exception as e:
        print(f"❌ Error during coverage comment upsert: {e}")


def main():
    main_cov = load_coverage("coverage_main.json")
    pr_cov = load_coverage("coverage_pr.json")

    if main_cov is None or pr_cov is None:
        print("⚠️ Coverage files missing. Skipping comment.")
        return

    diff = pr_cov - main_cov

    emoji = "🟢"
    if diff < 0:
        emoji = "🔴"
    elif diff == 0:
        emoji = "🟡"

    comment = f"""## 📊 Coverage Report (RepoPilot)

| Branch | Coverage |
|--------|----------|
| `main` | **{main_cov:.2f}%** |
| `PR`   | **{pr_cov:.2f}%** |

### Difference
{emoji} **{diff:+.2f}%**

---
*Generated automatically by RepoPilot Coverage Gate.*
"""

    upsert_comment(comment)


if __name__ == "__main__":
    main()
