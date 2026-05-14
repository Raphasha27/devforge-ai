import os
import httpx

class GitHubProjectsClient:
    """
    GraphQL Client for GitHub Projects (V2).
    Allows DevForge to manage project boards, fields, and items.
    """
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.endpoint = "https://api.github.com/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def execute_query(self, query: str, variables: dict = None):
        """Executes a GraphQL query against GitHub API."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json={"query": query, "variables": variables},
                headers=self.headers
            )
            return response.json()

    async def get_user_projects(self, login: str):
        """Fetches all projects for a specific user."""
        query = """
        query($login: String!) {
          user(login: $login) {
            projectsV2(first: 20) {
              nodes {
                id
                title
                number
                url
              }
            }
          }
        }
        """
        return await self.execute_query(query, {"login": login})

    async def create_project(self, owner_id: str, title: str):
        """Creates a new GitHub Project V2."""
        query = """
        mutation($ownerId: ID!, $title: String!) {
          createProjectV2(input: {ownerId: $ownerId, title: $title}) {
            projectV2 {
              id
              url
            }
          }
        }
        """
        return await self.execute_query(query, {"ownerId": owner_id, "title": title})

    async def add_item_to_project(self, project_id: str, content_id: str):
        """Adds an Issue or PR to a Project."""
        query = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
            item {
              id
            }
          }
        }
        """
        return await self.execute_query(query, {"projectId": project_id, "contentId": content_id})
