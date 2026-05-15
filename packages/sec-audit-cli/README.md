# 🛡️ sec-audit-cli
![Health-Hub](https://img.shields.io/badge/Health--Hub-%E2%9C%94-00D1FF?style=flat-square)

**Sec-Audit** is a lightweight, high-speed dependency vulnerability scanner designed for Python ecosystems. It provides instant feedback on the security status of your `requirements.txt` file, helping you catch known vulnerabilities before they reach production.

## 🚀 Features

-   **🔍 Instant Scan**: Analyzes your entire dependency list in milliseconds.
-   **🛡️ Vulnerability Mapping**: Cross-references package versions against known security advisories.
-   **📊 Clear Reporting**: Generates a high-fidelity dashboard of your ecosystem's security health.
-   **⚙️ CI/CD Integration**: Perfect for pre-push hooks to ensure zero vulnerable code is committed.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Raphasha27/sec-audit-cli.git
cd sec-audit-cli

# Install dependencies
pip install typer rich requests
```

## ⌨️ Usage

### Audit your requirements
```bash
python audit.py scan requirements.txt
```

---
*Built with ❤️ by Koketso Raphasha using DevForge AI (Automated 1 PM Launch).*
