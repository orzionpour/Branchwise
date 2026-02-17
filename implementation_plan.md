# Branchwise Implementation Plan

This plan outlines the steps to build **Branchwise**, an intelligent code review agent.

## Phase 1: Foundation & Setup
- [x] **Project Setup**:
    - Create directory structure (`branchwise/`, `tests/`, etc.).
    - Setup `pyproject.toml` using Poetry or standard setuptools.
    - Define dependencies: `typer`, `pydantic`, `PyGithub`, `openai`, `rich` (for CLI output), `python-dotenv`.
- [x] **Configuration Module**:
    - Create `branchwise/config` module.
    - Define `Settings` model using `pydantic-settings` to load config from `.env` and `branchwise.yaml` (optional).
    - Handle API keys (GITHUB_TOKEN, OPENAI_API_KEY) securely.

## Phase 2: Core Logic - GitHub Integration & Diff Parsing
- [x] **GitHub Client**:
    - Implement `branchwise/integrations/github.py` using `PyGithub`.
    - Functions to:
        - Authenticate with token.
        - Fetch PR details (title, description).
        - Fetch file list and raw content.
        - Fetch patch/diff data.
- [x] **Diff Parsing**:
    - Create utility to parse git diffs.
    - Extract changing lines and context for AI analysis.
    - Map file paths and line numbers correctly.

## Phase 3: AI Analysis Engine
- [x] **LLM Interface**:
    - Create `branchwise/llm` module.
    - Implement an `LLMClient` abstract base class.
    - Implement `OpenAIClient` (and potentially others).
- [x] **Review Logic**:
    - Create `branchwise/core/analyzer.py`.
    - Construct prompts for the LLM based on diff chunks and file context.
    - Structure the prompt to ask for specific types of feedback (bugs, style, performance).
    - Parse LLM response into structured `ReviewComment` objects.

## Phase 4: Reporting & Feedback Loop
- [x] **Comment Posting**:
    - Add functionality to `branchwise/integrations/github.py` to post comments on the PR.
    - Support line-specific comments (review comments) vs general PR comments.
    - Implement logic to avoid duplicate comments on subsequent runs.
- [x] **Review Summary**:
    - Generate a high-level summary of the review findings.

## Phase 5: CLI Interface
- [x] **CLI Implementation**:
    - Create `branchwise/cli/main.py`.
    - Implement `branchwise review <pr_url>` command.
    - Add flags: `--dry-run` (print suggestions without posting), `--config <path>`.
    - Use `rich` library for pretty printing results to the terminal.

## Phase 6: Testing & Polish
- [x] **Testing**:
    - Write unit tests for configuration loading.
    - Write tests for diff parsing logic.
    - Write integration tests with mocked GitHub/LLM responses.
- [x] **Documentation**:
    - Update `README.md` with installation and usage guide.
    - Document configuration options.
