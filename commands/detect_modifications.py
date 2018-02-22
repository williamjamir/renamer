import os
from contextlib import contextmanager

from click import ClickException
from git import Repo

from commands.utils import get_imports


@contextmanager
def branch_checkout(repo, branch_name):
    # type: (git.Repo, str) -> None
    """
    Change the current git branch for the branch informed on branch_name

    :param repo: A git.Repo object that represents the git repository from the project
    :type repo: git.Repo

    :param branch_name: Name of the branch that Git should move into
    :type branch_name: str
    """
    if (repo.is_dirty() or len(repo.untracked_files) != 0):
        raise ClickException("The repository is dirty, please clean it first ")

    getattr(repo.heads, branch_name).checkout()

    yield


def track_modifications(**kwargs):
    """
    Command to track all modifications made between two different branches. The output will be a
    list written directly to a file (which will later be used by the script to rename the imports)

    :param kwargs:
    """
    project_path = os.path.join(kwargs['project_path'])
    repo = Repo(project_path)

    origin_branch = kwargs["origin_branch"]

    if kwargs['work_branch']:
        work_branch = kwargs['work_branch']
    else:
        work_branch = repo.active_branch.name

    if origin_branch == work_branch:
        raise ClickException(
            "Origin and Working branch are the same. "
            "Please, change your activate branch to where you made you changes on the code, "
            "or use the option --origin_branch and --work_branch  ."
        )

    with branch_checkout(repo, origin_branch):
        origin_import_list = {imp for imp in get_imports(project_path)}

    with branch_checkout(repo, work_branch):
        working_import_list = {imp for imp in get_imports(project_path)}

    modified_imports = _generate_list_with_modified_imports(origin_import_list, working_import_list)
    print(type(kwargs['output_file']))
    _write_list_to_file(modified_imports, kwargs['output_file'])


def _write_list_to_file(list_with_modified_imports, file_name):
    # type: (set) -> None
    """
    Write the list of modified imports on a python file, the python file per default will be named
    "list_output.py" but can be changed by passing the argument --output_file

    The name of the list (inside the file) cannot be changed since it will be used later on the
    script for renaming the project.
    """
    with open(file_name, 'w') as fp:
        fp.write("list_of_classes_to_move =")
        fp.writelines(repr(list(list_with_modified_imports)))


def _generate_list_with_modified_imports(origin_import_list, working_import_list):
    # type: (set, set) -> set
    """
    This methods looks for imports that keep the name but has has different modules path

    :return: A list with unique elements that has the same name but different modules path
    :rtype: set
    """
    return {
        (origin.module + "." + origin.name, working.module + "." + working.name)
        for origin in origin_import_list
        for working in working_import_list
        if working.name is not '*'
        if origin.name == working.name
        if origin.module != working.module
    }
