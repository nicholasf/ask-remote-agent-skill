import subprocess

from tools.git_diff import git_diff


def test_git_diff_non_repo_returns_string(set_working_directory):
    result = git_diff.invoke({})
    assert isinstance(result, str)


def test_git_diff_staged_file_appears_in_output(set_working_directory):
    tmp_path = set_working_directory
    subprocess.run("git init", shell=True, cwd=tmp_path, capture_output=True)
    subprocess.run("git commit --allow-empty -m init", shell=True, cwd=tmp_path, capture_output=True)
    (tmp_path / "new_feature.py").write_text("x = 1\n")
    subprocess.run("git add new_feature.py", shell=True, cwd=tmp_path, capture_output=True)
    result = git_diff.invoke({})
    assert "new_feature.py" in result
