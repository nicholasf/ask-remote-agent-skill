from langchain_core.tools import tool

from . import _context


@tool
def git_diff() -> str:
    """Show unstaged and staged changes in the working tree."""
    result = _context.run_command("git diff && git diff --cached")
    if len(result) > 6000:
        result = result[:6000] + "\n...[truncated]"
    return result or "(no changes)"
