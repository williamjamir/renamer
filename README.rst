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

ModuleRenamer is a script made to facilitate the renaming of the import from a project in bulk, using a file as input.

Let's says that you have a core library used across different projects.

When some modules are renamed/moved inside the core library, all projects that use this lib will have the imports broken until someone manually updates all the references.

With ModuleRenamer, you can rename a whole project in bulk since it uses as input a list of moved imports, that can be created manually or automatically created from the script (more details later on.)

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
