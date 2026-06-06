from langchain_core.tools import tool

from . import _context


@tool
def bash(command: str) -> str:
    """
    Run a bash command in the project working directory.
    Always exclude node_modules from any recursive file operations.
    Do not run destructive commands (rm -rf, git reset --hard, etc.).
    """
    return _context.run_command(command)
