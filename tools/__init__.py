from .bash import bash
from .edit_file import edit_file
from .find_files import find_files
from .git_diff import git_diff
from .grep import grep
from .list_directory import list_directory
from .read_file import read_file
from .write_file import write_file

TOOLS = [read_file, bash, find_files, grep, write_file, edit_file, list_directory, git_diff]
TOOL_MAP = {t.name: t for t in TOOLS}
