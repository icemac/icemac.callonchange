# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt

"""Test helpers."""

import StringIO
import icemac.callonchange.observer
import os
import os.path
import shutil
import sys
import tempfile
import unittest


def grapStdout(callable, *args, **kw):
    """Grab the standard output and return it together with the result."""
    orig_stdout = sys.stdout
    sys.stdout = StringIO.StringIO()
    try:
        try:
            result = callable(*args, **kw)
        except SystemExit:
            # Handled internally
            result = ''
        #noinspection PyUnresolvedReferences
        return sys.stdout.getvalue(), result
    finally:
        sys.stdout = orig_stdout


class ObserverTestBase(unittest.TestCase):
    # Base class for directory an file observers

    def setUp(self):
        # Set up a place for the tests.
        self.tempdir = tempfile.mkdtemp()
        # Create the directory the observation normally takes place.
        self.basedir = os.path.join(self.tempdir, 'basedir')
        os.mkdir(self.basedir)

    def tearDown(self):
        # Remove all temporary test directories.
        shutil.rmtree(self.tempdir)

    def createScript(self):
        filename = os.path.join(self.tempdir, 'script')
        file = open(filename, 'w')
        file.write('#! /bin/bash\n')
        file.write('echo -n "script called" > "%s"\n' % os.path.join(
            self.tempdir, 'result'))
        file.flush()
        os.fsync(file.fileno())
        file.close()
        os.chmod(filename, 0o700)
        return filename

    def createObserver(self, dir=None, script=None, quite=True, **kw):
        # Create the observer which calls a predefined script.
        if dir is None:
            # By default observer the default directory.
            dir = self.basedir
        if script is None:
            # By default create an observation script.
            script = self.createScript()
        # Create the observer but make sure it does not exit on error
        # as this will exit the test runner, too.
        return icemac.callonchange.observer.Observer(
            dir, [script], quite=quite, **kw)

    def assertScriptCalled(self):
        """Assert that the script got called."""
        # Wait a bit as the events are processed in a different thread.
        self.assertEqual('script called',
                         open(os.path.join(self.tempdir, 'result')).read())

    def assertScriptNotCalled(self):
        """Assert that the script got not called."""
        # Wait a bit as so the event can get propagated.
        self.assertFalse(os.path.exists(os.path.join(self.tempdir, 'result')))
