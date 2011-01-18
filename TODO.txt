Ideas
=====

- It would be nice to have predefined argument lines (profiles) even
  when not using buildout. They could be stored in the home directory
  of the user. (Should support profiles which reverence other
  profiles.)

- In buildout recipe: default script name should be section name.

- A minimal time between calls (delay) might be nice, so a change does not
  result in a call of the utility when it occurred during the delay time.

- The options of callonchange should have long variants, too.

- White list/black list approach of nosier seems to be nice.

- When observing large trees for changes of files with a specific extension,
  starting up the script can take while as the whole tree has to to be
  scanned once. During this start up period changes are not yet handled, so
  a message would be nice when start up is done.

- http://pypi.python.org/pypi/watchdog could be a way to get callonchange
  running on Linux and Windows, too.