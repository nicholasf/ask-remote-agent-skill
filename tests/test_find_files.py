from tools.find_files import find_files


def test_find_files_matches_pattern(set_working_directory):
    tmp_path = set_working_directory
    (tmp_path / "alpha.py").write_text("")
    (tmp_path / "beta.py").write_text("")
    (tmp_path / "gamma.txt").write_text("")
    result = find_files.invoke({"pattern": "*.py"})
    assert "alpha.py" in result
    assert "beta.py" in result
    assert "gamma.txt" not in result
