# Branchwise Implementation Prompt

Develop **Branchwise**, an intelligent code review agent that automates pull request analysis to ensure high-quality code.

## Core Objectives
1.  **Automated PR Analysis**: Fetch pull request details (diffs, files, metadata) from GitHub.
2.  **AI-Powered Review**: Utilize Large Language Models (LLMs) to analyze code changes for:
    - Potential bugs and logic errors.
    - Code style and consistency violations.
    - Performance bottlenecks.
    - Security vulnerabilities.
    - Documentation gaps.
3.  **Actionable Feedback**: Post constructive review comments directly on the PR, or generate a summary report.
4.  **Configurability**: Support a configuration file (e.g., `.branchwise.yaml`) to customize rules, ignored files, and LLM settings.

## Technical Architecture
-   **Language**: Python 3.10+
-   **Structure**:
    -   `branchwise/core`: Core logic for orchestration and review processing.
    -   `branchwise/integrations`: Modules for Git/GitHub API interaction (using `PyGithub` or similar).
    -   `branchwise/llm`: Interface for LLM providers (OpenAI, Anthropic, etc.).
    -   `branchwise/config`: Pydantic-based configuration management.
    -   `branchwise/cli`: CLI entry point using `Typer` or `Click`.
-   **Data Validation**: Use `Pydantic` for robust data modeling.
-   **Testing**: `pytest` for unit and integration tests.

## Features
-   **CLI Command**: `branchwise review --pr <urls>` to trigger a review manually.
-   **Diff Parsing**: accurately parse git diffs to identify changed lines for targeted comments.
-   **Rule Engine**: basic rule engine to filter or prioritize AI suggestions.

## Deliverables
-   Fully functional Python package.
-   Clean, modular code following SOLID principles.
-   Comprehensive `README.md` with setup and usage instructions.
