import click
import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from rich.console import Console
from utils.github_api import get_github_client, GITHUB_TOKEN

console = Console()

def run_cmd(args: list[str], cwd: str):
    subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)

@click.command()
@click.argument("repo_name")
@click.option("--type", "repo_type", default="cyber", help="Type of seeding (e.g., cyber, web, cli)")
def seed(repo_name, repo_type):
    """Seed an empty repository with a project template."""
    client = get_github_client()
    user = client.get_user()
    
    try:
        repo = user.get_repo(repo_name)
    except Exception:
        console.print(f"[bold red]❌ Repository '{repo_name}' not found.[/bold red]")  # type: ignore
        return

    if repo.size > 0:  # type: ignore
        if not click.confirm(f"Repository '{repo_name}' is not empty. Overwrite with seed?"):
            return

    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_dir = os.path.join(tmp_dir, repo_name)
        console.print(f"[bold blue]🌱 Seeding '{repo_name}' with {repo_type} template...[/bold blue]")  # type: ignore
        
        os.makedirs(repo_dir)
        run_cmd(["git", "init", "-b", "main"], cwd=repo_dir)
        
        if repo_type == "cyber":
            seed_cyber(repo_dir)
        else:
            seed_default(repo_dir)
            
        run_cmd(["git", "add", "."], cwd=repo_dir)
        run_cmd(["git", "commit", "-m", f"chore: seed {repo_type} security ecosystem"], cwd=repo_dir)
        
        remote_url = f"https://{GITHUB_TOKEN}@github.com/{repo.full_name}.git"  # type: ignore
        run_cmd(["git", "remote", "add", "origin", remote_url], cwd=repo_dir)
        run_cmd(["git", "push", "-u", "origin", "main", "--force"], cwd=repo_dir)
        
        console.print(f"[bold green]✅ '{repo_name}' successfully seeded and pushed to GitHub![/bold green]")  # type: ignore

def seed_cyber(repo_dir):
    """Template for cybersecurity focus."""
    # README
    with open(os.path.join(repo_dir, "README.md"), "w") as f:
        f.write("# CyberShield & Threat Intelligence Hub\n\n")
        f.write("This repository serves as an autonomous security command center for detecting, mitigating, and analyzing cyber threats.\n\n")
        f.write("## Features\n")
        f.write("- **Decoy/Honeypot Systems**: Simple scripts to detect unauthorized access attempts.\n")
        f.write("- **Log Analysis**: Automated scanning of logs for suspicious patterns.\n")
        f.write("- **Security Hardening**: Scripts to audit and enforce security policies.\n")

    # Honeypot script
    with open(os.path.join(repo_dir, "honeypot.py"), "w") as f:
        f.write("""import socket
import logging

logging.basicConfig(filename='threats.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def start_honeypot(port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Honeypot listening on port {port}...")
    
    while True:
        client, addr = server.accept()
        msg = f"[!] Connection attempt from {addr[0]}:{addr[1]}"
        print(msg)
        logging.info(msg)
        client.send(b"HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n<html><body><h1>It Works!</h1></body></html>")
        client.close()

if __name__ == "__main__":
    start_honeypot()
""")

    # Security Auditor
    with open(os.path.join(repo_dir, "auditor.py"), "w") as f:
        f.write("""import os

def audit_system():
    print("--- Security Audit Report ---")
    # Check for sensitive files
    sensitive_files = ['.env', 'id_rsa', 'config.json']
    for f in sensitive_files:
        if os.path.exists(f):
            print(f"[!] Warning: Sensitive file '{f}' found in root!")
        else:
            print(f"[+] Clean: No '{f}' found.")

if __name__ == "__main__":
    audit_system()
""")

    # Threat Intelligence
    with open(os.path.join(repo_dir, "threat_intel.py"), "w") as f:
        f.write("""import requests

def fetch_threat_feed():
    print("[*] Fetching latest malicious IP feeds...")
    # Example feed: Abuse.ch or similar (simulated)
    try:
        # In a real scenario, you'd pull from a real API
        print("[+] Syncing with Global Threat Database...")
        malicious_ips = ["192.168.1.100", "45.33.22.11", "10.0.0.5"]
        print(f"[!] Identified {len(malicious_ips)} active threats targeting similar architectures.")
        return malicious_ips
    except Exception as e:
        print(f"[x] Feed sync failed: {e}")
        return []

if __name__ == "__main__":
    fetch_threat_feed()
""")

def seed_default(repo_dir):
    with open(os.path.join(repo_dir, "README.md"), "w") as f:
        f.write(f"# New Project\nInitialized by DevForge CLI.")
