import os
import requests

def fetch_github_repos():
    """
    Syncs the user's entire GitHub repository list.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {"error": "GITHUB_TOKEN is not set"}
        
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Failed to fetch repos: {response.status_code}", "details": response.text}
        
    return response.json()
