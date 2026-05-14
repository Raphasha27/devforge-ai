package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "commit":
		handleCommit()
	case "report":
		handleReport()
	case "analytics":
		handleAnalytics()
	case "setup":
		handleSetup()
	case "help":
		printUsage()
	default:
		fmt.Printf("Unknown command: %s\n", command)
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Println("GitFlowPro CLI - Automation & Intelligence")
	fmt.Println("\nUsage:")
	fmt.Println("  gitflow <command> [arguments]")
	fmt.Println("\nCommands:")
	fmt.Println("  commit     Generate an AI commit message based on staged changes")
	fmt.Println("  report     Generate a weekly repository status report")
	fmt.Println("  analytics  Run repository performance analytics")
	fmt.Println("  setup      Install local Git hooks for auto-formatting")
	fmt.Println("  help       Show this help message")
}
