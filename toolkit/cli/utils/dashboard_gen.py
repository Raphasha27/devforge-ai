# pyright: reportMissingImports=false
# pyright: reportGeneralTypeIssues=false
import os
from datetime import datetime
from utils.github_api import get_github_client, get_repos

def generate_html(repos_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cards_html = ""
    for r in repos_data:
        compliance_class = 'badge-success' if r['compliance'] == '✅' else 'badge-danger'
        risk_class = 'badge-success' if r['risk'] == 'Low' else 'badge-danger' if r['risk'] == 'High' else 'badge-warning'
        ci_color = 'var(--success)' if r['ci'] == 'Standard' else 'var(--warning)'
        prot_color = 'var(--success)' if r['protection'] else 'var(--danger)'
        readme_color = 'var(--success)' if r['readme'] else 'var(--danger)'
        
        cards_html += f"""
            <div class="repo-card">
                <div>
                    <div class="repo-name">{r['name']}</div>
                    <div class="repo-meta">
                        <span>{r['default_branch']}</span>
                        <span>{r['language'] or 'Mixed'}</span>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="badge {compliance_class}">
                            GitFlow: {r['compliance']}
                        </span>
                        <span class="badge {risk_class}">
                            Risk: {r['risk']}
                        </span>
                    </div>
                </div>
                <div class="repo-health">
                    <div class="indicator-group">
                        <div class="indicator active" style="background: {ci_color}; box-shadow: 0 0 8px {ci_color}" title="CI Status"></div>
                        <div class="indicator active" style="background: {prot_color}; box-shadow: 0 0 8px {prot_color}" title="Branch Protection"></div>
                        <div class="indicator active" style="background: {readme_color}; box-shadow: 0 0 8px {readme_color}" title="Documentation"></div>
                    </div>
                    <div style="font-size: 0.7rem; color: var(--text-dim);">
                        Last Push: {r['last_push']}
                    </div>
                </div>
            </div>
        """

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevForge AI | Control Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #050505;
            --card-bg: rgba(20, 20, 22, 0.7);
            --accent-primary: #00f2ff;
            --accent-secondary: #ff00e5;
            --text-main: #e0e0e0;
            --text-dim: #888;
            --success: #00ff88;
            --warning: #ffcc00;
            --danger: #ff4d4d;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background: var(--bg);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(0, 242, 255, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(255, 0, 229, 0.05) 0%, transparent 40%);
        }}

        header {{
            padding: 40px 60px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .logo {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }}

        .stats-bar {{
            display: flex;
            gap: 30px;
        }}

        .stat-item {{
            text-align: right;
        }}

        .stat-value {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--accent-primary);
        }}

        .stat-label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-dim);
        }}

        main {{
            padding: 60px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}

        .repo-card {{
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 25px;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .repo-card:hover {{
            transform: translateY(-8px);
            border-color: rgba(0, 242, 255, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }}

        .repo-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(to right, transparent, var(--accent-primary), transparent);
            opacity: 0;
            transition: opacity 0.4s;
        }}

        .repo-card:hover::before {{
            opacity: 1;
        }}

        .repo-name {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #fff;
        }}

        .repo-meta {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            font-size: 0.8rem;
            color: var(--text-dim);
        }}

        .badge {{
            padding: 4px 10px;
            border-radius: 100px;
            font-weight: 600;
            font-size: 0.7rem;
            text-transform: uppercase;
        }}

        .badge-success {{ background: rgba(0, 255, 136, 0.1); color: var(--success); }}
        .badge-warning {{ background: rgba(255, 204, 0, 0.1); color: var(--warning); }}
        .badge-danger {{ background: rgba(255, 77, 77, 0.1); color: var(--danger); }}
        .badge-neutral {{ background: rgba(255, 255, 255, 0.05); color: #ccc; }}

        .repo-health {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .indicator-group {{
            display: flex;
            gap: 8px;
        }}

        .indicator {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #333;
        }}

        .indicator.active {{
            /* Box-shadow applied dynamically */
        }}

        .footer {{
            padding: 40px 60px;
            text-align: center;
            color: var(--text-dim);
            font-size: 0.8rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }}

        @keyframes pulse {{
            0% {{ opacity: 0.4; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.4; }}
        }}

        .live-dot {{
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
    </style>
</head>
<body>
    <header>
        <div>
            <div class="logo">DevForge AI</div>
            <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 5px;">
                <span class="live-dot"></span> Ecosystem Control Hub
            </div>
        </div>
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{len(repos_data)}</div>
                <div class="stat-label">Total Repos</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{sum(1 for r in repos_data if r['compliance'] == '✅')}</div>
                <div class="stat-label">Compliant</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{sum(1 for r in repos_data if r['risk'] == 'Low')}</div>
                <div class="stat-label">Secure</div>
            </div>
        </div>
    </header>

    <main>
        <div class="grid">
            {cards_html}
        </div>
    </main>

    <div class="footer">
        Generated by DevForge AI Orchestrator • {now} • System v2.1
    </div>
</body>
</html>
"""
    return html_template

def build_dashboard():
    client = get_github_client()
    repos = list(get_repos(client))
    
    repos_data = []
    for repo in repos:
        # Basic Audit
        try:
            contents = [f.name for f in repo.get_contents("")]
        except:
            contents = []
            
        branches = [b.name for b in repo.get_branches()]
        has_develop = "develop" in branches
        is_protected = False
        try:
            main_branch = repo.get_branch(repo.default_branch)
            is_protected = main_branch.protected
        except:
            pass
            
        ci_status = "Missing"
        if ".github" in contents:
            try:
                workflows = [f.name for f in repo.get_contents(".github/workflows")]
                if "ci.yml" in workflows:
                    ci_status = "Standard"
            except:
                pass

        risk = "Low"
        if any(f.endswith(".env") or f == "secrets.json" for f in contents):
            risk = "High"
        elif ".gitignore" not in contents:
            risk = "Medium"

        repos_data.append({
            "name": repo.name,
            "default_branch": repo.default_branch,
            "language": repo.language,
            "compliance": "✅" if has_develop else "❌",
            "protection": is_protected,
            "risk": risk,
            "ci": ci_status,
            "readme": any(f.lower() == "readme.md" for f in contents),
            "last_push": repo.pushed_at.strftime("%Y-%m-%d")
        })

    html = generate_html(repos_data)
    target_path = os.path.join("c:\\Users\\nelso\\OneDrive\\Desktop\\Branch", "index.html")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html)
    return target_path

if __name__ == "__main__":
    path = build_dashboard()
    print(f"Dashboard generated at: {path}")
