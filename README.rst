``h5bp_jinja``
==============

.. image:: https://travis-ci.org/malept/h5bp-template.png?branch=master
   :alt: Travis CI status, see https://travis-ci.org/malept/h5bp-template

A small script that converts an `HTML5 Boilerplate`_ template into a `Jinja2`_
template. It is also available as a Python module, for integration into
Python-based build systems.

.. _HTML5 Boilerplate: http://html5boilerplate.com/
.. _Jinja2: http://jinja.pocoo.org/


Installation
------------

``h5bp_jinja`` should run on Python 2.6, 2.7, and 3.3, and also on PyPy. It
has not been tested on Jython 2.7, but I don't see any reason why it wouldn't
run there.

In Python 2.6, this script requires ``argparse`` to be installed (it is part
of the standard library in later versions).

The `argcomplete`_ (shell completion) module is optional.

To install the script, run::

    pip install git+git://github.com/malept/h5bp-jinja#egg=h5bp_jinja

.. _argcomplete: https://github.com/kislyuk/argcomplete

Command-line Usage
------------------

For usage instructions, consult ``h5bp-jinja --help``. If you are so inclined
(and your flavor of Python supports it), you can also run the script by
invoking the module, e.g., ``python -m h5bp_jinja --help``.
