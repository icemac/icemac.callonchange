Hacking
=======

Source code
-----------

Get the source code::

   $ hg clone https://bitbucket.org/icemac/icemac.callonchange

or fork me on: https://bitbucket.org/icemac/icemac.callonchange

Running Tests
-------------

(Currently not running successfully on Travis-CI until Mac OS X gets
supported there.)

.. image:: https://secure.travis-ci.org/icemac/icemac.callonchange.png
   :target: https://travis-ci.org/icemac/icemac.callonchange

To run the tests of `icemac.callonchange` call::

  $ python setup.py test

or use `zc.buildout`::

  $ python bootstrap.py
  $ bin/buildout
  $ bin/test

or use `callonchange` itself::

  $ python bootstrap.py
  $ bin/buildout
  $ bin/callonchange

In the last version you have to change something inside the `src`
directory of the package so the observer lets the tests run.
