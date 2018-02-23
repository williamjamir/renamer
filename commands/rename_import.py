from multiprocessing import Pool, cpu_count

import pasta
from pasta.augment import rename
from tqdm import tqdm

from commands.utils import time_it, walk_on_py_files
from list_of_import import list_of_classes_to_move


def execute_rename(filepath):
    with open(filepath, mode='r') as file:
        tree = pasta.parse(file.read())
        for class_to_move in list_of_classes_to_move:
            old_path = class_to_move[0]
            new_path = class_to_move[1]
            try:
                rename.rename_external(tree, old_path, new_path)
            except ValueError:
                print("Some error happened on the following path:" + filepath)
                print("While trying to rename from:" + old_path + " to: " + new_path)
        source_code = pasta.dump(tree)

    with open(filepath, mode='w') as file:
        file.write(source_code)


def start_execution(inputpath):
    filecounter = scan_total_of_files(inputpath)

    results = []
    print("Executing rename...")

    msg = "seconds to run the script"
    pool = Pool(cpu_count())
    pbar = tqdm(total=filecounter, unit="files")

    def update(*a):
        pbar.update()

    with time_it(msg):
        for python_file in walk_on_py_files(inputpath):
            results.append(pool.apply_async(execute_rename, args=(python_file,), callback=update))

        pool.close()
        pool.join()
        pbar.close()

    for r in results:
        try:
            r.get()
        except Exception as error:
            print("An exception has occurred...")
            print(error)


def scan_total_of_files(inputpath):
    filecounter = 0
    for filepath in walk_on_py_files(inputpath):
        filecounter += 1
    return filecounter


def execute_rename(paths):
    for input_path in paths:
        start_execution(input_path)
