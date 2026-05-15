import typer
import os
import subprocess
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Git-Oxide: Smart Git Repository Cleanup & Optimization CLI")
console = Console()

@app.command()
def scan():
    """
    Scans the repository for stale branches and bloat.
    """
    console.print("[bold blue]🔍 Scanning repository for optimization opportunities...[/bold blue]")
    
    # Check for stale branches
    try:
        branches = subprocess.check_output(["git", "branch", "--merged"]).decode().split("\n")
        stale = [b.strip() for b in branches if b.strip() and not b.startswith("*")]
        
        if stale:
            table = Table(title="Stale Branches (Merged)")
            table.add_column("Branch Name", style="cyan")
            for b in stale:
                table.add_row(b)
            console.print(table)
        else:
            console.print("[green]✅ No stale merged branches found.[/green]")
            
    except Exception as e:
        console.print(f"[red]Error scanning branches: {e}[/red]")

@app.command()
def clean(force: bool = typer.Option(False, "--force", "-f", help="Delete branches without confirmation")):
    """
    Cleans up merged branches and optimizes the .git folder.
    """
    console.print("[bold yellow]🧹 Starting cleanup process...[/bold yellow]")
    
    # 1. Prune remote branches
    subprocess.run(["git", "remote", "prune", "origin"])
    
    # 2. Delete local merged branches
    branches = subprocess.check_output(["git", "branch", "--merged"]).decode().split("\n")
    stale = [b.strip() for b in branches if b.strip() and not b.startswith("*") and b.strip() not in ["main", "master", "develop"]]
    
    if stale:
        for b in stale:
            if force or typer.confirm(f"Delete branch {b}?"):
                subprocess.run(["git", "branch", "-d", b])
                console.print(f"[green]Deleted {b}[/green]")
    
    # 3. Garbage collection
    console.print("[blue]⚙️ Running git garbage collection...[/blue]")
    subprocess.run(["git", "gc", "--prune=now", "--aggressive"])
    console.print("[bold green]✨ Cleanup complete! Repository optimized.[/bold green]")

if __name__ == "__main__":
    app()
