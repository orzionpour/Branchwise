import os
from branchwise.config import Settings, load_settings

def test_load_settings_defaults():
    settings = Settings()
    assert settings.llm.model == "gpt-4o"
    assert settings.rules.max_comments == 10

def test_load_settings_from_env(monkeypatch):
    monkeypatch.setenv("BRANCHWISE_LLM__MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("BRANCHWISE_RULES__MAX_COMMENTS", "20")
    
    # We need to re-instantiate Settings to pick up env vars if using pydantic-settings
    # But Settings() reads from os.environ at instantiation time.
    settings = Settings()
    
    assert settings.llm.model == "gpt-3.5-turbo"
    assert settings.rules.max_comments == 20

def test_ignore_files_default():
    settings = Settings()
    assert ".lock" in settings.rules.ignore_files
