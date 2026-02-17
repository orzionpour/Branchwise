import logging
from atlassian import Bitbucket
from typing import List

from branchwise.config import Settings
from branchwise.integrations.base import PullRequestDetails, PullRequestFile, VCSClient

logger = logging.getLogger(__name__)

class BitbucketClient(VCSClient):
    def __init__(self, settings: Settings):
        token = settings.bitbucket.token.get_secret_value() if settings.bitbucket.token else None
        url = settings.bitbucket.url
        if not token:
            logger.warning("Bitbucket token not provided. Bitbucket integration will be limited.")
        
        # Atlassian python api handles authentication via token or basicauth.
        # Assuming token is a personal access token.
        self.client = Bitbucket(url=url, token=token)

    def get_pr_details(self, repo_name: str, pr_number: int) -> PullRequestDetails:
        """Fetch details of a PR. Repo name format: PROJECT/REPO"""
        try:
            project_key, repo_slug = repo_name.split("/")
            pr = self.client.get_pull_request(project_key, repo_slug, pr_number)
            diff = self.client.get_pull_request_diff(project_key, repo_slug, pr_number)
            
            # Bitbucket diff output is raw diff, need to parse.
            # However, `atlassian-python-api` might return dict for some calls.
            # `get_pull_request_diff` returns the raw diff string usually.
            
            # Simple simulation as diff parsing logic is complex
            # We would need to implement robust diff parsing for Bitbucket as it doesn't give clean file objects like GitHub/GitLab APIs sometimes do directly.
            # For this MVP, we will rely on our DiffParser if we get a raw diff.
            
            # Actually, `atlassian-python-api` might not make it easy to list files with their individual diffs without parsing the global diff.
            # We will assume `get_pull_request_diff` returns the full diff and we use DiffParser later.
            # But `PullRequestDetails` expects list of files.
            
            # Let's inspect changes
            changes = self.client.get_pull_request_changes(project_key, repo_slug, pr_number)
            
            files = []
            for change in changes:
                # This depends on API response structure
                pass

            # Placeholder for complex bitbucket implementation
            return PullRequestDetails(
                number=pr['id'],
                title=pr['title'],
                description=pr.get('description', ""),
                author=pr['author']['user']['name'],
                head_sha=pr['fromRef']['latestCommit'],
                files=files
            )
        except Exception as e:
            logger.error(f"Error fetching Bitbucket PR details: {e}")
            raise

    def post_comment(self, repo_name: str, pr_number: int, body: str):
        """Post a general comment on the PR."""
        try:
            project_key, repo_slug = repo_name.split("/")
            self.client.add_pull_request_comment(project_key, repo_slug, pr_number, body)
        except Exception as e:
            logger.error(f"Error posting comment to Bitbucket: {e}")
            raise
