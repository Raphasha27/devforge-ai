# DevForge CLI Launcher
# Run from ANYWHERE on your system:
#
#   .\devforge.ps1 scan
#   .\devforge.ps1 audit --security repo1 repo2
#   .\devforge.ps1 enforce repo1 repo2
#   .\devforge.ps1 enforce --all
#   .\devforge.ps1 migrate --target-repo devforge-ai --dry-run
#   .\devforge.ps1 migrate --target-repo devforge-ai GitFlowPro flowsentinel env-guardian --push
#   .\devforge.ps1 ci-setup --all --force
#   .\devforge.ps1 ci-setup repo1 repo2

$CLI_DIR = "C:\Users\nelso\OneDrive\Desktop\gitflow-cli"
$PYTHON  = "$CLI_DIR\venv\Scripts\python.exe"

if (-not (Test-Path $PYTHON)) {
    Write-Error "Python venv not found at $PYTHON"
    Write-Host "Run: cd $CLI_DIR && python -m venv venv && .\venv\Scripts\pip install -r requirements.txt"
    exit 1
}

$env:PYTHONIOENCODING = "utf-8"
& $PYTHON "$CLI_DIR\cli.py" @args
