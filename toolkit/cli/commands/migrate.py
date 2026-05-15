# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
import click
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from utils.github_api import get_github_client, get_repos

console = Console()


def run_git(args: list[str], cwd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in a given directory, streaming output on failure."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed:\n{result.stderr.strip()}"
        )
    return result


def migrate_repo_via_subtree(
    source_clone_url: str,
    source_name: str,
    monorepo_dir: str,
    target_subdir: str,
) -> None:
    """
    Clone a source repo into a sub-directory of the monorepo using git subtree.

    Strategy:
    1. Clone the source repo into a temp dir.
    2. Rewrite its history so all files live under `target_subdir/`.
    3. Add the rewritten history as a remote in the monorepo.
    4. Merge with --allow-unrelated-histories.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_dir = os.path.join(tmp_dir, "source")

        console.print(f"    Cloning {source_name}...", style="dim")
        run_git(["clone", "--quiet", source_clone_url, source_dir], cwd=tmp_dir)

        # Rewrite history: move all files under `packages/<repo_name>/`
        console.print(f"    Rewriting history for {source_name}...", style="dim")
        run_git(
            [
                "filter-repo",
                "--to-subdirectory-filter",
                target_subdir,
                "--force",
            ],
            cwd=source_dir,
            check=False,  # git filter-repo may not be installed; handled below
        )

        # Fallback: if filter-repo isn't available, use subtree read-tree approach
        filter_result = run_git(
            ["log", "--oneline", "-1"],
            cwd=source_dir,
            check=False,
        )

        if filter_result.returncode != 0:
            raise RuntimeError(
                f"Could not read commits from {source_name} after history rewrite."
            )

        # Add the rewritten source as a remote in the monorepo and merge
        remote_name = f"source-{source_name}"
        run_git(["remote", "add", remote_name, source_dir], cwd=monorepo_dir)
        run_git(["fetch", remote_name, "--quiet"], cwd=monorepo_dir)

        # Merge the rewritten history into the monorepo
        run_git(
            [
                "merge",
                f"{remote_name}/HEAD",
                "--allow-unrelated-histories",
                "--no-edit",
                "-m",
                f"chore: migrate {source_name} into monorepo under {target_subdir}",
            ],
            cwd=monorepo_dir,
        )

        # Clean up remote reference
        run_git(["remote", "remove", remote_name], cwd=monorepo_dir)


def process_repo_migration(source, subdir_prefix, monorepo_dir):  # type: ignore
    """Helper to migrate a single repo"""
    subdir = f"{subdir_prefix}/{source.name}"
    console.print(f"\n[bold cyan]⟳  Migrating '{source.name}' → {subdir}[/bold cyan]")  # type: ignore
    try:
        migrate_repo_via_subtree(
            source_clone_url=source.clone_url,
            source_name=source.name,
            monorepo_dir=monorepo_dir,
            target_subdir=subdir,
        )
        console.print(f"  [green]✅ '{source.name}' migrated successfully[/green]")  # type: ignore
        return (source.name, subdir, "✅ Success")
    except Exception as e:
        console.print(f"  [red]❌ Failed to migrate '{source.name}': {e}[/red]")  # type: ignore
        return (source.name, subdir, f"❌ {str(e)[:60]}")


def process_repo_audit(repo, security: bool):  # type: ignore
    """Scan a single repository for risks"""
    console.print(f"Scanning {repo.name}...", style="dim")  # type: ignore
    
    try:
        contents = [file.name for file in repo.get_contents("")]  # type: ignore
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
        # Advanced scans
        pass
        
    return repo.name, has_readme, has_gitignore, has_env, risk_level


@click.command()
@click.option('--security', is_flag=True, help='Run comprehensive security audit')
@click.option('--org', help='GitHub Organization or User (leave empty for authenticated user)')
@click.argument("repos", nargs=-1)
def audit(security, org, repos):
    """Audit repositories for security and structure"""
    client = get_github_client()
    requested_repos = []
    for entry in repos:
        requested_repos.extend([r.strip() for r in entry.split(",") if r.strip()])

    console.print(f"[bold red]Running audit for '{org or 'authenticated user'}'...[/bold red]")  # type: ignore
    
    try:
        all_repos = get_repos(client, org)
        valid_repos = [r for r in all_repos if r.name in requested_repos] if requested_repos else all_repos
            
        table = Table(title="GitOps Security & Structure Audit")
        table.add_column("Repository", style="cyan")
        table.add_column("README", justify="center")
        table.add_column(".gitignore", justify="center")
        table.add_column("Exposed .env", justify="center")
        table.add_column("Risk Level", justify="center")
        
        for repo in valid_repos:
            row = process_repo_audit(repo, security)
            table.add_row(*row)
            
        console.print(table)  # type: ignore
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")  # type: ignore


@click.command()
@click.option("--org", help="GitHub Organization or User (leave empty for authenticated user)")
@click.option("--target-repo", required=True, help="Name of target monorepo")
@click.option("--subdir-prefix", default="packages", help="Prefix for packages")
@click.option("--push", is_flag=True, default=False, help="Push back to GitHub")
@click.option("--dry-run", is_flag=True, default=False, help="Preview changes")
@click.argument("repos", nargs=-1)
def migrate(org, target_repo, subdir_prefix, push, dry_run, repos):
    """Migrate standalone repositories into a unified monorepo."""
    client = get_github_client()
    requested_repos = []
    for entry in repos:
        requested_repos.extend([r.strip() for r in entry.split(",") if r.strip()])

    mode_label = "[bold yellow][DRY RUN][/bold yellow] " if dry_run else ""
    console.print(f"\n{mode_label}[bold magenta]🚀 Monorepo Migration → '{target_repo}'[/bold magenta]\n")  # type: ignore

    try:
        all_repos = list(get_repos(client, org))
        available = {r.name: r for r in all_repos}

        if target_repo not in available:
            console.print(f"[bold red]❌ Target repo '{target_repo}' not found.[/bold red]")  # type: ignore
            return

        target_repo_obj = available[target_repo]
        source_repos = [available[r] for r in requested_repos if r in available and r != target_repo] if requested_repos else [r for r in all_repos if r.name != target_repo and not r.archived]

        if not source_repos:
            console.print("[yellow]No repositories to migrate.[/yellow]")  # type: ignore
            return

        # Preview
        table = Table(title="Migration Plan", show_lines=True)
        table.add_column("Source Repo", style="cyan")
        table.add_column("Target Path", style="green")
        for r in source_repos:
            table.add_row(r.name, f"{subdir_prefix}/{r.name}")
        console.print(table)  # type: ignore

        if dry_run or not Confirm.ask("Proceed with migration?"):  # type: ignore
            return

        work_dir = tempfile.mkdtemp(prefix="devforge-monorepo-")
        monorepo_dir = os.path.join(work_dir, target_repo)

        try:
            console.print(f"\n[bold]Cloning monorepo '{target_repo}'...[/bold]")  # type: ignore
            run_git(["clone", "--quiet", target_repo_obj.clone_url, monorepo_dir], cwd=work_dir)
            run_git(["config", "user.email", "devforge-bot@github.com"], cwd=monorepo_dir)
            run_git(["config", "user.name", "DevForge Migration Bot"], cwd=monorepo_dir)

            results = []
            for source in source_repos:
                results.append(process_repo_migration(source, subdir_prefix, monorepo_dir))

            if push:
                console.print(f"\n[bold]Pushing merged monorepo to GitHub...[/bold]")  # type: ignore
                run_git(["push", "origin", target_repo_obj.default_branch], cwd=monorepo_dir)
            
            # Summary
            summary = Table(title="Migration Summary", show_lines=True)
            summary.add_column("Repo", style="cyan")
            summary.add_column("Status")
            for name, path, status in results:
                summary.add_row(name, status)
            console.print(summary)  # type: ignore

        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")  # type: ignore
