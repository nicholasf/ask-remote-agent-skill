from pathlib import Path

from langchain_core.tools import tool

from . import _context


@tool
def read_file(path: str) -> str:
    """Read the full contents of a file. Path may be absolute or relative to the working directory."""
    target = Path(path) if Path(path).is_absolute() else Path(_context.working_directory) / path
    try:
        return target.read_text()
    except Exception as e:
        return f"Error reading {path}: {e}"
