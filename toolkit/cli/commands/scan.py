import click
from rich.console import Console
from rich.table import Table
from utils.github_api import get_github_client, get_repos

console = Console()

@click.command()
@click.option('--org', help='GitHub Organization or User (leave empty for authenticated user)')
def scan(org):
    """Scan repositories for GitFlow compliance"""
    client = get_github_client()
    
    console.print(f"[bold green]Fetching repositories for '{org or 'authenticated user'}'...[/bold green]")
    try:
        repos = get_repos(client, org)
        
        table = Table(title="GitFlow Branch Compliance Scan")
        table.add_column("Repository", style="cyan")
        table.add_column("Has 'main'", justify="center")
        table.add_column("Has 'develop'", justify="center")
        table.add_column("Default Branch", style="magenta")
        table.add_column("Compliance", justify="center")

        seen = set()
        for repo in repos:
            if repo.name in seen:
                continue
            seen.add(repo.name)

            branches = [b.name for b in repo.get_branches()]
            has_main = "✅" if "main" in branches else "❌"
            has_develop = "✅" if "develop" in branches else "❌"
            default_branch = repo.default_branch
            
            is_compliant = "✅" if "main" in branches and "develop" in branches and default_branch in ["main", "develop"] else "❌"
            
            table.add_row(repo.name, has_main, has_develop, default_branch, is_compliant)
            
        console.print(table)
        console.print(f"\n[dim]Total: {len(seen)} repositories[/dim]")
    except Exception as e:
        console.print(f"[bold red]Error during scan: {str(e)}[/bold red]")
