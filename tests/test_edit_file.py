from tools.edit_file import edit_file


def test_edit_file_replaces_unique_string(set_working_directory):
    tmp_path = set_working_directory
    target = tmp_path / "config.txt"
    target.write_text("colour = blue\nsize = large\n")
    result = edit_file.invoke({"path": "config.txt", "old_string": "colour = blue", "new_string": "colour = red"})
    assert "Edited" in result
    assert target.read_text() == "colour = red\nsize = large\n"


def test_edit_file_string_not_found(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "config.txt").write_text("colour = blue\n")
    result = edit_file.invoke({"path": "config.txt", "old_string": "colour = green", "new_string": "colour = red"})
    assert result.startswith("Error")
    assert "not found" in result


def test_edit_file_multiple_matches(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "config.txt").write_text("x = 1\nx = 1\n")
    result = edit_file.invoke({"path": "config.txt", "old_string": "x = 1", "new_string": "x = 2"})
    assert result.startswith("Error")
    assert "2" in result
