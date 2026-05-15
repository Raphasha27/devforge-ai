# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from openai import OpenAI

load_dotenv()

app = FastAPI(title="GitOps AI Review Bot")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


@app.post("/webhook")
async def github_webhook(req: Request):
    payload = await req.json()
    event = req.headers.get("X-GitHub-Event")

    if event == "pull_request":
        return await handle_pr(payload)

    return {"status": "ignored", "event": event}


async def handle_pr(payload: dict):
    pr = payload.get("pull_request", {})
    action = payload.get("action")

    if action not in ["opened", "synchronize", "reopened"]:
        return {"status": "ignored", "action": action}

    branch = pr.get("head", {}).get("ref", "")
    base = pr.get("base", {}).get("ref", "")
    repo_full_name = payload.get("repository", {}).get("full_name")
    pr_number = pr.get("number")
    diff_url = pr.get("diff_url")

    violations = []

    # Branch Rules Enforcement
    if base == "main" and not branch.startswith("hotfix/"):
        violations.append("❌ Direct PR to main not allowed. Must use hotfix/ or target develop.")

    valid_prefixes = ("feature/", "bugfix/", "hotfix/", "release/")
    if not branch.startswith(valid_prefixes):
        violations.append(f"❌ Invalid branch naming. Must start with one of: {valid_prefixes}")

    # Fetch Diff
    diff_text = fetch_pr_diff(diff_url)

    # Run AI Review
    ai_review = "No diff available to review."
    if diff_text:
        ai_review = analyze_diff_with_ai(diff_text)

    # Post Comment back to PR
    comment_body = build_comment_body(violations, ai_review)
    post_github_comment(repo_full_name, pr_number, comment_body)

    return {
        "pr_number": pr_number,
        "branch": branch,
        "base": base,
        "violations": violations,
        "status": "failed" if violations else "passed",
    }


def fetch_pr_diff(diff_url: str) -> str:
    if not diff_url or not GITHUB_TOKEN:
        return ""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
    }
    try:
        resp = requests.get(diff_url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        return ""
    except Exception:
        return ""


def analyze_diff_with_ai(diff_text: str) -> str:
    if not openai_client:
        return "⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY."

    try:
        # Prevent context limits by truncating diff if too large
        truncated_diff = diff_text[:10000]

        prompt = f"""You are a Senior Staff Engineer reviewing a Pull Request.
Analyze the following git diff and provide:
1. A Risk Score (Low, Medium, High).
2. Security warnings (hardcoded secrets, unsafe patterns).
3. 2-3 specific suggestions for code improvement.

Diff:
{truncated_diff}
"""
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Analysis failed: {str(e)}"


def build_comment_body(violations: list, ai_review: str) -> str:
    body = "## 🤖 GitOps AI Review\n\n"

    if violations:
        body += "### 🚨 Branch Rule Violations\n"
        for v in violations:
            body += f"- {v}\n"
        body += "\n"
    else:
        body += "✅ **GitFlow Branching Rules Compliant**\n\n"

    body += "### 🧠 AI Analysis\n"
    body += ai_review

    return body


def post_github_comment(repo_name: str, pr_number: int, body: str):
    if not GITHUB_TOKEN or not repo_name or not pr_number:
        return

    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    requests.post(url, json={"body": body}, headers=headers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
