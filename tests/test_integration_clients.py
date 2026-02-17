from branchwise.config import Settings
from unittest.mock import MagicMock
import pytest

def test_github_client_init():
    from branchwise.integrations.github import GitHubClient
    settings = Settings()
    # Mock token
    settings.github.token = MagicMock()
    settings.github.token.get_secret_value.return_value = "token"
    
    try:
        client = GitHubClient(settings)
    except Exception as e:
        pytest.fail(f"Failed to instantiate GitHubClient: {e}")

def test_gitlab_client_init():
    from branchwise.integrations.gitlab_client import GitLabClient
    settings = Settings()
    settings.gitlab.token = MagicMock()
    settings.gitlab.token.get_secret_value.return_value = "token"
    
    try:
        client = GitLabClient(settings)
    except Exception as e:
        pytest.fail(f"Failed to instantiate GitLabClient: {e}")

def test_bitbucket_client_init():
    from branchwise.integrations.bitbucket_client import BitbucketClient
    settings = Settings()
    settings.bitbucket.token = MagicMock()
    settings.bitbucket.token.get_secret_value.return_value = "token"
    
    try:
        client = BitbucketClient(settings)
    except Exception as e:
        pytest.fail(f"Failed to instantiate BitbucketClient: {e}")
