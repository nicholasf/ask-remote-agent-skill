from tools.list_directory import list_directory


def test_list_directory_shows_nested_paths(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("")
    (tmp_path / "README.md").write_text("")
    result = list_directory.invoke({})
    assert "src" in result
    assert "main.py" in result
    assert "README.md" in result


def test_list_directory_excludes_node_modules(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "lodash.js").write_text("")
    (tmp_path / "index.js").write_text("")
    result = list_directory.invoke({})
    assert "lodash.js" not in result
    assert "index.js" in result
