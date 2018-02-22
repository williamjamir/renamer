import ast
from collections import namedtuple

import os
from contextlib import contextmanager
from email import contentmanager

from git import Repo

from commands.utils import walkdir

Import = namedtuple("Import", ["module", "name", "alias"])


def get_imports(project_path):
    for filepath in walkdir(project_path):

        with open(filepath, mode='r') as fh:
            root = ast.parse(fh.read(), filepath)

        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):
                module = node.module
            else:
                continue

            for n in node.names:
                yield Import(module, n.name, n.asname)


@contextmanager
def branch_checkout(repo, branch_name):
    if (repo.is_dirty() or len(repo.untracked_files) != 0):
        raise RuntimeError("The repository is dirty, please clean it first ")
    getattr(repo.heads, branch_name).checkout()
    yield


def track_modifications(**kwargs):
    project_path = os.path.join(kwargs['project_path'])
    repo = Repo(project_path)

    branch_origin = kwargs['origin']

    if kwargs['destination']:
        destination_branch = kwargs['destination']
    else:
        destination_branch = repo.active_branch.name

    if branch_origin == destination_branch:
        raise RuntimeError(
            "Please, check your activate branch. Use the option --origin and --destination if you do not want to change you current branch")

    with branch_checkout(repo, branch_origin):
        origin_branch_import_list = set()
        for imp in get_imports(project_path):
            origin_branch_import_list.add(imp)

    with branch_checkout(repo, destination_branch):
        destination_branch_import_list = set()
        for imp in get_imports(project_path):
            destination_branch_import_list.add(imp)

    print(origin_branch_import_list)
    print(destination_branch_import_list)

    list_with_imports_modify = set()
    for original in origin_branch_import_list:
        for modification in destination_branch_import_list:
            if original.name == modification.name:
                if original.module != modification.module:
                    list_with_imports_modify.add((original.module + "." + original.name,
                                                  modification.module + "." + modification.name))

    print(list_with_imports_modify)
