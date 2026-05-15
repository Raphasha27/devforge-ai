package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

func handleCommit() {
	fmt.Println("🤖 Analyzing staged changes with RepoPilot AI...")
	diff, err := getGitDiff()
	if err != nil {
		fmt.Printf("❌ Error getting git diff: %v\n", err)
		return
	}

	if diff == "" {
		fmt.Println("⚠️ No staged changes found. Stage some files first using 'git add'.")
		return
	}

	msg := generateCommitMessage(diff)
	fmt.Printf("\n🚀 AI Suggested Commit Message:\n\n   %s\n", msg)
	fmt.Printf("\nRun this command to commit:\n   git commit -m \"%s\"\n", msg)
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
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		return "feat: add/update core project components"
	}

	model := os.Getenv("OPENAI_MODEL")
	if model == "" {
		model = "gpt-4o-mini"
	}

	prompt := fmt.Sprintf("Write a concise, one-line semantic commit message based on the following git diff. Return ONLY the message, no quotes or explanation:\n\n%s", diff)
	if len(prompt) > 8000 {
		prompt = prompt[:8000]
	}

	requestBody, _ := json.Marshal(map[string]interface{}{
		"model": model,
		"messages": []map[string]string{
			{"role": "system", "content": "You are a professional software engineer."},
			{"role": "user", "content": prompt},
		},
		"temperature": 0.2,
	})

	req, _ := http.NewRequest("POST", "https://api.github.com/v1/chat/completions", bytes.NewBuffer(requestBody))
	// Wait, the endpoint for OpenAI is not github.com. It's api.openai.com.
	// But the user might be using a proxy. However, standard is:
	req, _ = http.NewRequest("POST", "https://api.openai.com/v1/chat/completions", bytes.NewBuffer(requestBody))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+apiKey)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("⚠️ AI unavailable (%v). Falling back to heuristic generation.\n", err)
		return fallbackMessage(diff)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("⚠️ AI returned status %d. Falling back to heuristic generation.\n", resp.StatusCode)
		return fallbackMessage(diff)
	}

	body, _ := io.ReadAll(resp.Body)
	var result struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
	}

	if err := json.Unmarshal(body, &result); err != nil || len(result.Choices) == 0 {
		return fallbackMessage(diff)
	}

	return strings.TrimSpace(result.Choices[0].Message.Content)
}

func fallbackMessage(diff string) string {
	if strings.Contains(diff, "README.md") {
		return "docs: update project documentation"
	}
	if strings.Contains(diff, ".github/workflows") {
		return "ci: update github actions workflow"
	}
	if strings.Contains(diff, "package.json") || strings.Contains(diff, "go.mod") {
		return "chore: update dependencies"
	}
	if strings.Contains(diff, "test") {
		return "test: add/update test cases"
	}
	if strings.Contains(diff, "func ") || strings.Contains(diff, "def ") {
		return "feat: implement new core logic"
	}
	return "refactor: optimize internal components"
}
