# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
import click
from rich.console import Console
from rich.table import Table
from utils.github_api import get_github_client, get_repos

console = Console()

@click.command()
@click.option('--security', is_flag=True, help='Run comprehensive security audit')
@click.option('--org', help='GitHub Organization or User (leave empty for authenticated user)')
@click.argument("repos", nargs=-1)
def audit(security, org, repos):
    """Audit repositories for security and structure"""
    client = get_github_client()
    
    # Handle PowerShell comma-splitting or multiple args
    requested_repos: list[str] = []
    for entry in repos:
        requested_repos.extend([r.strip() for r in entry.split(",") if r.strip()])

    console.print(f"[bold red]Running audit for '{org or 'authenticated user'}'...[/bold red]")
    
    try:
        all_repos = get_repos(client, org)
        if requested_repos:
            valid_repos = [r for r in all_repos if r.name in requested_repos]
        else:
            valid_repos = all_repos
            
        table = Table(title="GitOps Security & Structure Audit")
        table.add_column("Repository", style="cyan")
        table.add_column("README", justify="center")
        table.add_column(".gitignore", justify="center")
        table.add_column("Exposed .env", justify="center")
        table.add_column("Risk Level", justify="center")
        
        for repo in valid_repos:
            console.print(f"Scanning {repo.name}...", style="dim")
            
            # Fetch root directory contents
            try:
                contents = [file.name for file in repo.get_contents("")]
            except Exception:
                contents = []
                
            has_readme = "✅" if any(f.lower() == "readme.md" for f in contents) else "❌"
            has_gitignore = "✅" if ".gitignore" in contents else "❌"
            has_env = "🚨 YES" if any(f.endswith(".env") or f == "secrets.json" for f in contents) else "✅ Safe"
            
            risk_level = "Low"
            if has_env != "✅ Safe":
                risk_level = "[bold red]High[/bold red]"
            elif has_gitignore == "❌":
                risk_level = "[bold yellow]Medium[/bold yellow]"
                
            if security:
                # Placeholder for advanced security scanning (e.g. searching for AWS keys)
                pass
                
            table.add_row(repo.name, has_readme, has_gitignore, has_env, risk_level)
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error during audit: {str(e)}[/bold red]")
