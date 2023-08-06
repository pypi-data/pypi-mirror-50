project-system
==============

Create and open projects.
Use multiple workstations to work on projects.

.. image:: https://img.shields.io/github/stars/iandennismiller/project-system.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/project-system

.. image:: https://img.shields.io/pypi/v/project-system.svg
    :target: https://pypi.python.org/pypi/project-system

.. image:: https://readthedocs.org/projects/project-system/badge/?version=latest
    :target: http://project-system.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/iandennismiller/project-system.svg?branch=master
    :target: https://travis-ci.org/iandennismiller/project-system

**Project-System** simplifies the management of projects within a working space.
Each project consists of a folder and a python virtual environment.
The folder is initialized for git and it is designed to correspond to a remote git repository.

Quick Start
-----------

Create a new project.
This makes a new folder, git repo, and virtual environment for the project.

::

    project-new my-project

Start working on the project.
This step opens a code editor and new ``tmux`` window for the project.

::

    project-workon my-project

See `Usage <https://project-system.readthedocs.io/en/latest/usage.html>`_ for more.

Installation
------------

::

    pip install project-system

To get the most from project-system, use `tmux <https://github.com/tmux/tmux/wiki>`_.

::

    apt install tmux

Optionally, to install bash completion scripts:

::

    project-completion-init

Now the `project-workon` script supports auto-completion of projects by name.

Ensure ~/.bashrc contains the following:

::

    for bcfile in ${COMPLETION_PATH}/* ; do
        [ -f "\$bcfile" ] && . \$bcfile
    done

Online Resources
----------------

- `Documentation <https://project-system.readthedocs.io>`_
- `Source Code <https://github.com/iandennismiller/project-system>`_
