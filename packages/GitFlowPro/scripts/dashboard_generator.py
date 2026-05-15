import os
import json
from datetime import datetime

OUTPUT_DIR = "dashboard"
DATA_DIR = "compliance_exports/org"

def load_org_report():
    path = "reports/org/org_report.json"
    if not os.path.exists(path):
        return {"generated_at": "N/A", "repos": [], "summary": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def risk_color(risk):
    if risk == "risk:high": return "#ff4d4d"
    if risk == "risk:medium": return "#ffcc00"
    return "#2ecc71"

def generate_html(data):
    repos = data.get("repos", [])
    generated_at = data.get("generated_at", "N/A")
    summary = data.get("summary", {})
    total = summary.get("total_repos", len(repos))
    high = summary.get("high_risk_repos", 0)
    med = summary.get("medium_risk_repos", 0)
    low = summary.get("low_risk_repos", 0)
    rows = ""
    for repo in repos:
        name = repo.get("repo")
        risk = repo.get("risk_label", "risk:low")
        score = repo.get("governance_score", 0)
        approvals = repo.get("required_approvals", 0)
        workflows = repo.get("workflow_count", 0)
        alerts = repo.get("security_alerts", 0)
        rows += f'''
        <tr>
          <td>{name}</td>
          <td style="color:{risk_color(risk)}; font-weight:bold;">{risk}</td>
          <td>{score}/100</td>
          <td>{approvals}</td>
          <td>{workflows}</td>
          <td>{alerts}</td>
        </tr>
        '''
    html = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1.0" />
  <title>GitFlowPro Governance Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 0; }}
    header {{ padding: 24px; background: #161b22; border-bottom: 1px solid #30363d; }}
    h1 {{ margin: 0; font-size: 22px; }}
    .meta {{ margin-top: 8px; font-size: 14px; color: #8b949e; }}
    .container {{ padding: 24px; }}
    .cards {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }}
    .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 16px; min-width: 160px; flex: 1; }}
    .card h2 {{ margin: 0; font-size: 14px; color: #8b949e; }}
    .card p {{ margin: 8px 0 0 0; font-size: 22px; font-weight: bold; }}
    table {{ width: 100%; border-collapse: collapse; background: #161b22; border: 1px solid #30363d; border-radius: 10px; overflow: hidden; }}
    th, td {{ padding: 12px; border-bottom: 1px solid #30363d; text-align: left; font-size: 14px; }}
    th {{ background: #0d1117; color: #8b949e; }}
    footer {{ padding: 20px; text-align: center; color: #8b949e; font-size: 12px; }}
  </style>
</head>
<body>
<header>
  <h1>GitFlowPro Governance Dashboard (v3)</h1>
  <div class="meta">Generated at: {generated_at}</div>
</header>
<div class="container">
  <div class="cards">
    <div class="card"><h2>Total Repos</h2><p>{total}</p></div>
    <div class="card"><h2>Low Risk</h2><p>{low}</p></div>
    <div class="card"><h2>Medium Risk</h2><p>{med}</p></div>
    <div class="card"><h2>High Risk</h2><p>{high}</p></div>
  </div>
  <table>
    <thead>
      <tr><th>Repository</th><th>Risk</th><th>Governance Score</th><th>Required Approvals</th><th>Workflows</th><th>Security Alerts</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>
<footer>GitFlowPro Governance Engine v3 · Generated automatically by GitHub Actions</footer>
</body>
</html>'''
    return html

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = load_org_report()
    html = generate_html(data)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard generated at dashboard/index.html")

if __name__ == "__main__":
    main()
