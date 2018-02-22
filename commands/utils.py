import ast
import fnmatch
import os
import timeit
from collections import namedtuple
from contextlib import contextmanager


@contextmanager
def time_it(msg):
    start_time = timeit.default_timer()
    yield
    print("Took: ", timeit.default_timer() - start_time, " ", msg)

def walkdir(folder):
    """Walk through each files in a directory"""
    for dirpath, dirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, '*.py'):
            yield os.path.abspath(os.path.join(dirpath, filename))


Import = namedtuple("Import", ["module", "name"])


def get_imports(project_path):
    # type: (str) -> Import
    """
    Look for all .py files on the given project path and return the import statements found on
    each file.

    :type project_path: str
    :rtype: commands.utils.Import
    """
    for file_path in walkdir(project_path):

        with open(file_path, mode='r') as file:
            file_content = ast.parse(file.read(), file_path)

        for node in ast.iter_child_nodes(file_content):
            if isinstance(node, ast.Import):
                module = ''
            elif isinstance(node, ast.ImportFrom):
                # node.module can be None on the following situation
                #   from . import foo
                if node.module is not None:
                    module = node.module
                else:
                    module = ''
            else:
                continue

            for n in node.names:
                yield Import(module, n.name)
