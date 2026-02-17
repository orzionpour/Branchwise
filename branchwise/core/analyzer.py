import logging
from typing import List, Optional

from pydantic import BaseModel

from branchwise.config import Settings
from branchwise.integrations.github import PullRequestDetails, PullRequestFile
from branchwise.llm.client import LLMClient, ReviewComment
from branchwise.utils.diff_parser import DiffParser


class AnalysisResult(BaseModel):
    summary: str
    comments: List[ReviewComment]


class Analyzer:
    def __init__(self, settings: Settings, llm_client: LLMClient):
        self.settings = settings
        self.llm_client = llm_client
        self.logger = logging.getLogger(__name__)

    def analyze_pr(self, pr_details: PullRequestDetails) -> AnalysisResult:
        """
        Analyze the pull request and return a list of comments.
        """
        all_comments = []
        summary_points = []
        
        for file in pr_details.files:
            if self._should_ignore_file(file.filename):
                self.logger.info(f"Skipping ignored file: {file.filename}")
                continue
            
            if file.status == "removed":
                continue
                
            if not file.patch:
                self.logger.warning(f"No patch available for file: {file.filename}")
                continue

            self.logger.info(f"Analyzing file: {file.filename}")
            file_comments = self._analyze_file(file)
            all_comments.extend(file_comments)
            
            if file_comments:
                summary_points.append(f"- {file.filename}: {len(file_comments)} issues found.")

        summary = "\n".join(summary_points) if summary_points else "No significant issues found."
        
        return AnalysisResult(
            summary=summary,
            comments=all_comments
        )

    def _analyze_file(self, file: PullRequestFile) -> List[ReviewComment]:
        """
        Analyze a single file diff using LLM.
        """
        # Parse diff to get context if needed, but for simplicity pass raw patch to LLM with line numbers annotated?
        # Actually LLMs are good at raw diffs if formatted well.
        # But to be precise about line numbers for comments, we need to map diff lines to file lines.
        
        # Simpler approach: Ask LLM to return line number relative to the file.
        # But LLM only sees the diff snippet. It needs to know the starting line number of the hunk.
        
        # Let's use the DiffParser to structure the input better for the LLM.
        diff_changes = DiffParser.parse(file.patch)
        
        # Construct a more detailed prompt with line numbers
        annotated_diff = []
        for hunk in diff_changes:
            annotated_diff.append(f"Hunk starting at line {hunk.new_line_start}:")
            for line, line_num in hunk.lines:
                prefix = f"{line_num}:" if line_num else "   "
                annotated_diff.append(f"{prefix} {line}")
        
        full_diff_text = "\n".join(annotated_diff)
        
        comments = self.llm_client.analyze_diff(file.filename, full_diff_text)
        return comments

    def _should_ignore_file(self, filename: str) -> bool:
        """Check if file should be ignored based on settings."""
        for pattern in self.settings.rules.ignore_files:
            if filename.endswith(pattern):
                return True
        return False
