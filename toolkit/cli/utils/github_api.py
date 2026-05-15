import os
from dotenv import load_dotenv
from github import Github, GithubException
from rich.console import Console

load_dotenv()

console = Console()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_github_client():
    if not GITHUB_TOKEN:
        console.print("[bold red]Error: GITHUB_TOKEN not set in environment.[/bold red]")
        exit(1)
    return Github(GITHUB_TOKEN)


def get_repos(client, org_name=None):
    if org_name:
        try:
            return client.get_organization(org_name).get_repos()
        except GithubException:
            # Fallback if it's a user and not an organization
            return client.get_user(org_name).get_repos()
    else:
        return client.get_user().get_repos()
