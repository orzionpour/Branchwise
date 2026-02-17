import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel

from branchwise.config import Settings


class ReviewComment(BaseModel):
    file_path: str
    line_number: int
    content: str
    type: str  # "bug", "style", "performance", "security", "doc"
    severity: str # "critical", "major", "minor"


class LLMClient(ABC):
    @abstractmethod
    def analyze_diff(self, file_name: str, diff_content: str, context: Optional[str] = None) -> List[ReviewComment]:
        """Analyze a file diff and return a list of review comments."""
        pass


class OpenAIClient(LLMClient):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.llm.api_key.get_secret_value(),
            base_url=settings.llm.base_url
        )
        self.model = settings.llm.model

    def analyze_diff(self, file_name: str, diff_content: str, context: Optional[str] = None) -> List[ReviewComment]:
        prompt = self._construct_prompt(file_name, diff_content, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Analyze the code changes in the git diff provided."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.settings.llm.max_tokens,
                temperature=0.2, # Low temperature for more deterministic and focused output
            )
            
            content = response.choices[0].message.content
            return self._parse_response(content, file_name)
        except Exception as e:
            logging.error(f"Error calling OpenAI API: {e}")
            return []

    def _construct_prompt(self, file_name: str, diff_content: str, context: Optional[str]) -> str:
        return f"""
        Analyze the following git diff for the file `{file_name}`.
        Identify potential bugs, security vulnerabilities, performance issues, and code style violations.
        
        Return the response strictly in the following format for each issue found:
        
        ---
        Line: <line_number>
        Type: <bug|security|performance|style|doc>
        Severity: <critical|major|minor>
        Content: <description of the issue>
        ---
        
        If no issues are found, return "No issues found."
        
        Diff:
        {diff_content}
        """

    def _parse_response(self, content: str, file_path: str) -> List[ReviewComment]:
        comments = []
        if "No issues found" in content:
            return comments
            
        # Very simple parser - can be improved with regex or JSON mode
        chunks = content.split("---")
        for chunk in chunks:
            if not chunk.strip():
                continue
            
            lines = chunk.strip().split("\n")
            comment_data = {}
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    comment_data[key.strip().lower()] = value.strip()
            
            if "line" in comment_data and "content" in comment_data:
                try:
                    comments.append(ReviewComment(
                        file_path=file_path,
                        line_number=int(comment_data["line"]),
                        content=comment_data["content"],
                        type=comment_data.get("type", "style"),
                        severity=comment_data.get("severity", "minor")
                    ))
                except ValueError:
                    logging.warning(f"Failed to parse line number: {comment_data['line']}")
                    
        return comments
