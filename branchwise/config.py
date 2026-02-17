"""
Configuration management for Branchwise.
"""
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseModel):
    """Configuration for LLM providers."""
    api_key: SecretStr = SecretStr("sk-...")
    model: str = "gpt-4o"
    provider: str = "openai"
    base_url: Optional[str] = None
    max_tokens: int = 4096


class GitHubSettings(BaseModel):
    """Configuration for GitHub integration."""
    token: Optional[SecretStr] = None


class GitLabSettings(BaseModel):
    """Configuration for GitLab integration."""
    token: Optional[SecretStr] = None
    url: str = "https://gitlab.com"


class BitbucketSettings(BaseModel):
    """Configuration for Bitbucket integration."""
    token: Optional[SecretStr] = None
    url: str = "https://bitbucket.org"


class RuleSettings(BaseModel):
    """Configuration for review rules."""
    max_comments: int = 10
    ignore_files: list[str] = [".lock", ".png", ".jpg", ".md"]
    focus_files: list[str] = [".py", ".js", ".ts", ".go", ".java"]


class Settings(BaseSettings):
    """Main application settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        env_prefix="BRANCHWISE_",
    )

    github: GitHubSettings = GitHubSettings()
    gitlab: GitLabSettings = GitLabSettings()
    bitbucket: BitbucketSettings = BitbucketSettings()
    llm: LLMSettings = LLMSettings()
    rules: RuleSettings = RuleSettings()
    
    # Project specific overrides
    config_file: Optional[Path] = None


def load_settings(config_path: Optional[Path] = None) -> Settings:
    """Load settings from environment variables and optional config file."""
    # Logic to load from config_path if provided could be added here
    # For now, rely on pydantic-settings defaults.
    return Settings()
