from __future__ import print_function

from multiprocessing import Pool, cpu_count

import click
import pasta
import six
from pasta.augment import rename
from tqdm import tqdm

from commands.utils import total_of_py_files_on_project, walk_on_py_files


def execute_rename(file_path, moved_imports):
    if six.PY2:
        import imp
        import_from_user = imp.load_source('moved_imports', moved_imports)
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location("moved_imports", moved_imports)
        import_from_user = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(import_from_user)

    with open(file_path, mode='r') as file:
        tree = pasta.parse(file.read())
        for class_to_move in import_from_user.imports_to_move:
            old_path = class_to_move[0]
            new_path = class_to_move[1]
            try:
                rename.rename_external(tree, old_path, new_path)
            except ValueError:
                click.ClickException("Some error happened on the following path: {0}.\n "
                                     "While trying to rename from: {1} to {2}"
                                     .format(file_path, old_path, new_path))
        source_code = pasta.dump(tree)

    with open(file_path, mode='w') as file:
        file.write(source_code)


def start_execution(project_path, moved_imports):
    file_counter = total_of_py_files_on_project(project_path)


    pool = Pool(cpu_count())
    progress_bar = tqdm(total=file_counter, unit="files", leave=False)

    def update(*a):
        progress_bar.update()

    results = []
    for python_file in walk_on_py_files(project_path):
        results.append(pool.apply_async(execute_rename, args=(python_file, moved_imports),
                                        callback=update))

        pool.close()
        pool.join()
        progress_bar.close()

    for r in results:
        try:
            r.get()
        except Exception as error:
            click.ClickException(error)


def run_rename(**kwargs):
    moved_imports = kwargs['moved_imports_file']
    for input_path in kwargs['project_path']:
        print(input_path)
        start_execution(input_path, moved_imports)
