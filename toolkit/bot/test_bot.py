"""
End-to-end test for the GitOps AI Review Bot.

Simulates a GitHub pull_request webhook payload and sends it to the
running FastAPI server to verify the full review pipeline works.

Usage:
    1. Start the bot:  uvicorn main:app --port 8000
    2. Run this test:  python test_bot.py
"""
import json
import requests

BOT_URL = "http://localhost:8000"

# --- Compliant PR payload (should PASS) ---
COMPLIANT_PAYLOAD = {
    "action": "opened",
    "pull_request": {
        "number": 42,
        "head": {"ref": "feature/add-login-flow"},
        "base": {"ref": "develop"},
        "diff_url": None,  # No diff for local test
    },
    "repository": {"full_name": "your-org/your-repo"},
}

# --- Violating PR payload (should FAIL) ---
VIOLATING_PAYLOAD = {
    "action": "opened",
    "pull_request": {
        "number": 99,
        "head": {"ref": "my-random-branch"},
        "base": {"ref": "main"},
        "diff_url": None,
    },
    "repository": {"full_name": "your-org/your-repo"},
}


def send_webhook(payload: dict, label: str):
    print(f"\n{'='*60}")
    print(f"  🧪 TEST: {label}")
    print(f"{'='*60}")
    try:
        response = requests.post(
            f"{BOT_URL}/webhook",
            json=payload,
            headers={"X-GitHub-Event": "pull_request"},
            timeout=10,
        )
        data = response.json()
        status = data.get("status", "unknown")
        violations = data.get("violations", [])

        if status == "passed":
            print(f"  ✅ RESULT: PASSED (no violations)")
        else:
            print(f"  ❌ RESULT: FAILED")
            for v in violations:
                print(f"     - {v}")

        print(f"\n  Raw response:")
        print(json.dumps(data, indent=4))

    except requests.exceptions.ConnectionError:
        print("  ⚠️  Bot is not running. Start it with: uvicorn main:app --port 8000")
    except Exception as e:
        print(f"  ❌ Error: {e}")


def test_health():
    print("\n🔍 Checking bot health...")
    try:
        r = requests.get(f"{BOT_URL}/docs", timeout=5)
        if r.status_code == 200:
            print("  ✅ Bot is running — FastAPI docs reachable at http://localhost:8000/docs")
        else:
            print(f"  ⚠️  Unexpected status: {r.status_code}")
    except requests.exceptions.ConnectionError:
        print("  ❌ Bot is not running. Start with: uvicorn main:app --port 8000")


if __name__ == "__main__":
    test_health()
    send_webhook(COMPLIANT_PAYLOAD, "Compliant PR (feature/ → develop) — should PASS")
    send_webhook(VIOLATING_PAYLOAD, "Violating PR (random branch → main) — should FAIL")
    print("\n✅ Tests complete.\n")
