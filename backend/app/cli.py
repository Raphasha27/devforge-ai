import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from app.core.company_cycle import DevForgeCompany
import asyncio

app = typer.Typer(help="DevForge AI - Autonomous Ecosystem Controller")
console = Console()
company = DevForgeCompany()

@app.command()
def status():
    """Check the status of the DevForge Ecosystem."""
    console.print(Panel("[bold green]DevForge AI Core[/bold green] - v11.5 Operational", border_style="bright_blue"))
    
    table = Table(title="Ecosystem Health")
    table.add_column("Repository", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Health", style="yellow")
    
    # Mock data for CLI demo
    table.add_row("git-oxide", "Active", "98%")
    table.add_row("sec-audit-cli", "Active", "95%")
    table.add_row("env-guardian", "Evolving", "82%")
    
    console.print(table)

@app.command()
def cycle():
    """Trigger a manual business cycle."""
    console.print("[bold yellow]Initiating Autonomous Business Cycle...[/bold yellow]")
    asyncio.run(company.execute_business_cycle())
    console.print("[bold green]Cycle Complete.[/bold green]")

@app.command()
def chat():
    """Monitor internal agent collaboration chat."""
    from app.core.collaboration import collaboration_feed
    console.print(Panel("Internal Collaboration Feed", style="magenta"))
    for msg in collaboration_feed.get_feed():
        console.print(f"{msg['emoji']} [bold]{msg['actor']}[/bold]: {msg['text']}")

if __name__ == "__main__":
    app()
