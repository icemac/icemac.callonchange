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


In Buildout
-----------

Installation
~~~~~~~~~~~~

Add a section to your buildout to generate a script for
icemac.callonchange (don't forget to add it to the parts!)::

  [coc]
  recipe = zc.recipe.egg
  eggs = icemac.callonchange
  arguments = "src", "bin/test"

This creates a callonchange script for the src directory which calls
``bin/test`` on each change in src or a subdirectory.

Usage as buildout script
~~~~~~~~~~~~~~~~~~~~~~~~

You can add additional parameters when you call the generated script::

  $ bin/callonchange -t testObserver

This command line calls ``bin/test -t testObserver`` on each change in
the src directory.

Run tests
---------

To run the tests of icemac.callonchange call::

  $ python setup.py test

or use buildout::

  $ python bootstrap.py
  $ bin/buildout
  $ bin/test


Thanks
======

Thanks to Malte Borch for the great MacFSEvents_ which
icemac.callonchange is based on.


.. _MacFSEvents: http://pypi.python.org/pypi/MacFSEvents