# Security Policy

## Supported Versions

Only the latest version of GitFlowPro is supported for security updates.

| Version | Supported          |
| ------- | ------------------ |
| v1.x    | :white_check_mark: |
| < v1.0  | :x:                |

## Reporting a Vulnerability

We take the security of GitFlowPro seriously. If you believe you have found a security vulnerability, please do NOT open a public issue. Instead, follow these steps:

1. Send an email to **security@example.com** (replace with your actual contact).
2. Include a detailed description of the vulnerability.
3. Provide steps to reproduce the issue.

We will acknowledge your report within 48 hours and provide a timeline for a fix.

## Security Hardening in GitFlowPro

This repository includes several automated security features:
- **CodeQL Analysis**: Continuous static analysis for vulnerabilities.
- **Secret Scanning**: Automated detection of committed secrets and credentials.
- **Least Privilege**: All GitHub Workflows run with minimal required permissions.
- **Dependency Auditing**: Automated PR scanning for vulnerable packages.
