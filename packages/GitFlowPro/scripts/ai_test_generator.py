import os
import requests
import json
import base64
import sys
from openai import OpenAI

BOT_TOKEN = os.getenv("REPOPILOT_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO = os.getenv("REPO_NAME")
PR_NUMBER = os.getenv("PR_NUMBER")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    print("⚠️ OPENAI_API_KEY is not set. Skipping AI Test Generation.")
    sys.exit(0)

if not BOT_TOKEN:
    print("⚠️ REPOPILOT_BOT_TOKEN is not set. Skipping AI Test Generation.")
    sys.exit(0)

if not all([REPO, PR_NUMBER]):
    print("❌ Missing required environment variables (REPO_NAME, PR_NUMBER).")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

headers = {
    "Authorization": f"token {BOT_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def github_get(url):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def github_post(url, payload):
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()


def github_put(url, payload):
    r = requests.put(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()


def get_pr_files():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    return github_get(url)


def get_default_branch():
    url = f"https://api.github.com/repos/{REPO}"
    return github_get(url).get("default_branch", "main")


def get_latest_commit_sha(branch):
    url = f"https://api.github.com/repos/{REPO}/git/ref/heads/{branch}"
    data = github_get(url)
    return data["object"]["sha"]


def create_branch(new_branch, base_branch):
    base_sha = get_latest_commit_sha(base_branch)

    url = f"https://api.github.com/repos/{REPO}/git/refs"
    payload = {"ref": f"refs/heads/{new_branch}", "sha": base_sha}

    try:
        github_post(url, payload)
        print(f"✅ Created branch: {new_branch}")
    except requests.exceptions.HTTPError as e:
        if "Reference already exists" in str(e):
            print(f"⚠️ Branch already exists: {new_branch}")
        else:
            raise


def create_or_update_file(branch, filepath, content, message):
    url = f"https://api.github.com/repos/{REPO}/contents/{filepath}"

    existing_sha = None
    r = requests.get(url, headers=headers, params={"ref": branch})
    if r.status_code == 200:
        existing_sha = r.json().get("sha")

    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": branch
    }

    if existing_sha:
        payload["sha"] = existing_sha

    github_put(url, payload)


def open_pull_request(head_branch, base_branch, title, body):
    url = f"https://api.github.com/repos/{REPO}/pulls"
    payload = {
        "title": title,
        "head": head_branch,
        "base": base_branch,
        "body": body
    }

    try:
        pr = github_post(url, payload)
        pr_number = pr["number"]

        # add labels
        label_url = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/labels"
        github_post(label_url, {"labels": ["ai:reviewed", "risk:low"]})

        print(f"✅ Created PR: {pr.get('html_url')}")
        return pr
    except requests.exceptions.HTTPError as e:
        print("⚠️ Could not create PR (may already exist).")
        print(e)
        return None


def ai_generate_tests(diff_text):
    prompt = f"""
You are RepoPilot AI Test Generator.
Generate unit tests for the code changes.

Rules:
- Only output JSON
- No markdown
- No explanations outside JSON
- If Python code changed, generate pytest tests.
- If JavaScript/TypeScript changed, generate Jest tests.

Return JSON like:

{{
  "tests": [
    {{
      "filepath": "tests/test_example.py",
      "content": "...full file content..."
    }}
  ]
}}

Diff Snippets:
{diff_text[:12000]}
"""

    res = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a strict JSON generator."},
            {"role": "user", "content": prompt}
        ]
    )

    raw = res.choices[0].message.content.strip()
    # Handle possible markdown code blocks in output
    if raw.startswith("```json"):
        raw = raw[7:-3].strip()
    elif raw.startswith("```"):
        raw = raw[3:-3].strip()

    return json.loads(raw)


def main():
    try:
        base_branch = get_default_branch()
        new_branch = f"ai/tests/pr-{PR_NUMBER}"

        files = get_pr_files()

        patches = []
        for f in files[:30]:
            patch = f.get("patch", "")
            filename = f.get("filename", "")
            if patch:
                patches.append(f"FILE: {filename}\n{patch}")

        diff_text = "\n\n".join(patches)

        if not diff_text.strip():
            print("No diff text found. Exiting.")
            return

        print("🤖 Generating tests using AI...")
        test_plan = ai_generate_tests(diff_text)

        tests = test_plan.get("tests", [])
        if not tests:
            print("⚠️ AI returned no tests. Exiting.")
            return

        create_branch(new_branch, base_branch)

        for t in tests:
            filepath = t["filepath"]
            content = t["content"]
            create_or_update_file(
                new_branch,
                filepath,
                content,
                message=f"test: add generated tests for PR #{PR_NUMBER}"
            )
            print(f"✅ Added test file: {filepath}")

        open_pull_request(
            head_branch=new_branch,
            base_branch=base_branch,
            title=f"test: AI-generated tests for PR #{PR_NUMBER}",
            body=f"""## 🤖 RepoPilot AI Test Generator

This PR contains AI-generated tests for PR #{PR_NUMBER}.

### Notes
- Please review tests carefully.
- Ensure coverage matches expected behavior.

Linked PR: #{PR_NUMBER}
"""
        )
    except Exception as e:
        print(f"❌ Error during AI test generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
