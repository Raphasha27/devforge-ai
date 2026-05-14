package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func handleSetup() {
	fmt.Println("⚙️ Setting up GitFlowPro local environment...")

	hookDir := filepath.Join(".git", "hooks")
	if _, err := os.Stat(hookDir); os.IsNotExist(err) {
		fmt.Println("❌ Error: Not inside a git repository (.git/hooks not found).")
		return
	}

	preCommitPath := filepath.Join(hookDir, "pre-commit")
	
	hookScript := `#!/bin/sh
# GitFlowPro Pre-Commit Hook

echo "🛡️ GitFlowPro: Running local quality gates..."

# Format Go code
if command -v go &> /dev/null; then
    go fmt ./...
fi

# Format Python code
if command -v black &> /dev/null; then
    black . --quiet
fi
if command -v ruff &> /dev/null; then
    ruff check . --fix --quiet
fi

echo "✅ Quality gates passed!"
`

	err := os.WriteFile(preCommitPath, []byte(hookScript), 0755)
	if err != nil {
		fmt.Printf("❌ Error writing pre-commit hook: %v\n", err)
		return
	}

	fmt.Println("✅ Local Git hooks installed successfully!")
	fmt.Println("   Every time you 'git commit', GitFlowPro will auto-format your Go and Python code.")
}
