from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel


class PullRequestFile(BaseModel):
    filename: str
    status: str
    patch: Optional[str] = None
    blob_url: str

class PullRequestDetails(BaseModel):
    number: int
    title: str
    description: str
    author: str
    head_sha: str
    files: List[PullRequestFile]

class VCSClient(ABC):
    """Abstract base class for Version Control System clients."""
    
    @abstractmethod
    def get_pr_details(self, repo_name: str, pr_number: int) -> PullRequestDetails:
        """Fetch details of a pull request."""
        pass

    @abstractmethod
    def post_comment(self, repo_name: str, pr_number: int, body: str):
        """Post a general comment on the PR."""
        pass
