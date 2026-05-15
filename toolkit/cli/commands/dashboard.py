# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
import click
import os
import webbrowser
from rich.console import Console
from utils.dashboard_gen import build_dashboard

console = Console()

@click.command()
@click.option('--open', 'open_browser', is_flag=True, help='Open the dashboard in the default browser')
def dashboard(open_browser):
    """Generate a high-fidelity control dashboard for the ecosystem"""
    console.print("[bold cyan]⟳  Generating DevForge Control Dashboard...[/bold cyan]")
    
    try:
        path = build_dashboard()
        console.print(f"[bold green]✅ Dashboard successfully generated at: {path}[/bold green]")
        
        if open_browser:
            webbrowser.open(f"file:///{path}")
            
    except Exception as e:
        console.print(f"[bold red]❌ Failed to generate dashboard: {e}[/bold red]")
