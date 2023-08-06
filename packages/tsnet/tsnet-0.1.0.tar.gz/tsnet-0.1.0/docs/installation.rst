.. highlight:: shell

============
Installation
============

Setup Python Environment
------------------------------

TSNet is tested against Python versions 2.7, 3.5 and 3.6.
It can be installed on Windows, Linux, and Mac OS X operating systems.
Python distributions, such as Anaconda, are recommended to manage the Python
environment as they already contain (or easily support installation of) many
Python packages (e.g. SciPy, NumPy, pandas, pip, matplotlib, etc.) that are
used in the TSNet package.  For more information on Python package
dependencies, see :ref:`Dependencies`.

Two examples of those distributions are:

  1. http://conda.pydata.org/miniconda.html Conda is an open source package
  management system and environment management system for installing multiple
  versions of software  packages and their dependencies and switching easily
  between them.

  2. https://winpython.github.io/ WinPython comes along with a lot of Python
  packages (e.g. SciPy, NumPy, pip, matplotlib, etc.)..


Stable Release (for users)
--------------------------

To install TSNet, run this command in your terminal:

.. code-block:: console

    $ pip install tsnet

This is the preferred method to install tsnet, as it will always install the
most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From Sources (for developers)
-----------------------------

The sources for TSNet can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/glorialulu/tsnet

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/glorialulu/tsnet/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/glorialulu/tsnet
.. _tarball: https://github.com/glorialulu/tsnet/tarball/master


Dependencies
------------

In addition to the packages included in Anaconda and WinPython,
TSNet requires several other Python packages:

1. wntr: Water Network Tool for Resilience
  install on a python-enabled command line with `pip install wntr`

2. networkx: Network creation and manipulation engine
  install on a python-enabled command line with `pip install networkx`

3. pytest: Unit Tests engine
  install on a python-enabled command line with `pip install -U pytest`
