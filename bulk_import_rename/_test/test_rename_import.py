import os

import pytest


@pytest.fixture
def run_cli_rename():
    def _run_cli_rename(dir, file):
        from click.testing import CliRunner
        runner = CliRunner()

        from bulk_import_rename.main import rename
        return runner.invoke(rename, [dir, file])

    return _run_cli_rename


def test_run_rename(tmpdir, run_cli_rename):
    # Create test case scenario
    file_content = ['from a.b import c\n', 'from d.e import f\n']

    os.makedirs(os.path.join(str(tmpdir), 'src'))

    file_path = os.path.join(str(tmpdir), 'src', 'file_a.py')
    with open(file_path, 'w+') as file:
        file.writelines(file_content)

    # Create the file with the list of imports to move
    file_imports_to_move = os.path.join(str(tmpdir), "list_output.py")
    with open(file_imports_to_move, 'w+') as file:
        file.writelines("imports_to_move = [('a.b.c', 'x.x.c')]")

    file_folder = os.path.join(str(tmpdir), 'src')
    result = run_cli_rename(file_folder, file_imports_to_move)

    print(result.output)
    assert result.exit_code == 0
    expected_file_content = "from x.x import c\nfrom d.e import f\n"
    with open(file_path, mode='r') as file:
        assert file.read() == expected_file_content
