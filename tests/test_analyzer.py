from unittest.mock import Mock, MagicMock
from branchwise.core.analyzer import Analyzer, AnalysisResult
from branchwise.config import Settings
from branchwise.integrations.base import PullRequestDetails, PullRequestFile
from branchwise.llm.client import ReviewComment

def test_analyzer_ignores_files():
    mock_settings = Settings()
    mock_settings.rules.ignore_files = [".lock"]
    
    mock_llm = Mock()
    mock_llm.analyze_diff.return_value = []
    
    analyzer = Analyzer(mock_settings, mock_llm)
    
    pr_file_ignored = PullRequestFile(filename="foo.lock", status="modified", patch="foo", blob_url="http://foo")
    pr_file_ok = PullRequestFile(filename="bar.py", status="modified", patch="bar", blob_url="http://bar")
    
    pr_details = PullRequestDetails(
        number=1,
        title="Test PR",
        description="Desc",
        author="User",
        head_sha="sha",
        files=[pr_file_ignored, pr_file_ok]
    )
    
    result = analyzer.analyze_pr(pr_details)
    
    # Should only analyze bar.py
    mock_llm.analyze_diff.assert_called_once()
    args, _ = mock_llm.analyze_diff.call_args
    assert args[0] == "bar.py"

def test_analyzer_aggregates_comments():
    mock_settings = Settings()
    mock_llm = Mock()
    
    comment = ReviewComment(
        file_path="foo.py",
        line_number=10,
        content="Fix this",
        type="bug",
        severity="major"
    )
    mock_llm.analyze_diff.return_value = [comment]
    
    analyzer = Analyzer(mock_settings, mock_llm)
    
    pr_file = PullRequestFile(filename="foo.py", status="modified", patch="patch", blob_url="url")
    pr_details = PullRequestDetails(
        number=1, title="PR", description="", author="User", head_sha="sha", files=[pr_file]
    )
    
    result = analyzer.analyze_pr(pr_details)
    
    assert len(result.comments) == 1
    assert result.comments[0].content == "Fix this"
    assert "foo.py" in result.summary
