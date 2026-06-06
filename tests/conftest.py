import pytest
from tools import _context


@pytest.fixture(autouse=False, scope="function")
def set_working_directory(tmp_path):
    """Set the working directory for tools to the temporary path."""
    original_cwd = _context.working_directory
    _context.working_directory = str(tmp_path)
    yield tmp_path
    _context.working_directory = original_cwd
