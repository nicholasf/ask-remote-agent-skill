from tools.write_file import write_file


def test_write_file_creates_file(set_working_directory):
    tmp_path = set_working_directory
    result = write_file.invoke({"path": "test.txt", "content": "Hello, World!"})
    assert "Written: " in result
    assert (tmp_path / "test.txt").read_text() == "Hello, World!"


def test_write_file_executable(set_working_directory):
    tmp_path = set_working_directory
    write_file.invoke({"path": "test.sh", "content": "#!/bin/bash\necho hello", "executable": True})
    file_path = tmp_path / "test.sh"
    assert file_path.read_text() == "#!/bin/bash\necho hello"
    assert (file_path.stat().st_mode & 0o111) != 0


def test_write_file_creates_parent_directories(set_working_directory):
    tmp_path = set_working_directory
    write_file.invoke({"path": "subdir/nested.txt", "content": "Nested content"})
    assert (tmp_path / "subdir" / "nested.txt").read_text() == "Nested content"
