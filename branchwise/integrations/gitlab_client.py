import logging
import gitlab
from typing import List

from branchwise.config import Settings
from branchwise.integrations.base import PullRequestDetails, PullRequestFile, VCSClient

logger = logging.getLogger(__name__)

class GitLabClient(VCSClient):
    def __init__(self, settings: Settings):
        token = settings.gitlab.token.get_secret_value() if settings.gitlab.token else None
        url = settings.gitlab.url
        if not token:
            logger.warning("GitLab token not provided. GitLab integration will be limited.")
        
        self.client = gitlab.Gitlab(url=url, private_token=token)

    def get_pr_details(self, repo_name: str, pr_number: int) -> PullRequestDetails:
        """Fetch details of a merge request."""
        try:
            # GitLab uses project ID or namespace/project_name
            project = self.client.projects.get(repo_name)
            mr = project.mergerequests.get(pr_number)
            
            files = []
            # Fetch changes
            changes = mr.changes()
            for change in changes['changes']:
                files.append(PullRequestFile(
                    filename=change['new_path'],
                    status="added" if change['new_file'] else "modified" if not change['deleted_file'] else "removed",
                    patch=change['diff'],
                    blob_url=f"{project.web_url}/-/blob/{mr.sha}/{change['new_path']}"
                ))
            
            return PullRequestDetails(
                number=mr.iid,
                title=mr.title,
                description=mr.description or "",
                author=mr.author['username'],
                head_sha=mr.sha,
                files=files
            )
        except Exception as e:
            logger.error(f"Error fetching GitLab MR details: {e}")
            raise

    def post_comment(self, repo_name: str, pr_number: int, body: str):
        """Post a general comment on the MR."""
        try:
            project = self.client.projects.get(repo_name)
            mr = project.mergerequests.get(pr_number)
            mr.notes.create({'body': body})
        except Exception as e:
            logger.error(f"Error posting comment to GitLab: {e}")
            raise
