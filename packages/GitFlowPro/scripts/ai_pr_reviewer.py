import os
import requests
import json
import sys
from openai import OpenAI

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO = os.getenv("REPO_NAME")
PR_NUMBER = os.getenv("PR_NUMBER")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

FAIL_ON_HIGH_RISK = os.getenv("FAIL_ON_HIGH_RISK", "false").lower() == "true"

if not OPENAI_API_KEY:
    print("⚠️ OPENAI_API_KEY is not set. Skipping AI PR Review.")
    sys.exit(0)

if not all([GITHUB_TOKEN, REPO, PR_NUMBER]):
    print("❌ Missing required environment variables (GITHUB_TOKEN, REPO_NAME, PR_NUMBER).")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
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


def github_patch(url, payload):
    r = requests.patch(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()


def upsert_comment(comment_body: str):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    try:
        comments = github_get(url)

        for c in comments:
            if c.get("body", "").startswith("## 🤖 RepoPilot AI Review"):
                comment_id = c["id"]
                update_url = f"https://api.github.com/repos/{REPO}/issues/comments/{comment_id}"
                github_patch(update_url, {"body": comment_body})
                print("🔁 Updated AI review comment.")
                return

        github_post(url, {"body": comment_body})
        print("🆕 Created AI review comment.")
    except Exception as e:
        print(f"❌ Error during comment upsert: {e}")


def apply_labels(labels):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    try:
        github_post(url, {"labels": labels})
    except Exception as e:
        print(f"❌ Error applying labels: {e}")


def clear_risk_labels():
    try:
        issue_url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}"
        issue_data = github_get(issue_url)

        existing = [l["name"] for l in issue_data.get("labels", [])]
        risk_labels = {"risk:low", "risk:medium", "risk:high"}

        for lbl in existing:
            if lbl in risk_labels:
                delete_url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels/{lbl}"
                requests.delete(delete_url, headers=headers)
    except Exception as e:
        print(f"❌ Error clearing risk labels: {e}")


def detect_critical_patterns(diff_text: str):
    patterns = [
        "AWS_SECRET_ACCESS_KEY",
        "BEGIN PRIVATE KEY",
        "PRIVATE KEY-----",
        "password=",
        "api_key",
        "SECRET_KEY",
        "eval(",
        "exec(",
        "os.system(",
        "subprocess.Popen(",
        "DROP TABLE",
        "DELETE FROM",
        "INSERT INTO",
        "SELECT * FROM",
    ]

    found = []
    lower = diff_text.lower()

    for p in patterns:
        if p.lower() in lower:
            found.append(p)

    return found


def main():
    pr_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    files_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"

    try:
        pr_data = github_get(pr_url)
        files_data = github_get(files_url)
    except Exception as e:
        print(f"❌ Error fetching PR data: {e}")
        sys.exit(1)

    title = pr_data.get("title", "")
    pr_body = pr_data.get("body", "")

    changed_files = []
    patches = []

    for f in files_data[:40]:
        filename = f.get("filename")
        status = f.get("status")
        additions = f.get("additions")
        deletions = f.get("deletions")
        patch = f.get("patch", "")

        changed_files.append(f"- {filename} ({status}) +{additions}/-{deletions}")

        if patch:
            patches.append(f"FILE: {filename}\n{patch}")

    diff_text = "\n\n".join(patches)

    critical_hits = detect_critical_patterns(diff_text)

    ai_prompt = f"""
You are RepoPilot AI Reviewer.
You are a senior software engineer specializing in security, performance, and maintainability.

Review the PR below and return STRICT JSON ONLY.
No markdown. No explanation outside JSON.

PR_TITLE: {title}

PR_DESCRIPTION:
{pr_body}

CHANGED_FILES:
{chr(10).join(changed_files)}

DIFF_SNIPPETS:
{diff_text[:12000]}

Return JSON in this format:

{{
  "summary": "short summary",
  "risk_level": "low|medium|high",
  "risk_score": 0-100,
  "security_findings": ["..."],
  "performance_findings": ["..."],
  "code_quality_findings": ["..."],
  "suggested_tests": ["..."],
  "recommended_actions": ["..."]
}}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a strict JSON generator."},
                {"role": "user", "content": ai_prompt}
            ]
        )

        raw = response.choices[0].message.content.strip()
        # Handle possible markdown code blocks in output
        if raw.startswith("```json"):
            raw = raw[7:-3].strip()
        elif raw.startswith("```"):
            raw = raw[3:-3].strip()

        try:
            ai_data = json.loads(raw)
        except Exception as e:
            print(f"❌ Failed to parse AI JSON: {e}")
            ai_data = {
                "summary": "AI failed to return valid JSON output.",
                "risk_level": "medium",
                "risk_score": 60,
                "security_findings": ["Invalid JSON returned by model."],
                "performance_findings": [],
                "code_quality_findings": [],
                "suggested_tests": [],
                "recommended_actions": ["Retry workflow or check model output."]
            }

        risk_level = ai_data.get("risk_level", "medium")
        risk_score = ai_data.get("risk_score", 50)

        block_label_needed = False
        if critical_hits:
            block_label_needed = True

        clear_risk_labels()

        labels_to_apply = [risk_label, "ai:reviewed"]

        if block_label_needed or risk_level.lower() == "high":
            labels_to_apply.append("ai:block")

        apply_labels(labels_to_apply)

        critical_section = ""
        if critical_hits:
            critical_section = "\n\n## 🚨 Critical Pattern Matches\n" + "\n".join([f"- `{x}`" for x in critical_hits])

        comment = f"""## 🤖 RepoPilot AI Review

### ✅ Summary
{ai_data.get("summary", "No summary provided.")}

### 📌 Risk
**Level:** `{risk_level.upper()}`
**Score:** `{risk_score}/100`

### 🔐 Security Findings
{chr(10).join([f"- {x}" for x in ai_data.get("security_findings", [])]) or "- None"}

### ⚡ Performance Findings
{chr(10).join([f"- {x}" for x in ai_data.get("performance_findings", [])]) or "- None"}

### 🧹 Code Quality Findings
{chr(10).join([f"- {x}" for x in ai_data.get("code_quality_findings", [])]) or "- None"}

### 🧪 Suggested Tests
{chr(10).join([f"- {x}" for x in ai_data.get("suggested_tests", [])]) or "- None"}

### 🛠 Recommended Actions
{chr(10).join([f"- {x}" for x in ai_data.get("recommended_actions", [])]) or "- None"}

{critical_section}

---
*Generated automatically by RepoPilot AI Reviewer.*
"""

        upsert_comment(comment)

        # Optional fail gate
        if FAIL_ON_HIGH_RISK:
            if risk_level.lower() == "high" or len(critical_hits) > 0:
                print("❌ RepoPilot blocked this PR due to HIGH risk or critical patterns.")
                sys.exit(1)

        print("✅ RepoPilot AI review completed successfully.")
    except Exception as e:
        print(f"❌ Error during AI review process: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
