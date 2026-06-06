from tools.read_file import read_file


def test_read_file_existing_file(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "test.txt").write_text("Hello, World!")
    assert read_file.invoke({"path": "test.txt"}) == "Hello, World!"


def test_read_file_missing_file(set_working_directory):
    result = read_file.invoke({"path": "nonexistent.txt"})
    assert result.startswith("Error reading")
