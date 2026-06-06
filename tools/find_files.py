from langchain_core.tools import tool

from . import _context


@tool
def find_files(pattern: str, directory: str = ".") -> str:
    """
    Find files matching a name pattern, excluding node_modules.
    Example: find_files("*.ts", "backend/saga/src")
    """
    return _context.run_command(
        f'find {directory} -name "{pattern}" -not -path "*/node_modules/*" | sort'
    )
