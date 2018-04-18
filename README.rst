------
Module Renamer
------


.. image:: https://travis-ci.org/ESSS/module-renamer.svg?branch=master
    :target: https://travis-ci.org/ESSS/module-renamer

.. image:: https://ci.appveyor.com/api/projects/status/github/ESSS/module-renamer?branch=master
    :target: https://ci.appveyor.com/project/ESSS/module_renamer/?branch=master&svg=true

.. image:: https://img.shields.io/pypi/v/module_renamer.svg
    :target: https://pypi.python.org/pypi/module_renamer

.. image:: https://codecov.io/gh/ESSS/module-renamer/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ESSS/module-renamer

ModuleRenamer is a tool to facilitate the renaming of the imports of a project in a bulk, using a single file as input.

Motivation
--------
Let's says that you have a core library used across different projects.
When a python module from this library is renamed/moved, all projects that import this module needs to manually update these references.

With ModuleRenamer, you can update these reference on the whole project using a single file, that can have multiple entries. Each entry should have the "old path" from the module and the "new path" of the module.

.. code-block:: bash 

    imports_to_move = [('vegetable.tomato', 'fruits.tomato')]


Still confused? Let's look a example.


* Free software: MIT license


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
