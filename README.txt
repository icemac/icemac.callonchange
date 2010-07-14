icemac.callonchange calls a specific command when a directory or
something in it has changed. It was developed to ease test driven
development (TDD): it can call the test case under development each
time the test case or the developed code changes.

.. contents::


Requirements
============

* Mac OS X 10.5+ (Leopard)
* Python 2.5

General usage
=============

Usage: callonchange [options] path utility [utility arguments]

coc invokes *utility* with its *utility arguments* when *path* or
something in it changes.

Options:
  -h, --help    show this help message and exit
  -e EXTENSION  only call utility on changes of a file with this extension
                (option might be used multiple times)

EXTENSION might be specified with or without leading dot:

  ``-e .py`` is equal to ``-e py``

**Caution:** optional arguments must be specified *before* the
positional arguments (path and utility). Arguments specified after the
positional arguments are taken as arguments of the utility.


Usage as script
===============

Installation
------------

To install callonchange as script call::

  $ python setup.py install

or install it using a package manager like easy_install or pip.

Call as script
--------------

To call it as a script add the path to the directory to be observed
and the command (script or program) to be called when the directory or
something in it has changed.

Example to call ``xeyes`` when a file with the extension `log` has
changed in `/var/log` enter::

  $ callonchange -e log /var/log xeyes

**Caution:** In this example `xeyes` is called on every new entry in
the log file.


In buildout
===========

There is a recipe in the package which eases installation using
buildout.

Installation with default arguments
-----------------------------------

Add a section to your buildout to generate a script for callonchange
(don't forget to add it to the parts!)::

  [coc]
  recipe = icemac.callonchange

This creates a callonchange script with default arguments. These are::

  '-e', 'py', '-e', 'zcml', '-e', 'pt', '-e', 'txt', 'src', 'bin/test', '-cv'

Which means: observe in the `src` directory files with the extensions
py, zcml, pt and txt. Call ``bin/test`` with the arguments cv (verbose
and color) on changes.

Installation with customized arguments
--------------------------------------

To override the default arguments add an `arguments` parameter to the
buildout section::

  [coc]
  recipe = icemac.callonchange
  name = coc
  arguments = 'Products', 'bin/ztest'

This means: The created script will be named `coc`. When called it
will observe the `Products` directory and call ``bin/ztest`` on
changes.


Usage as buildout script
------------------------

You can add additional parameters when you call the generated script::

  $ bin/callonchange -t testObserver

When you use the default arguments in the buildout section, this
command line calls ``bin/test -cv -t testObserver`` on each change of
py, zcml, pt or txt files in the `src` directory.

Stopping callonchange
=====================

To stop a running callonchange instance hit ^C (Control-C).


Runing the tests
================

To run the tests of icemac.callonchange call::

  $ python setup.py test

or use buildout::

  $ python bootstrap.py
  $ bin/buildout
  $ bin/test

or use callonchange itself::

  $ python bootstrap.py
  $ bin/buildout
  $ bin/callonchange

In the last version you have to change something inside the `src`
directory of the package so the observer lets the tests run.


Thanks
======

Thanks to Malte Borch for the great MacFSEvents_ which
icemac.callonchange is based on.

.. _MacFSEvents: http://pypi.python.org/pypi/MacFSEvents

Similar tools
=============

* pest_: "Auto tester for python" Seems to be designed to run tests
  and nothing else. Has growl integration. Current version (1.0.2) has
  no automatic tests.

* sniffer_: "An automatic test runner. Supports nose out of the box."
  Supports Linux, Windows and Mac OS X. But in current version (0.1.1)
  Windows and Mac OS X are untested. Current version has no automatic
  tests.


.. _pest: http://pypi.python.org/pypi/pest
.. _sniffer: http://pypi.python.org/pypi/sniffer