from pathlib import Path

from langchain_core.tools import tool

from . import _context


@tool
def edit_file(path: str, old_string: str, new_string: str) -> str:
    """
    Replace an exact string in a file. Fails if old_string is not found or
    matches more than once (use a larger context window to make it unique).
    """
    target = Path(path) if Path(path).is_absolute() else Path(_context.working_directory) / path
    try:
        content = target.read_text()
    except Exception as e:
        return f"Error reading {path}: {e}"
    count = content.count(old_string)
    if count == 0:
        return f"Error: old_string not found in {path}"
    if count > 1:
        return f"Error: old_string matches {count} times in {path} — provide more context to make it unique"
    target.write_text(content.replace(old_string, new_string, 1))
    return f"Edited: {target}"
