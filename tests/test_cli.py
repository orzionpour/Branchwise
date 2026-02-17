from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from branchwise.main import app
from branchwise.integrations.base import PullRequestDetails, PullRequestFile
from branchwise.llm.client import ReviewComment

runner = CliRunner()

@patch("branchwise.main.load_settings")
@patch("branchwise.integrations.github.GitHubClient")
@patch("branchwise.main.OpenAIClient")
@patch("branchwise.main.Analyzer")
def test_review_command_dry_run(mock_analyzer_cls, mock_openai_cls, mock_github_cls, mock_load_settings):
    # Setup Mocks
    mock_settings = MagicMock()
    mock_settings.github.token = "token"
    mock_settings.gitlab.url = "https://gitlab.com"
    mock_settings.bitbucket.url = "https://bitbucket.org"
    mock_settings.llm.api_key = "key"
    mock_load_settings.return_value = mock_settings

    mock_github_instance = mock_github_cls.return_value
    mock_pr_details = PullRequestDetails(
        number=123,
        title="Test PR",
        description="Description",
        author="User",
        head_sha="sha",
        files=[
            PullRequestFile(filename="test.py", status="modified", patch="diff", blob_url="url")
        ]
    )
    mock_github_instance.get_pr_details.return_value = mock_pr_details

    mock_analyzer_instance = mock_analyzer_cls.return_value
    mock_result = MagicMock()
    mock_result.summary = "Good job!"
    mock_result.comments = [
        ReviewComment(file_path="test.py", line_number=1, content="Issue", type="bug", severity="minor")
    ]
    mock_analyzer_instance.analyze_pr.return_value = mock_result

    # Run Command
    result = runner.invoke(app, ["https://github.com/owner/repo/pull/123", "--dry-run"])

    print(result.stdout)
    if result.exception:
        import traceback
        traceback.print_exception(result.exception)
    # Assertions
    assert result.exit_code == 0
    assert "Starting review for PR #123" in result.stdout
    assert "Found PR: Test PR" in result.stdout
    assert "Review Summary" in result.stdout
    assert "Good job!" in result.stdout
    assert "Dry run mode" in result.stdout
    
    # Verify mock interactions
    mock_github_cls.assert_called_once()
    mock_github_instance.get_pr_details.assert_called_with("owner/repo", 123)
    mock_analyzer_instance.analyze_pr.assert_called_with(mock_pr_details)
    mock_github_instance.post_comment.assert_not_called()

@patch("branchwise.main.load_settings")
def test_review_command_invalid_url(mock_load_settings):
    mock_settings = MagicMock()
    mock_settings.github.token = "token"
    mock_settings.gitlab.url = "https://gitlab.com"
    mock_settings.bitbucket.url = "https://bitbucket.org"
    mock_settings.llm.api_key = "key"
    mock_load_settings.return_value = mock_settings

    result = runner.invoke(app, ["invalid-url"])
    
    # Expect failure due to URL parsing
    assert result.exit_code == 1
    assert "Invalid PR URL format" in result.stdout or "Unsupported URL" in result.stdout
