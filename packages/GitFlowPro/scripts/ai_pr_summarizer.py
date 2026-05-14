import os
import requests
from openai import OpenAI
import sys

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO = os.getenv("REPO_NAME")
PR_NUMBER = os.getenv("PR_NUMBER")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    print("⚠️ OPENAI_API_KEY is not set. Skipping AI PR Summary.")
    sys.exit(0)

if not all([GITHUB_TOKEN, REPO, PR_NUMBER]):
    print("❌ Missing required environment variables (GITHUB_TOKEN, REPO_NAME, PR_NUMBER).")
    sys.exit(1)


client = OpenAI(api_key=OPENAI_API_KEY)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def github_api(url):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def upsert_comment(body: str):
    list_url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    comments = github_api(list_url)

    for c in comments:
        if c.get("body", "").startswith("## 🤖 RepoPilot AI PR Summary"):
            comment_id = c["id"]
            update_url = f"https://api.github.com/repos/{REPO}/issues/comments/{comment_id}"
            r = requests.patch(update_url, headers=headers, json={"body": body})
            r.raise_for_status()
            print("🔁 Updated existing AI summary comment.")
            return

    # else create new comment
    r = requests.post(list_url, headers=headers, json={"body": body})
    r.raise_for_status()
    print("🆕 Created new AI summary comment.")


def main():
    pr_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    files_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"

    try:
        pr_data = github_api(pr_url)
        files_data = github_api(files_url)
    except Exception as e:
        print(f"❌ Error fetching data from GitHub: {e}")
        sys.exit(1)

    title = pr_data.get("title", "")
    body = pr_data.get("body", "")

    changed_files = []
    patch_data = []

    for f in files_data[:25]:
        filename = f.get("filename")
        status = f.get("status")
        additions = f.get("additions")
        deletions = f.get("deletions")
        patch = f.get("patch", "")

        changed_files.append(f"- {filename} ({status}) +{additions}/-{deletions}")

        if patch:
            patch_data.append(f"FILE: {filename}\nPATCH:\n{patch}\n")

    prompt = f"""
You are RepoPilot AI PR Reviewer.
Your job is to summarize pull requests in a clean developer-friendly format.

PR Title: {title}

PR Description:
{body}

Changed Files:
{chr(10).join(changed_files)}

Diff Snippets:
{chr(10).join(patch_data)}

Return a professional GitHub PR summary in Markdown with:

## Summary
## Key Changes
## Risk Level (Low/Medium/High) + Reason
## Suggested Tests
## Potential Issues

Be concise but informative.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a senior software engineer and PR reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        ai_summary = response.choices[0].message.content

        final_comment = f"""## 🤖 RepoPilot AI PR Summary

{ai_summary}

---
*Generated automatically by RepoPilot.*
"""

        upsert_comment(final_comment)
        print("✅ AI PR Summary processed successfully.")
    except Exception as e:
        print(f"❌ Error during AI summary generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
