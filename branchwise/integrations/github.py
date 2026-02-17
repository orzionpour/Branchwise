import logging
from typing import List

from github import Github, GithubException, Auth

from branchwise.config import Settings
from branchwise.integrations.base import PullRequestDetails, PullRequestFile, VCSClient

logger = logging.getLogger(__name__)

class GitHubClient(VCSClient):
    def __init__(self, settings: Settings):
        token = settings.github.token.get_secret_value() if settings.github.token else None
        auth = Auth.Token(token) if token else None
        if not auth:
            logger.warning("GitHub token not provided. GitHub integration will be limited.")
        self.client = Github(auth=auth)

    def get_pr_details(self, repo_name: str, pr_number: int) -> PullRequestDetails:
        """Fetch details of a pull request."""
        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            files = []
            for file in pr.get_files():
                files.append(PullRequestFile(
                    filename=file.filename,
                    status=file.status,
                    patch=file.patch,
                    blob_url=file.blob_url
                ))
            
            return PullRequestDetails(
                number=pr.number,
                title=pr.title,
                description=pr.body or "",
                author=pr.user.login,
                head_sha=pr.head.sha,
                files=files
            )
        except GithubException as e:
            logger.error(f"Error fetching PR details: {e}")
            raise

    def post_comment(self, repo_name: str, pr_number: int, body: str):
        """Post a general comment on the PR."""
        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(body)
        except GithubException as e:
            logger.error(f"Error posting comment: {e}")
            raise

    def post_review_comment(self, repo_name: str, pr_number: int, body: str, commit_id: str, path: str, line: int):
        """Post a specific review comment on a line of code."""
        # Note: GitHub API requires the commit_id to be the latest commit of the PR for the comment to be valid.
        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            # We need to find the correct commit object
            commit = repo.get_commit(commit_id)
            pr.create_review_comment(body, commit, path, line)
        except GithubException as e:
            logger.error(f"Error posting review comment: {e}")
            raise
