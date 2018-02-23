import ast
import fnmatch
import os
import timeit
from collections import namedtuple
from contextlib import contextmanager

from tqdm import tqdm


@contextmanager
def time_it(msg):
    start_time = timeit.default_timer()
    yield
    print("Took: ", timeit.default_timer() - start_time, " ", msg)


def walk_on_py_files(folder):
    """
    Walk through each python files in a directory
    """
    for dir_path, _, files in os.walk(folder):
        for filename in fnmatch.filter(files, '*.py'):
            yield os.path.abspath(os.path.join(dir_path, filename))


Import = namedtuple("Import", ["module", "name"])


def get_imports(project_path, file_counter):
    # type: (str) -> Import
    """
    Look for all .py files on the given project path and return the import statements found on
    each file.

    Note.: I inserted the TQDM here because was the only way that I could have an accurate
    progress bar, you (the reader obviously) are more than welcome to share any thoughts or tips on
    how to improve this approach =)

    :type project_path: str
    :rtype: commands.utils.Import
    """
    with tqdm(total=file_counter, unit='files', leave=True, desc=project_path) as pbar:
        for file_path in walk_on_py_files(project_path):
            pbar.update()
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
