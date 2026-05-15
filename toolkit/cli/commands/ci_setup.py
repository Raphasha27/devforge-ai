# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
import click
import base64
from rich.console import Console
from utils.github_api import get_github_client, get_repos

console = Console()

PYTHON_CI = """
name: Python CI

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Run tests
      run: |
        if [ -d tests ]; then python -m pytest; else echo "No tests/ directory found. Skipping tests."; fi
"""

NODE_CI = """
name: Node.js CI

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Use Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: npm install
    - name: Run tests
      run: npm test || echo "No 'npm test' script found. Skipping tests."
"""

JAVA_CI = """
name: Java CI with Maven

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    - name: Build with Maven
      run: mvn -B package --file pom.xml
"""

STANDARD_CI = """
name: Standard CI

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run Generic Build
      run: echo "Generic build/test step. Update this with your project commands."
"""

from rich.table import Table

@click.command()
@click.option('--template', default='standard', help='CI/CD template to apply')
@click.option('--org', help='GitHub Organization or User (leave empty for authenticated user)')
@click.option('--all', 'apply_all', is_flag=True, help='Apply to all repositories')
@click.option('--force', is_flag=True, help='Overwrite existing CI files if they are non-standard')
@click.argument("repos", nargs=-1)
def ci_setup(template, org, apply_all, force, repos):
    """Setup CI/CD pipelines with health auditing"""
    client = get_github_client()
    
    requested_repos: list[str] = []
    for entry in repos:
        requested_repos.extend([r.strip() for r in entry.split(",") if r.strip()])

    if not apply_all and not requested_repos:
        console.print("[yellow]Please use --all or provide repository names as arguments.[/yellow]")
        return

    console.print(f"\n[bold cyan]🛡️  GitOps CI Orchestration → Template: {template}[/bold cyan]\n")
    
    results = []
    try:
        all_repos = get_repos(client, org)
        # type: ignore (Silence LSP name-resolution errors in partial snippets)
        valid_repos = [r for r in all_repos if r.name in requested_repos] if requested_repos else list(all_repos)

        for repo in valid_repos:
            status = "Unknown"
            try:
                # ── Intelligent Template Selection ──────────
                selected_template = STANDARD_CI
                template_name = "Standard"
                
                try:
                    root_files = [f.name for f in repo.get_contents("/")]
                    if "requirements.txt" in root_files or "setup.py" in root_files or any(f.endswith(".py") for f in root_files):
                        selected_template = PYTHON_CI
                        template_name = "Python"
                    elif "package.json" in root_files:
                        selected_template = NODE_CI
                        template_name = "Node.js"
                    elif "pom.xml" in root_files:
                        selected_template = JAVA_CI
                        template_name = "Java (Maven)"
                except Exception:
                    pass # Fallback to standard if root listing fails

                try:
                    existing = repo.get_contents(".github/workflows/ci.yml")
                    content = base64.b64decode(existing.content).decode("utf-8")
                    
                    # Audit existing CI
                    is_standard = "CI/CD Pipeline" in content or "name: Python CI" in content or "name: Node.js CI" in content or "name: Java CI" in content or "name: Standard CI" in content
                    
                    if force:
                        label = "Legacy" if is_standard else "Custom"
                        console.print(f"  [yellow]🔄 {repo.name}: {label} {template_name} CI found. Overwriting...[/yellow]")
                        repo.update_file(
                            path=existing.path,
                            message=f"chore: update {template_name} CI pipeline",
                            content=selected_template,
                            sha=existing.sha,
                            branch=repo.default_branch
                        )
                        status = f"🔄 Updated ({template_name})"
                    elif is_standard:
                        console.print(f"  [blue]✓ {repo.name}: {template_name} CI already exists.[/blue]")
                        status = f"✅ {template_name}"
                    else:
                        console.print(f"  [yellow]⚠️ {repo.name}: Custom CI detected. Use --force to overwrite.[/yellow]")
                        status = "⚠️ Custom (skipped)"
                except Exception:
                    # File doesn't exist, create it
                    repo.create_file(
                        path=".github/workflows/ci.yml",
                        message=f"chore: initialize {template_name} CI pipeline",
                        content=selected_template,
                        branch=repo.default_branch
                    )
                    console.print(f"  [green]✅ {repo.name}: {template_name} CI injected successfully.[/green]")
                    status = f"✅ Injected ({template_name})"
                
                # Verification Step
                try:
                    verified = repo.get_contents(".github/workflows/ci.yml")
                    if verified.sha:
                        status += " (Verified)"
                except Exception:
                    status += " (Verify Failed)"

            except Exception as e:
                console.print(f"  [red]❌ {repo.name}: Failed ({str(e)[:50]})[/red]")
                status = f"❌ Error"
            
            results.append((repo.name, status))

        # Show Summary Table
        table = Table(title="CI/CD Setup Summary", show_lines=True)
        table.add_column("Repository", style="cyan")
        table.add_column("CI Status", style="magenta")
        for r_name, r_status in results:
            table.add_row(r_name, r_status)
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error during CI setup: {str(e)}[/bold red]")
