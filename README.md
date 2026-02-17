# Branchwise

>❗ © 2026 Or Zionpour. All rights reserved.<br>
This code may not be copied, modified, distributed, or used
for any purpose without explicit written permission from the author.
Commercial use is strictly prohibited.


Branchwise is an intelligent code review agent that analyzes pull requests, detects potential issues, and suggests improvements before they reach your main branch. It helps teams maintain clean, consistent, and high-quality code - automatically and at scale.

## Features

- **Multi-Platform Support**: Seamlessly analyzes Pull Requests (GitHub, Bitbucket) and Merge Requests (GitLab).
- **Automated Code Analysis**: Fetches PR/MR details and diffs automatically.
- **AI-Powered Review**: Uses OpenAI's GPT models or local LLMs (Ollama) to analyze code changes for bugs, security issues, performance bottlenecks, and style violations.
- **Actionable Feedback**: Provides a summary report and detailed comments.
- **CLI Interface**: Easy-to-use command line interface.
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
    Create a `.env` file in the root directory (use `.env.example` as a template).

    **GitHub**:
    ```env
    BRANCHWISE_GITHUB_TOKEN=your_github_token
    ```

    **GitLab**:
    ```env
    BRANCHWISE_GITLAB_TOKEN=your_gitlab_token
    # Optional: Self-hosted GitLab URL
    # BRANCHWISE_GITLAB_URL=https://gitlab.example.com
    ```

    **Bitbucket**:
    ```env
    BRANCHWISE_BITBUCKET_TOKEN=your_bitbucket_token
    # Optional: Self-hosted Bitbucket URL
    # BRANCHWISE_BITBUCKET_URL=https://bitbucket.example.com
    ```

    **LLM Settings**:
    ```env
    BRANCHWISE_LLM_API_KEY=your_openai_api_key
    ```

## Usage

### Run a Review

Branchwise automatically detects the platform based on the URL provided.

**GitHub**:
```bash
branchwise https://github.com/owner/repo/pull/123
```

**GitLab**:
```bash
branchwise https://gitlab.com/owner/repo/-/merge_requests/456
```

**Bitbucket**:
```bash
branchwise https://bitbucket.org/owner/repo/pull-requests/789
```

**Options:**
- `--dry-run`: Analyze the PR and print results to the console without posting comments to the provider.
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

----

>❗ © 2026 Or Zionpour. All rights reserved.<br>
This code may not be copied, modified, distributed, or used
for any purpose without explicit written permission from the author.
Commercial use is strictly prohibited.
