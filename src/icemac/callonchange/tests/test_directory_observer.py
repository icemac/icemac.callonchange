# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt

import icemac.callonchange.testing
import os
import os.path
import time


class TestDirectoryObserver(icemac.callonchange.testing.ObserverTestBase):
    # Tests for the observation of all files in a directory.

    def callFUT(
        self, dir=None, script=None, quite=True, immediate=False, **kw):
        # Call the function under test
        observer = self.createObserver(
            dir=dir, script=script, quite=quite, immediate=immediate, **kw)
        try:
            try:
                observer.start()
                if not immediate:
                    os.mkdir(os.path.join(self.basedir, '1'))
                time.sleep(1)
            except KeyboardInterrupt:
                # When an OSError occurres during script call a
                # KeyboardInterrupt is raised to stop the whole
                # process. But this is the test which should not get
                # stopped.
                pass
        finally:
            observer.stop()

    def test_observer_called_on_changed_dir(self):
        # Assert that the script is called when something inside the
        # observed directory changes.
        self.callFUT()
        self.assertScriptCalled()

    def test_observer_called_on_changed_dir_not_quite(self):
        # Assert that the script is called when something inside the
        # observed directory changes. When the quite option is not
        # set, information about the called script is printed on
        # stdout.
        stdout, ignored = icemac.callonchange.testing.grapStdout(
            self.callFUT, quite=False)
        self.assertScriptCalled()
        self.assert_(stdout.startswith('Calling: '))
        self.assert_(stdout.endswith('script\n'))

    def test_observer_not_called_on_outside_change(self):
        # Assert that the script is _not_ called when something
        # outside the observed directory changes.
        observe_dir = os.path.join(self.basedir, 'observe')
        os.mkdir(observe_dir)
        self.callFUT(dir=observe_dir)
        self.assertScriptNotCalled()

    def test_not_existing_script(self):
        # When the script does not exist, an error message is
        # displayed.
        stdout, ignored = icemac.callonchange.testing.grapStdout(
            self.callFUT, script='not-existing-script.sh')
        self.assertEqual(
            "OSError: [Errno 2] No such file or directory\n"
            "Parameters were: not-existing-script.sh\n", stdout)

    def test_not_existing_script_not_quite(self):
        # When the script quite option is not set, the file called is
        # displayed, but it is not repeated in the error message.
        self.createObserver()
        stdout, ignored = icemac.callonchange.testing.grapStdout(
            self.callFUT, script='not-existing-script.sh', quite=False)
        self.assertEqual(
            "Calling: not-existing-script.sh\n"
            "OSError: [Errno 2] No such file or directory\n", stdout)

    def test_immediate(self):
        # When "immediate" is set the utility is called without a change.
        self.callFUT(immediate=True)
        self.assertScriptCalled()

    def test_immediate_not_quite(self):
        # When "immediate" is set, the "quite" flag is handled, too.
        stdout, ignored = icemac.callonchange.testing.grapStdout(
            self.callFUT, quite=False, immediate=True)
        self.assertScriptCalled()
        self.assert_(stdout.startswith('Calling: '))
        self.assert_(stdout.endswith('script\n'))

    def test_immediate_not_existing_script_not_quite(self):
        # When "immediate" is set and the script does not exists, the
        # "quite" flag is handled as usual.
        self.createObserver()
        stdout, ignored = icemac.callonchange.testing.grapStdout(
            self.callFUT, script='not-existing-script.sh', quite=False,
            immediate=True)
        self.assertEqual(
            "Calling: not-existing-script.sh\n"
            "OSError: [Errno 2] No such file or directory\n", stdout)
