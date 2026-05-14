package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type GitHubItem struct {
	Number int `json:"number"`
}

type RepoConfig struct {
	Repos []string `json:"repos"`
}

func handleReport() {
	token := os.Getenv("GH_TOKEN")
	if token == "" {
		fmt.Println("Error: GH_TOKEN environment variable must be set.")
		return
	}

	repos := getRepoList()
	if len(repos) == 0 {
		fmt.Println("No repositories configured. Set REPO_NAME or update configs/repos.json")
		return
	}

	fmt.Printf("🚀 Generating Multi-Repo Weekly Report for %d repositories...\n", len(repos))
	fmt.Println("===============================================================")

	for _, repo := range repos {
		generateSingleRepoReport(repo, token)
	}
}

func getRepoList() []string {
	// 1. Try environment variable
	if repo := os.Getenv("REPO_NAME"); repo != "" {
		return []string{repo}
	}

	// 2. Try repos.json
	data, err := os.ReadFile("configs/repos.json")
	if err == nil {
		var config RepoConfig
		if err := json.Unmarshal(data, &config); err == nil {
			return config.Repos
		}
	}

	return []string{}
}

func generateSingleRepoReport(repo, token string) {
	fmt.Printf("\n📊 Repository: %s\n", repo)

	openIssues, err := fetchGitHubData(fmt.Sprintf("https://api.github.com/repos/%s/issues?state=open", repo), token)
	if err != nil {
		fmt.Printf("  ❌ Error fetching issues: %v\n", err)
		return
	}

	openPRs, err := fetchGitHubData(fmt.Sprintf("https://api.github.com/repos/%s/pulls?state=open", repo), token)
	if err != nil {
		fmt.Printf("  ❌ Error fetching PRs: %v\n", err)
		return
	}

	fmt.Printf("  ✅ Open Issues: %d\n", len(openIssues))
	fmt.Printf("  ✅ Open PRs:    %d\n", len(openPRs))
}

func fetchGitHubData(url, token string) ([]GitHubItem, error) {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("Authorization", "token "+token)
	req.Header.Set("Accept", "application/vnd.github+json")

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("GitHub API returned status: %s", resp.Status)
	}

	var items []GitHubItem
	if err := json.NewDecoder(resp.Body).Decode(&items); err != nil {
		return nil, err
	}
	return items, nil
}
