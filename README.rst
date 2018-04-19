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

ModuleRenamer is a tool to facilitate the update of imports from a project in bulk, using a single file as input.

Motivation
--------

Let's says that you have a core library used across different projects.

When a module from this library is renamed/moved, all references to this module needs to be manually updated.

With ModuleRenamer, you can update these reference on the whole project using a single file, which can have multiple entries. 

On this files, each entry needs to have the ``old path`` from the module and the ``new path`` of the module.

So, in the following example all references to ``vegetable.tomato`` will be updated to ``fruits.tomato``

.. code-block:: bash 

    imports_to_move = [('vegetable.tomato', 'fruits.tomato')]


Let's look the tool in action







Features
--------

* TODO


License
-------
* Free software: MIT license

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
