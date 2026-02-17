# Branchwise

Branchwise is an intelligent code review agent that analyzes pull requests, detects potential issues, and suggests improvements before they reach your main branch. It helps teams maintain clean, consistent, and high-quality code - automatically and at scale.

## Features

- **Automated PR Analysis**: Fetches PR details and diffs from GitHub.
- **AI-Powered Review**: Uses OpenAI's GPT models to analyze code changes for bugs, security issues, performance bottlenecks, and style violations.
- **Actionable Feedback**: Provides a summary report and detailed comments.
- **CLI Interface**: easy-to-use command line interface.
- **Configurable**: Customize rules, ignored files, and LLM settings via config file or environment variables.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/orzionpour/Branchwise.git
    cd Branchwise
    ```

2.  **Install the package**:
    ```bash
    pip install .
    # Or for development:
    pip install -e .[dev]
    ```

3.  **Set up configuration**:
    Create a `.env` file in the root directory (use `.env.example` as a template):
    ```env
    BRANCHWISE_GITHUB_TOKEN=your_github_token
    BRANCHWISE_LLM_API_KEY=your_openai_api_key
    ```

## Usage

### Run a Review

To review a specific pull request:

```bash
branchwise review https://github.com/owner/repo/pull/123
```

**Options:**
- `--dry-run`: Analyze the PR and print results to the console without posting comments to GitHub.
- `--verbose`: Enable verbose logging for debugging.

### Using with Ollama (Local LLM)

Branchwise supports local LLMs via Ollama. Update your `.env` or environment variables:

```bash
BRANCHWISE_LLM_BASE_URL=http://localhost:11434/v1
BRANCHWISE_LLM_API_KEY=ollama  # Required but ignored by Ollama
BRANCHWISE_LLM_MODEL=llama3    # Or any model you have pulled in Ollama
```

### Configuration

You can configure Branchwise using environment variables or by modifying `branchwise/config.py`.

Key settings:
- `BRANCHWISE_RULES__MAX_COMMENTS`: Maximum number of comments to post (default: 10).
- `BRANCHWISE_RULES__IGNORE_FILES`: Comma-separated list of file extensions to ignore (e.g. `.lock,.png`).

## Development

To run tests:
```bash
python -m pytest
```

## License

MIT
