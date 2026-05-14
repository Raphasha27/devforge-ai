# 🚀 GitFlowPro
**The Ultimate Enterprise-Grade GitHub Automation & Intelligence Toolkit**

[![Go Report Card](https://goreportcard.com/badge/github.com/Raphasha27/GitFlowPro)](https://goreportcard.com/report/github.com/Raphasha27/GitFlowPro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Security Scan](https://github.com/Raphasha27/GitFlowPro/actions/workflows/security-scan.yml/badge.svg)](https://github.com/Raphasha27/GitFlowPro/actions/workflows/security-scan.yml)

GitFlowPro is a high-performance, security-first automation suite built in **Go**. It is designed to transform complex multi-repository environments into streamlined, self-managing, and intelligent workspaces. Whether you are managing a single project or an entire organization, GitFlowPro provides the tools you need to ensure code quality, security compliance, and developer productivity.

---

## 📖 Table of Contents
1. [Core Features](#-core-features)
2. [Architecture Overview](#-architecture-overview)
3. [Multi-Repo Management](#-multi-repo-management)
4. [AI-Powered Intelligence](#-ai-powered-intelligence)
5. [Security & Compliance](#-security--compliance)
6. [Installation & Setup](#-installation--setup)
7. [CLI Usage](#-cli-usage)
8. [Workflow Automation](#-workflow-automation)
9. [Project Structure](#-project-structure)
10. [Contributing](#-contributing)
11. [License](#-license)

---

## 🛠️ Core Features

### 1. 🤖 AI-Powered Intelligence
*   **AI Commit Generator**: Instantly generate semantic, descriptive commit messages based on your staged changes.
*   **AI PR Reviewer (RepoPilot)**: Automatically summarizes PRs, flags security/performance risks, and assigns risk-based labels (`risk:low`, `risk:medium`, `risk:high`).
*   **AI Test Generator**: Automatically generates `pytest` or `Jest` unit tests for PR changes and opens a specialized test PR for your review.

### 2. ⚡ Automation & Workflow
*   **Smart Labeler**: Automatically categorizes PRs and Issues based on deep file path analysis and content inspection.
*   **PR Size Labeler**: Flags large PRs to encourage smaller, more reviewable atomic changes.
*   **Stale Cleanup**: Automatically manages inactive issues and PRs to keep your backlog clean and relevant.
*   **Semantic Release**: Automated versioning and changelog generation following the Semantic Versioning (SemVer) standard.

### 3. 🛡️ Security & Compliance
*   **CodeQL Scanning**: Real-time static analysis to detect common vulnerabilities and code smells.
*   **Secret Protection**: Integrated `gitleaks` scanning to prevent sensitive credentials from ever entering your history.
*   **Principle of Least Privilege**: All GitHub Actions are hardened with strictly scoped permissions.
*   **CODEOWNERS Integration**: Ensures that every change is reviewed by the right person automatically.

### 4. 📊 Analytics & Reporting
*   **Multi-Repo Pulse**: Generate aggregated reports across multiple repositories to track team velocity and repository health.
*   **Discord/Slack Integration**: Automated delivery of weekly reports to your preferred communication channels.

---

## 🏗️ Architecture Overview
GitFlowPro is built on a hybrid architecture that combines the performance of a compiled **Go CLI** with the flexibility of **GitHub Actions** and **Python scripts**.

*   **Go CLI (`cmd/gitflow`)**: Handles heavy-duty data processing, multi-repo aggregation, and local developer tools (like the commit generator).
*   **GitHub Actions**: Serves as the orchestration layer, triggering automation events based on repository state changes.
*   **Python Scripts**: Used for lightweight API integrations and specialized reporting logic where rapid iteration is key.

---

## 🌐 Multi-Repo Management
GitFlowPro is uniquely designed to handle multiple repositories from a single installation. You can configure the toolkit to track several projects simultaneously.

### How to Configure Multi-Repo
1.  **Environment Variable**: Set `REPO_NAME` for single-repo focus.
2.  **Config File**: Edit `configs/repos.json` to list all repositories you want to track:
    ```json
    {
      "repos": [
        "your-org/backend-api",
        "your-org/frontend-app",
        "your-org/shared-utils"
      ]
    }
    ```
3.  **Aggregation**: Running `./gitflow report` will now iterate through all listed repos and provide a consolidated status.

---

## 🤖 AI Configuration
The AI features require an OpenAI API Key.

1.  **Local Usage**: Add `OPENAI_API_KEY` to your local environment.
2.  **GitHub Actions**: Add `OPENAI_API_KEY` to your GitHub Repository Secrets.

---

## 🛡️ Security & Compliance
We prioritize the safety of your code. GitFlowPro includes:
*   **Vulnerability Scanning**: Automated CodeQL scans for Go, Python, and JavaScript.
*   **Credential Leak Prevention**: Immediate detection of secrets in PRs.
*   **Hardened Permissions**: Workflows run with the minimum `contents: read` permissions required.

For more details, see our [SECURITY.md](./.github/SECURITY.md).

---

## 🚀 Installation & Setup

### Prerequisites
*   **Go 1.21+**
*   **Python 3.11+**
*   **GitHub Personal Access Token (PAT)** with `repo` and `workflow` scopes.

### Quick Start
```powershell
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/GitFlowPro.git

# 2. Build the CLI
go build -o gitflow.exe ./cmd/gitflow

# 3. Initialize Git
git init

# 4. Set Environment Variables
$env:GH_TOKEN="your_token"
$env:REPO_NAME="your_user/your_repo"
```

---

## 💻 CLI Usage
The `gitflow` CLI is the Swiss Army knife for your development workflow.

*   **`./gitflow commit`**: Generate an AI commit message for staged changes.
*   **`./gitflow report`**: Generate a status report for all configured repositories.
*   **`./gitflow analytics`**: Run deep performance analytics.
*   **`./gitflow help`**: Display help information.

---

## 📂 Project Structure
```text
GitFlowPro/
├── .github/
│   ├── ISSUE_TEMPLATE/     # Standardized Bug & Feature templates
│   ├── workflows/          # CI/CD & Automation pipelines
│   ├── CODEOWNERS          # Reviewer assignment rules
│   └── SECURITY.md         # Security policy & reporting
├── cmd/gitflow/            # Go CLI Source (Core logic)
├── configs/                # Automation & Multi-repo configurations
├── scripts/                # Python-based automation utilities
├── docs/                   # Extended documentation
├── go.mod                  # Go module definition
├── package.json            # Semantic release configuration
└── README.md               # You are here
```

---

## 🤝 Contributing
We love our contributors! Whether you are fixing a bug, adding a feature, or improving documentation, your help is welcome.

1. Read our [Contributing Guide](./CONTRIBUTING.md).
2. Follow our [Code of Conduct](./CODE_OF_CONDUCT.md).
3. Check the [Open Issues](https://github.com/Raphasha27/GitFlowPro/issues).

---

## ❤️ Community & Support
*   **Issues**: For bug reports and feature requests.
*   **Discussions**: For general questions and community sharing.
*   **Security**: Please report vulnerabilities via the [Security Policy](./.github/SECURITY.md).

---
<p align="center">
  Built with ❤️ for the Developer Community by <b>GitFlowPro Contributors</b>
</p>
