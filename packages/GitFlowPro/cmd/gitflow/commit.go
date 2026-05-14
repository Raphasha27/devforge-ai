package main

import (
	"fmt"
	"os/exec"
	"strings"
)

func handleCommit() {
	diff, err := getGitDiff()
	if err != nil {
		fmt.Printf("Error getting git diff: %v\n", err)
		return
	}

	msg := generateCommitMessage(diff)
	fmt.Printf("\n🚀 Suggested Commit Message:\n\n   %s\n", msg)
	fmt.Printf("\nTo use this message, run:\n   git commit -m \"%s\"\n", msg)
}

func getGitDiff() (string, error) {
	cmd := exec.Command("git", "diff", "--staged")
	out, err := cmd.Output()
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(out)), nil
}

func generateCommitMessage(diff string) string {
	if diff == "" {
		return "chore: update repository"
	}

	// Simple heuristic-based generation
	if strings.Contains(diff, "README.md") {
		return "docs: update project documentation"
	}
	if strings.Contains(diff, ".github/workflows") {
		return "ci: enhance github actions workflow"
	}
	if strings.Contains(diff, "package.json") || strings.Contains(diff, "go.mod") {
		return "chore: update dependencies"
	}
	if strings.Contains(diff, "test") {
		return "test: add/update test cases"
	}
	if strings.Contains(diff, "func ") || strings.Contains(diff, "def ") || strings.Contains(diff, "class ") {
		return "feat: implement new core logic"
	}

	return "refactor: optimize internal components"
}
