from __future__ import print_function, print_function

import os
from collections import Counter
from contextlib import contextmanager

from click import ClickException, confirm, echo
from git import Repo

from commands.utils import get_imports

CONFLICT_MSG = "\nUnfortunately, you moved two objects with the same name on " \
               "different paths.\nThis situation could be catastrophic while running " \
               "the script for rename the imports. \n" \
               "These are the imports that have conflict: \n -> {} \n"

INFORMATIVE_CONFLICT_MSG = 'Do you want to generate the file without this import? (otherwise the script ' \
                           'will be aborted'



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

    current_branch = repo.active_branch.name
    getattr(repo.heads, branch_name).checkout()

    try:
        yield
    finally:
        getattr(repo.heads, current_branch).checkout()


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

    modified_imports = generate_list_with_modified_imports(origin_import_list, working_import_list)
    write_list_to_file(modified_imports, kwargs['output_file'])


def write_list_to_file(list_with_modified_imports, file_name):
    # type: (set) -> None
    """
    Write the list of modified imports on a python file, the python file per default will be named
    "list_output.py" but can be changed by passing the argument --output_file

    The name of the list (inside the file) cannot be changed since it will be used later on the
    script for renaming the project.
    """
    echo('Generating the file {0}'.format(file_name))
    with open(file_name, 'w') as fp:
        fp.write("list_of_classes_to_move =")
        fp.writelines(repr(list(list_with_modified_imports)))


def generate_list_with_modified_imports(origin_import_list, working_import_list):
    # type: (set, set) -> set
    """
    This methods looks for imports that keep the same name but has has different modules path

    :return: A list with unique elements that has the same name but different modules path
    :rtype: set
    """

    origin_filtered, working_filtered = _filter_import(origin_import_list, working_import_list)

    moved_imports = _find_moved_imports(origin_filtered, working_filtered)

    list_with_modified_imports = _check_for_conflicts(moved_imports)

    return list_with_modified_imports


def _filter_import(origin_import_list, working_import_list):
    """
    Create a new set with elements present origin_list or working_list but not on both,
    this helps to filter classes that could have same name but different modules.
    """
    difference = origin_import_list.symmetric_difference(working_import_list)
    origin_filtered = origin_import_list.intersection(difference)
    working_filtered = working_import_list.intersection(difference)
    return origin_filtered, working_filtered


def _find_moved_imports(origin_filtered, working_filtered):
    list_with_modified_imports = {
        (origin.module + "." + origin.name, working.module + "." + working.name)
        for origin in origin_filtered
        for working in working_filtered
        if working.name is not '*'
        if origin.name == working.name
        if origin.module != working.module
    }
    return list_with_modified_imports


def _check_for_conflicts(list_with_modified_imports):
    import_from = [modified_import[0] for modified_import in list(list_with_modified_imports)]
    imports_with_conflict = [class_name
                             for class_name, number_of_occurrences in Counter(import_from).items()
                             if number_of_occurrences > 1]
    if len(imports_with_conflict) > 0:
        echo(CONFLICT_MSG.format('\n -> '.join(imports_with_conflict)))

        if confirm(INFORMATIVE_CONFLICT_MSG, abort=True):
            list_with_modified_imports = [modified_import for modified_import in
                                          list_with_modified_imports
                                          if modified_import[0] not in imports_with_conflict
                                          if modified_import[1] not in imports_with_conflict]
    return list_with_modified_imports
