# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt

import icemac.callonchange.testing
import os
import os.path
import time


class TestFileObserver(icemac.callonchange.testing.ObserverTestBase):
    # Tests for the observation of specific files in a directory.

    def writeFile(self, path, mode='w'):
        my_file = file(path, mode)
        # my_file.flush and os.fsync are not enough (at least on my
        # MacBook Pro), so I write really big files hopefully beyond
        # the cache size.
        my_file.write(10000000 * 'asdf')
        my_file.flush()
        os.fsync(my_file.fileno())
        my_file.close()

    def callFUT(self, filename, filemode='w', dir=None, script=None,
                quite=True, immediate=False, **kw):
        # Call the function under test.
        # filename ... name of the file which is to be created.
        # filemode ... mode of the created file, defaults to 'w'
        # dir ... directory which is to be observed, defaults to self.basedir
        # script ... name of teh script to be called, defaults to creation of
        #            default script
        # quite ... set quite option on observer
        # **kw ... additional options for observer
        observer = self.createObserver(
            dir=dir, script=script, quite=quite, immediate=immediate, **kw)
        try:
            try:
                observer.start()
                # Wait a bit so the observer can set up its observation
                # routine:
                time.sleep(1)
                if not immediate:
                    self.writeFile(os.path.join(self.basedir, filename),
                                   mode=filemode)
            except KeyboardInterrupt:
                # Do not care about KeyboardInterrupt here as it is raised
                # when the script cannot be found.
                pass
        finally:
            observer.stop()

    def test_not_existing_script(self):
        # When the script does not exist, an error message is
        # displayed.
        stdout, ignored = icemac.callonchange.testing.grapStdout(
            self.callFUT, 'one.py', script='file-not-existing-script.sh',
            extensions=['.py'])
        self.assertEqual(
            "OSError: [Errno 2] No such file or directory\n"
            "Parameters were: file-not-existing-script.sh\n", stdout)

    def test_not_existing_script_not_quite(self):
        # When the script does not exist and the quite option is not
        # set, the called script name and an error message are
        # displayed.
        stdout, ignored = icemac.callonchange.testing.grapStdout(
            self.callFUT, 'one.py', script='file-not-existing-script.sh',
            quite=False, extensions=['.py'])
        self.assertEqual(
            "Calling: file-not-existing-script.sh\n"
            "OSError: [Errno 2] No such file or directory\n", stdout)

    def test_not_matching_extension(self):
        # When the extension of the changed file inside the observed
        # directory is not in the extenion list, script is not called
        self.callFUT('one.pyc', extensions=['.py'])
        self.assertScriptNotCalled()

    def test_matching_extension_create(self):
        # The script is called when the extension of the created file
        # is inside the observed directory and the file's extension is
        # in the extension list.
        self.callFUT('one.py', extensions=['.py'])
        self.assertScriptCalled()

    def test_matching_extension_modify(self):
        # The script is also called when the extension of the changed
        # file inside the observed directory is in the extenion list.
        # Create a file which gets modified when under observation.
        path = os.path.join(self.basedir, 'one.py')
        self.writeFile(path)
        self.callFUT('one.py', filemode='w+a', extensions=['.py'])
        self.assertScriptCalled()

    def test_matching_extension_not_quite(self):
        # When the quite option is not set, a message about the called
        # script is displayed.
        stdout, result = icemac.callonchange.testing.grapStdout(
            self.callFUT, 'one.py', quite=False, extensions=['.py'])
        self.assertScriptCalled()
        self.assert_(stdout.startswith('Calling: '))
        self.assert_(stdout.endswith('script\n'))

    def test_matching_extension_but_outside_observed_dir(self):
        # When a file outside the observed dir changes the script does
        # not get called.
        observe_dir = os.path.join(self.basedir, 'observe')
        os.mkdir(observe_dir)
        self.callFUT('one.py', dir=observe_dir, extensions=['.py'])
        self.assertScriptNotCalled()

    def test_immediate(self):
        # When "immediate" is set the utility is called without a change.
        self.callFUT('one.py', extensions=['.py'], immediate=True)
        self.assertScriptCalled()
