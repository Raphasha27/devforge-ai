import os
import requests
from github import Github

class GithubPublisher:
    """
    Handles automated GitHub repository creation and file management.
    """
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.gh = Github(self.token) if self.token else None

    def create_repository(self, name: str, description: str):
        """
        Creates a new public repository.
        """
        if not self.gh:
            return {"error": "GITHUB_TOKEN not found"}
            
        user = self.gh.get_user()
        try:
            repo = user.create_repo(
                name=name,
                description=description,
                private=False,
                auto_init=True
            )
            return {"status": "created", "url": repo.html_url, "name": repo.name}
        except Exception as e:
            return {"error": str(e)}

    def push_files(self, repo_name: str, files: dict, commit_message: str = "Initial commit by DevForge AI"):
        """
        Pushes a dictionary of {path: content} to the repository.
        """
        if not self.gh:
            return {"error": "GITHUB_TOKEN not found"}
            
        repo = self.gh.get_user().get_repo(repo_name)
        
        results = []
        for path, content in files.items():
            try:
                # Check if file exists to update or create
                try:
                    contents = repo.get_contents(path)
                    repo.update_file(path, commit_message, content, contents.sha)
                    results.append({"path": path, "action": "updated"})
                except:
                    repo.create_file(path, commit_message, content)
                    results.append({"path": path, "action": "created"})
            except Exception as e:
                results.append({"path": path, "error": str(e)})
                
        return results

    def get_repo_stats(self, repo_name: str):
        """
        Retrieves real-time metrics for a repository.
        """
        if not self.gh:
            return {"error": "GITHUB_TOKEN not found"}
            
        try:
            repo = self.gh.get_user().get_repo(repo_name)
            return {
                "name": repo.name,
                "stars_delta": repo.stargazers_count, # Simple delta for mock
                "open_issues": repo.open_issues_count,
                "total_builds": 10, # Mocked
                "failed_builds": 1, # Mocked
                "lines_of_code": 5000 # Mocked
            }
        except Exception as e:
            return {"error": str(e)}
    def get_open_prs(self, repo_name: str):
        """Retrieves all open pull requests for a repository."""
        if not self.gh: return []
        repo = self.gh.get_user().get_repo(repo_name)
        return repo.get_pulls(state='open')

    def comment_on_pr(self, repo_name: str, pr_number: int, comment: str):
        """Posts a comment on a specific pull request."""
        if not self.gh: return False
        repo = self.gh.get_user().get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment)
        return True
