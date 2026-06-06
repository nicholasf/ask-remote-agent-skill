from pathlib import Path

from langchain_core.tools import tool

from . import _context


@tool
def write_file(path: str, content: str, executable: bool = False) -> str:
    """
    Write content to a file. Path may be absolute or relative to the working directory.
    Set executable=true for shell scripts.
    """
    target = Path(path) if Path(path).is_absolute() else Path(_context.working_directory) / path
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        if executable:
            target.chmod(target.stat().st_mode | 0o111)
        return f"Written: {target} ({len(content)} bytes)"
    except Exception as e:
        return f"Error writing {path}: {e}"
