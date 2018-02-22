import fnmatch
import timeit
from contextlib import contextmanager

import os


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
