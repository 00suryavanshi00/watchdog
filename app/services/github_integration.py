from typing import Optional, Dict, List
import httpx
import base64, logging
from urllib.parse import urlparse

logger = logging.getLogger("pr_analysis")

class GitHubService:
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    async def _make_request(self, url: str, method: str = "GET") -> Dict:
        """Make authenticated request to GitHub API"""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                follow_redirects=True
            )
            if response.status_code == 404:
                logger.error(f"GitHub API error: 404 Not Found. URL: {url}. Response: {response.text}")
            response.raise_for_status()
            return response.json()

    def parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL"""
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")
        return path_parts[0], path_parts[1]

    async def get_pr_files(self, repo_url: str, pr_number: int) -> List[Dict]:
        """Get list of files changed in PR"""
        owner, repo = self.parse_repo_url(repo_url)
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        return await self._make_request(url)

    async def get_file_content(self, repo_url: str, file_path: str, ref: str) -> str:
        """Get content of a specific file"""
        owner, repo = self.parse_repo_url(repo_url)
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}?ref={ref}"
        response = await self._make_request(url)
        if response.get("encoding") == "base64":
            return base64.b64decode(response["content"]).decode("utf-8")
        return response["content"]

    async def get_pr_diff(self, repo_url: str, pr_number: int) -> Dict[str, Dict]:
        """
        Get complete PR diff with before and after content for each file
        Returns a dictionary with file paths as keys and their diff details as values
        """
        try:
            owner, repo = self.parse_repo_url(repo_url)
            
            # Get PR details to get base and head refs
            pr_url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
            pr_details = await self._make_request(pr_url)
            base_sha = pr_details["base"]["sha"]
            head_sha = pr_details["head"]["sha"]

            # Get list of changed files
            files = await self.get_pr_files(repo_url, pr_number)
            
            diff_details = {}
            for file in files:
                file_path = file["filename"]
                
                # Get file content before and after changes
                try:
                    before_content = await self.get_file_content(repo_url, file_path, base_sha)
                except httpx.HTTPError:
                    before_content = ""  # File might be newly created

                try:
                    after_content = await self.get_file_content(repo_url, file_path, head_sha)
                except httpx.HTTPError:
                    after_content = ""  # File might be deleted

                diff_details[file_path] = {
                    "status": file["status"],  # added, modified, removed
                    "additions": file["additions"],
                    "deletions": file["deletions"],
                    "before_content": before_content,
                    "after_content": after_content,
                    "patch": file.get("patch", ""),  # Unified diff format
                }

            return diff_details

        except httpx.HTTPError as e:
            raise ValueError(f"GitHub API error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error fetching PR diff: {str(e)}")