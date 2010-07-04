icemac.callonchange calls a specific command when a directory or
something in it has changed. It was developed to ease test driven
development (TDD): it can call the test case under development each
time the test case or the developed code changes.

.. contents::


Requirements
============

* Mac OS X 10.5+ (Leopard)

Usage
=====

icemac.callonchange can be used as standalone script and in buildout.

Usage as script
---------------

Installation
~~~~~~~~~~~~

To install icemac.callonchange as script call::

  $ python setup.py install

or install it using a package manager like easy_install or pip.

Call as script
~~~~~~~~~~~~~~

To call it as a script add the path to the directory to be observed
and the command (script or program) to be called when the directory or
something in it has changed.

Example to call ``xeyes`` when something changed in the Downloads
directory enter::

  $ callonchange ~/Dowloads xeyes


In buildout
-----------

There is a recipe in the package which eases installation using
buildout.

Installation with default arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a section to your buildout to generate a script for
icemac.callonchange (don't forget to add it to the parts!)::

  [coc]
  recipe = icemac.callonchange

This creates a callonchange script with default arguments. These are::

  'src', 'bin/test', '-cv'

Which means: observe the `src` directory and call ``bin/test`` with the arguments verbose and color on changes.

Installation with customized arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To override the default arguments add an `arguments` parameter to the
buildout section::

  [coc]
  recipe = icemac.callonchange
  arguments = 'Products', 'bin/ztest'

This means: observe the `Products` directory and call ``bin/ztest`` on changes.


Usage as buildout script
~~~~~~~~~~~~~~~~~~~~~~~~

You can add additional parameters when you call the generated script::

  $ bin/callonchange -t testObserver

When you use the default arguments in the buildout section, this
command line calls ``bin/test -cv -t testObserver`` on each change in
the `src` directory.

Stopping icemac.callonchange
----------------------------

To stop a running icemac.callonchange instance hit ^C (Control-C).


Run tests
---------

To run the tests of icemac.callonchange call::

  $ python setup.py test

or use buildout::

  $ python bootstrap.py
  $ bin/buildout
  $ bin/test

or use icemac.callonchange itself::

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