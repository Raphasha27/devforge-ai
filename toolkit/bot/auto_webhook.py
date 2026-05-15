import os
import sys
import time
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Auto-install missing dependencies if needed
try:
    from pyngrok import ngrok
    from github import Github
except ImportError:
    print("Installing required packages: pyngrok, PyGithub...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok", "PyGithub"])
    from pyngrok import ngrok
    from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("\n[ERROR] GITHUB_TOKEN is not set.")
    print("Please add it to your .env file: GITHUB_TOKEN=your_token_here")
    print("Generate a token at: https://github.com/settings/tokens")
    sys.exit(1)

print("Starting Ngrok tunnel to expose port 8000...")
try:
    http_tunnel = ngrok.connect(8000)
except Exception as e:
    print(f"Failed to start Ngrok: {e}")
    sys.exit(1)

public_url = http_tunnel.public_url
webhook_url = f"{public_url}/webhook"

print(f"✅ Ngrok Tunnel active: {public_url}")
print(f"🔗 Webhook Endpoint: {webhook_url}")

client = Github(GITHUB_TOKEN)

print("\nSetting up webhooks on your GitHub repositories...")
user = client.get_user()
repos = list(user.get_repos())

for repo in repos:
    # Only attach to repos the authenticated user owns to avoid permissions errors
    if repo.owner.login != user.login:
        continue

    try:
        # Clear out any old ngrok webhooks created previously
        for hook in repo.get_hooks():
            if "ngrok" in hook.config.get("url", ""):
                hook.delete()

        # Create new webhook pointing to our local AI bot
        repo.create_hook(
            name="web",
            config={
                "url": webhook_url,
                "content_type": "json",
                "insecure_ssl": "0",
            },
            events=["pull_request"],
            active=True,
        )
        print(f"  [+] Webhook attached to {repo.full_name}")
    except Exception as e:
        print(f"  [-] Failed on {repo.full_name}: {e}")

print("\n🚀 DONE! The GitOps AI Bot is now securely wired into all your GitHub repositories.")
print("Waiting for PR events... (Press Ctrl+C to disconnect)")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing tunnel...")
    ngrok.disconnect(http_tunnel.public_url)
    ngrok.kill()
