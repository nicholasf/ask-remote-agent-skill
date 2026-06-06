from tools.bash import bash


def test_bash_simple_command(set_working_directory):
    result = bash.invoke({"command": "echo hello"})
    assert result == "hello"


def test_bash_failing_command_includes_stderr(set_working_directory):
    result = bash.invoke({"command": "ls nonexistent_directory_xyz"})
    assert "STDERR" in result
