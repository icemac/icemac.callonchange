Requirements
============

* Mac OS X 10.5+ (Leopard)
* Python 2.7

General usage
=============

Usage: callonchange [options] path utility [utility arguments]

callonchange invokes *utility* with its *utility arguments* when
*path* or something in it changes.

Options:
  --version     show program's version number and exit
  -h, --help    show this help message and exit
  -e EXTENSION  only call utility on changes of a file with this extension
                (option might be used multiple times)
  -i            Run utility immediately after callonchange has been started.
                (By default the utility is only run when something changed.)
  -q            Do not display any output of callonchange. (Still displays the
                output of the utility.)


*EXTENSION* might be specified with or without a leading dot:

  ``-e .py`` is equal to ``-e py`` is equal to ``-epy``

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

  '-i', '-e', 'py', '-e', 'zcml', '-e', 'pt', '-e', 'txt', 'src', 'bin/test', '-cv'

Which means: observe in the `src` directory files with the extensions
py, zcml, pt and txt. Call ``bin/test`` with the arguments ``cv`` (verbose
and color) when callonchange has been invoked and later on when something
has changed.

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

Thanks
======

Thanks to Malte Borch for the great MacFSEvents_ which
icemac.callonchange is based on.

.. _MacFSEvents: http://pypi.python.org/pypi/MacFSEvents

Similar tools
=============

(Sorted by the time I got to know them.)

* pest_: "Auto tester for python" Seems to be designed to run tests
  and nothing else. Has growl integration. Current version (1.0.3) has
  no automatic tests.

* sniffer_: "An automatic test runner. Supports nose out of the box."
  Supports Linux, Windows and Mac OS X. Current version (0.2.2) has no
  automatic tests.

* autonose_: "continuous test tracker / runner for nosetests" Seems to
  focus on nose tests. Version 0.2 only acts on changes of python
  files.

* PyZen_: "Continuous testing for paranoid developers." Seems to be tightly
  integrated into python's `unittest` framework and Django. Detects file
  changes using comparison of file modification time stamps. So it is slow
  on larger code bases. Version 0.1 has no automatic tests.

* Flask-Zen_: "Flask-Script commands to integrate with PyZen." Light layer
  around PyZen to integrate it into Flask. Version 0.1 has no automatic
  tests.

* nosier_: "Monitors paths and upon detecting changes runs the specified
  command" It is however limited to Linux 2.6 since it depends on the
  inotify facility. Uses black lists and white lists for files thos changes
  sould be tracked and has some other nice features. Version 1.1 has no
  automatic tests.

* supcut_: "Simple unobtrusive Python continuous unit testing" It is limited
  to Linux as it depends on inotify. Expects some of its template files are
  installed in `/usr/share/doc/python-supcut/examples`. Although it always
  talks about running nose tests, it might be used for arbitrary calls,
  too. Can send e-mails about test run. Version 0.5.1 has no automatic
  tests.

* rerun_: "Command-line executable Python script to re-run the given command
  every time files are modified in the current directory or its
  subdirectories." Runs OS independent but polls the change times of
  files. Version 1.0.16 has no automatic tests.


.. _pest: http://pypi.python.org/pypi/pest
.. _sniffer: http://pypi.python.org/pypi/sniffer
.. _autonose: http://pypi.python.org/pypi/autonose
.. _PyZen: http://pypi.python.org/pypi/PyZen
.. _Flask-Zen: http://pypi.python.org/pypi/Flask-Zen
.. _nosier: http://pypi.python.org/pypi/nosier
.. _supcut: http://pypi.python.org/pypi/supcut
.. _rerun: http://pypi.python.org/pypi/rerun
