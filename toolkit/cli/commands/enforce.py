# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
import os
import requests
import click
from github.Repository import Repository
from rich.console import Console
from rich.table import Table
from utils.github_api import get_github_client, get_repos, GITHUB_TOKEN

from typing import TYPE_CHECKING, List, Tuple
if TYPE_CHECKING:
    from rich.console import Console
    from github.Repository import Repository
    console: Console
    results: List[Tuple[str, str]]
    repo: Repository
    GITHUB_TOKEN: str
    admin_bypass: bool
    require_reviews: int

console = Console()


def process_repo_enforcement(repo: Repository, admin_bypass: bool, require_reviews: int) -> str:
    """Helper to process a single repository's enforcement logic"""
    console.print(f"[bold cyan]⟳  {repo.name}[/bold cyan]")  # type: ignore

    # ── Detect empty repos ──────────────────────────────────────────────────
    if repo.size == 0:
        try:
            branches = [b.name for b in repo.get_branches()]
            if not branches:
                console.print("  [dim]⚪ Empty repository — skipping.[/dim]")  # type: ignore
                return "⚪ Empty repo"
        except Exception:
            console.print("  [dim]⚪ Empty repository — skipping.[/dim]")  # type: ignore
            return "⚪ Empty repo"
    else:
        branches = [b.name for b in repo.get_branches()]  # type: ignore

    # ── Step 1: Ensure 'main' ───────────────────────────────────────────────
    if "main" not in branches:  # type: ignore
        if "master" in branches:  # type: ignore
            try:
                resp = requests.post(
                    f"https://api.github.com/repos/{repo.full_name}/branches/master/rename",  # type: ignore
                    json={"new_name": "main"},
                    headers={
                        "Authorization": f"token {GITHUB_TOKEN}",  # type: ignore
                        "Accept": "application/vnd.github.v3+json",
                    },
                )
                resp.raise_for_status()
                console.print("  [green]✅ Renamed 'master' → 'main'[/green]")  # type: ignore
                branches = [b.name for b in repo.get_branches()]  # type: ignore
            except Exception as e:
                console.print(f"  [yellow]⚠️  Could not rename 'master': {e}[/yellow]")  # type: ignore
                return "⚠️ Master rename failed"
        else:
            console.print("  [red]❌ No 'main' or 'master' branch found.[/red]")  # type: ignore
            return "❌ No main/master"

    # ── Step 2: Create 'develop' ────────────────────────────────────────────
    if "develop" not in branches:  # type: ignore
        try:
            repo.create_git_ref(  # type: ignore
                ref="refs/heads/develop",
                sha=repo.get_branch("main").commit.sha,  # type: ignore
            )
            console.print("  [green]✅ Created 'develop'[/green]")  # type: ignore
        except Exception as e:
            console.print(f"  [red]❌ Failed to create 'develop': {e}[/red]")  # type: ignore
    else:
        console.print("  [blue]✓ 'develop' already exists[/blue]")  # type: ignore

    # ── Step 3: Apply Protection ───────────────────────────────────────────
    try:
        main_branch = repo.get_branch("main")  # type: ignore
        main_branch.edit_protection(  # type: ignore
            enforce_admins=not admin_bypass,
            dismiss_stale_reviews=True,
            required_approving_review_count=require_reviews if require_reviews > 0 else 0,
        )
        admin_note = "(admin bypass ON)" if admin_bypass else "(strict)"
        console.print(f"  [green]✅ Protected 'main' {admin_note}[/green]")  # type: ignore
        return "✅ Enforced"
    except Exception as e:
        err = str(e)
        if "403" in err or "Upgrade to GitHub Pro" in err:
            console.print("  [yellow]⚠️  Private repo — needs GitHub Pro for protection.[/yellow]")  # type: ignore
            return "⚠️ Private (no protection)"
        console.print(f"  [red]⚠️  Protection failed: {err[:60]}[/red]")  # type: ignore
        return f"❌ {err[:40]}"


@click.command()
@click.option("--all", "apply_all", is_flag=True, help="Apply to all repositories")
@click.option("--org", help="GitHub Organization or User (leave empty for authenticated user)")
@click.option(
    "--require-reviews",
    default=1,
    show_default=True,
    help="Number of required PR reviews",
)
@click.option(
    "--admin-bypass/--no-admin-bypass",
    default=True,
    show_default=True,
    help="Allow repo admins to bypass branch protection",
)
@click.argument("repos", nargs=-1)
def enforce(apply_all, org, require_reviews, admin_bypass, repos):
    """Enforce GitFlow branching rules across repositories."""
    client = get_github_client()
    requested_repos = []
    for entry in repos:
        requested_repos.extend([r.strip() for r in entry.split(",") if r.strip()])

    if not apply_all and not requested_repos:
        console.print("[yellow]Please provide repositories or use --all.[/yellow]")  # type: ignore
        return

    try:
        all_repos = get_repos(client, org)
        valid_repos = [r for r in all_repos if r.name in requested_repos] if requested_repos else list(all_repos)

        # Deduplicate
        seen = set()
        unique_repos = [r for r in valid_repos if r.name not in seen and not seen.add(r.name)]  # type: ignore

        results = []
        for repo in unique_repos:
            res = process_repo_enforcement(repo, admin_bypass, require_reviews)
            results.append((repo.name, res))

        # Table
        table = Table(title="Enforcement Summary", show_lines=True)
        table.add_column("Repository", style="cyan")
        table.add_column("Result")
        for name, result in results:
            table.add_row(name, result)
        console.print(table)  # type: ignore

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")  # type: ignore
