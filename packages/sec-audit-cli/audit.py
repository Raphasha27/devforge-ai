import typer
import requests
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Sec-Audit: Lightweight dependency vulnerability scanner.")
console = Console()

# Mock database of vulnerable versions for demonstration
VULNERABLE_VERSIONS = {
    "requests": "2.25.1",
    "flask": "1.1.2",
    "django": "3.1.7",
    "jinja2": "2.11.2"
}

@app.command()
def scan(file: str = typer.Argument("requirements.txt", help="Path to requirements file")):
    """
    Scans your requirements.txt for known vulnerable packages.
    """
    console.print(f"[bold red]🛡️ Starting security audit for {file}...[/bold red]")
    
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            
        table = Table(title="Security Audit Results")
        table.add_column("Package", style="cyan")
        table.add_column("Current Version", style="yellow")
        table.add_column("Status", style="bold")
        
        found_issues = False
        for line in lines:
            if "==" in line:
                pkg, ver = line.strip().split("==")
                if pkg in VULNERABLE_VERSIONS and ver == VULNERABLE_VERSIONS[pkg]:
                    table.add_row(pkg, ver, "[red]❌ VULNERABLE[/red]")
                    found_issues = True
                else:
                    table.add_row(pkg, ver, "[green]✅ SECURE[/green]")
                    
        console.print(table)
        
        if found_issues:
            console.print("\n[bold red]CRITICAL: Vulnerable packages detected. Upgrade immediately![/bold red]")
        else:
            console.print("\n[bold green]Ecosystem Health: OPTIMAL. No known vulnerabilities found.[/bold green]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    app()
