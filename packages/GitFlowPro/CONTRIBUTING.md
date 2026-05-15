# Contributing to GitFlowPro

First off, thank you for considering contributing to GitFlowPro! It's people like you that make GitFlowPro such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](./CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs
*   Check the [issue tracker](https://github.com/Raphasha27/GitFlowPro/issues) to see if the bug has already been reported.
*   If not, open a new issue using the **Bug Report** template.
*   Include as much detail as possible, including your OS, Go version, and steps to reproduce.

### Suggesting Enhancements
*   Open a new issue using the **Feature Request** template.
*   Explain the "why" behind the feature and how it would benefit the community.

### Pull Requests
1.  Fork the repo and create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  If you've changed APIs, update the documentation.
4.  Ensure the test suite passes (`go test ./...`).
5.  Make sure your code lints correctly.
6.  Use semantic commit messages (e.g., `feat: ...`, `fix: ...`).

## Development Setup

1.  Clone your fork: `git clone https://github.com/YOUR_USERNAME/GitFlowPro.git`
2.  Install dependencies: `go mod download`
3.  Build the CLI: `go build -o gitflow ./cmd/gitflow`

## Style Guide
*   **Go**: Follow standard `gofmt` and Go community idioms.
*   **Python**: Follow the rules defined in `pyproject.toml` (Ruff/Black).
*   **Commits**: Use [Conventional Commits](https://www.conventionalcommits.org/).

Thank you for your contributions!
