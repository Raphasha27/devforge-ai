import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import click
from rich.console import Console
from commands.scan import scan
# pyrefly: ignore [missing-import]
from commands.enforce import enforce
# pyrefly: ignore [missing-import]
from commands.audit import audit
from commands.ci_setup import ci_setup
from commands.migrate import migrate
from commands.seed import seed
from commands.dashboard import dashboard

console = Console()

@click.group()
def cli():
    """GitFlow Orchestrator - Multi-Repo Automation Engine"""
    pass

cli.add_command(scan)
cli.add_command(enforce)
cli.add_command(audit)
cli.add_command(ci_setup)
cli.add_command(migrate)
cli.add_command(seed)
cli.add_command(dashboard)

if __name__ == "__main__":
    cli()
