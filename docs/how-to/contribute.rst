.. _contribute:

==============================
How to contribute to Colosseum
==============================

If you experience problems with Colosseum, `log them on GitHub`_. If you want
to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/pybee/colosseum/issues
.. _fork the code: https://github.com/pybee/colosseum
.. _submit a pull request: https://github.com/pybee/colosseum/pulls

Set up your development environment
===================================

The recommended way of setting up your development environment for Colosseum
is to install a virtual environment, install the required dependencies and
start coding::

    $ python3 -m venv venv
    $ source venv/bin/activate.sh
    $ git clone git@github.com:pybee/colosseum.git
    $ cd colosseum
    $ pip install -e .

In order to test the capabilities of Colosseum, the test suite contains
an Objective-C library with some known classes. To run the test suite,
you'll need to compile this library::

    $ make

This will produce `tests/objc/libcolosseumharness.dylib`.

In order for Colosseum to find this file, it will need to be on your
dynamic library path. You can set this by setting an environment
variable::

    $ export DYLD_LIBRARY_PATH=$(pwd)/tests/objc

You can then run the test suite::

    $ python setup.py test

Now you are ready to start hacking on Colosseum. Have fun!
