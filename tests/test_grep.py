from tools.grep import grep


def test_grep_finds_pattern(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "source.py").write_text("def hello_world():\n    pass\n")
    result = grep.invoke({"pattern": "hello_world"})
    assert "source.py" in result
    assert "hello_world" in result


def test_grep_missing_pattern_returns_no_output(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "source.py").write_text("def hello():\n    pass\n")
    result = grep.invoke({"pattern": "nonexistent_symbol_xyz"})
    assert result == "(no output)"
