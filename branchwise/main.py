import logging
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from branchwise.config import load_settings, Settings
from branchwise.core.analyzer import Analyzer
from branchwise.integrations.base import VCSClient
from branchwise.llm.client import OpenAIClient

# Configure logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

app = typer.Typer(help="Branchwise - Intelligent Code Review Agent")
console = Console()
logger = logging.getLogger("branchwise")


@app.command()
def review(
    pr_url: str = typer.Argument(..., help="URL of the pull request to review"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not post comments to GitHub"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """
    Review a pull request and provide intelligent feedback.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        # Load settings
        settings = load_settings()
        
        if not settings.llm.api_key:
            console.print("[bold red]Error:[/bold red] LLM API key not found. Please set BRANCHWISE_LLM_API_KEY.")
            raise typer.Exit(code=1)

        # Detect VCS provider and parse URL
        client: VCSClient
        repo_name: str
        pr_number: int
        
        # Simple heuristic for URL parsing
        if "github.com" in pr_url:
            from branchwise.integrations.github import GitHubClient
            
            if not settings.github.token:
                 console.print("[yellow]Warning: GitHub token not found. API limits may apply.[/yellow]")

            parts = pr_url.rstrip("/").split("/")
            try:
                # https://github.com/owner/repo/pull/123
                pr_number = int(parts[-1])
                repo_name = f"{parts[-4]}/{parts[-3]}"
                client = GitHubClient(settings)
            except (IndexError, ValueError) as e:
                console.print(f"[bold red]Error:[/bold red] Invalid GitHub URL format. {e}")
                raise typer.Exit(code=1)
                
        elif "gitlab.com" in pr_url or (settings.gitlab.url and settings.gitlab.url in pr_url):
            from branchwise.integrations.gitlab_client import GitLabClient
            
            if not settings.gitlab.token:
                console.print("[bold red]Error:[/bold red] GitLab token not found. Please set BRANCHWISE_GITLAB_TOKEN.")
                raise typer.Exit(code=1)

            # https://gitlab.com/owner/repo/-/merge_requests/123
            # or custom instance
            try:
                # This parsing is brittle and depends on URL structure
                # Assuming standard GitLab URL: .../project/path/-/merge_requests/ID
                if "/-/merge_requests/" in pr_url:
                    base, mr_part = pr_url.split("/-/merge_requests/")
                    repo_name = base.split("/")[-1] # This might be wrong for nested groups
                    # Better to take relative path from domain
                    
                    # Let's try to extract project namespace/name
                    # Remove protocol
                    path_only = pr_url.split("://")[-1].split("/", 1)[1]
                    project_path, _ = path_only.split("/-/merge_requests/")
                    repo_name = project_path
                    pr_number = int(mr_part.split("/")[0])
                else:
                    raise ValueError("URL does not look like a merge request URL")
                
                client = GitLabClient(settings)
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] Invalid GitLab URL format. {e}")
                raise typer.Exit(code=1)

        elif "bitbucket.org" in pr_url:
            from branchwise.integrations.bitbucket_client import BitbucketClient
            
            if not settings.bitbucket.token:
                 console.print("[bold red]Error:[/bold red] Bitbucket token not found.")
                 raise typer.Exit(code=1)
            
            # https://bitbucket.org/owner/repo/pull-requests/123
            try:
                parts = pr_url.rstrip("/").split("/")
                # owner/repo/pull-requests/123
                # parts[-1] is ID?
                # bitbucket URLs can be complex.
                # Assuming standard cloud URL
                pr_number = int(parts[-1])
                repo_name = f"{parts[-4]}/{parts[-3]}"
                client = BitbucketClient(settings)
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] Invalid Bitbucket URL format. {e}")
                raise typer.Exit(code=1)
        else:
             console.print("[bold red]Error:[/bold red] Unsupported URL. Only GitHub, GitLab, and Bitbucket are supported.")
             raise typer.Exit(code=1)

        console.print(f"[bold blue]Starting review for PR #{pr_number} in {repo_name}...[/bold blue]")

        # Initialize components
        llm_client = OpenAIClient(settings)
        analyzer = Analyzer(settings, llm_client)

        # Fetch PR details
        with console.status("[bold green]Fetching PR details...[/bold green]"):
            pr_details = client.get_pr_details(repo_name, pr_number)
            
        console.print(f"Found PR: [bold]{pr_details.title}[/bold] by {pr_details.author}")
        if hasattr(pr_details, 'files'): # Basic check
             console.print(f"Files changed: {len(pr_details.files)}")

        # Analyze PR
        with console.status("[bold green]Analyzing code changes...[/bold green]"):
            result = analyzer.analyze_pr(pr_details)

        # Output results
        console.print("\n[bold]Review Summary:[/bold]")
        console.print(result.summary)
        
        if result.comments:
            table = Table(title="Review Comments")
            table.add_column("File", style="cyan")
            table.add_column("Line", style="magenta")
            table.add_column("Type", style="yellow")
            table.add_column("Severity", style="red")
            table.add_column("Comment", style="white")
            
            for comment in result.comments:
                table.add_row(
                    comment.file_path,
                    str(comment.line_number),
                    comment.type,
                    comment.severity,
                    comment.content
                )
            
            console.print(table)
            
            # Post comments if not dry run
            if not dry_run:
                with console.status("[bold green]Posting comments to Provider...[/bold green]"):
                    summary_body = "### Branchwise Code Review\n\n" + result.summary
                    client.post_comment(repo_name, pr_number, summary_body)
                    
                    # Inline comments logic would go here if specialized per provider
                    
                    console.print("[bold green]Comments posted successfully![/bold green]")
            else:
                console.print("[yellow]Dry run mode: Comments were not posted.[/yellow]")
        else:
            console.print("[green]No issues found![/green]")

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")
        # if verbose:
        logger.exception(e)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
