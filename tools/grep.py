from langchain_core.tools import tool

from . import _context


@tool
def grep(pattern: str, path: str = ".") -> str:
    """
    Search for a pattern in files, excluding node_modules.
    Example: grep("runUseCase", "backend/saga/src")
    """
    return _context.run_command(
        f'grep -r --exclude-dir=node_modules -n "{pattern}" {path}'
    )
