from langchain_core.tools import tool

from . import _context


@tool
def list_directory(path: str = ".", max_depth: int = 3) -> str:
    """
    List directory tree, excluding node_modules, .git, __pycache__, .venv, dist.
    """
    return _context.run_command(
        f'find {path} -maxdepth {max_depth} '
        f'-not -path "*/node_modules/*" '
        f'-not -path "*/.git/*" '
        f'-not -path "*/__pycache__/*" '
        f'-not -path "*/.venv/*" '
        f'-not -path "*/dist/*" '
        f'| sort'
    )
