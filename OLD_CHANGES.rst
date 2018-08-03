Older Changelog
===============

*Newer changes see CHANGES.rst.*

0.5 (2010-07-21)
----------------

- Added `--version` option to callonchange.

- Added another similar tool to the list.


0.4 (2010-07-16)
----------------

- When the utility gets called a messge is displayed. This can be
  omitted by specifying the `-q` option for callonchange.

- When the utility is not found or another OSError occurred when
  calling the utility callonchange is now stopped.


0.3.2 (2010-07-14)
------------------

- Added list of similar tools.


0.3.1 (2010-07-10)
------------------

- Fixed incorrect handling of the `find-links` buildout parameter.


0.3 (2010-07-07)
----------------

- Added abbility to specify file extensions so only files with these
  extensions will be observed.

- Added a `name` parameter to the recipe to control the name of the
  generated script, e. g. allowing more than one icemac.callonchange
  script in a buildout.


0.2 (2010-07-04)
----------------

- Added buildout recipe to ease integration with buildout
  projects. (See section `In buildout`_.)


0.1 (2010-07-02)
----------------

- Initial release.
