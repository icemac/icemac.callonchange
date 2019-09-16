Hacking
=======

Source code
-----------

Get the source code::

   $ git clone https://github.com/icemac/icemac.callonchange

or fork me on: https://github.com/icemac/icemac.callonchange

Running Tests
-------------

.. image:: https://travis-ci.com/icemac/icemac.callonchange.svg?branch=master
    :target: https://travis-ci.com/icemac/icemac.callonchange

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

In the last variant you have to change something inside the `src`
directory of the package so the observer lets the tests run.
