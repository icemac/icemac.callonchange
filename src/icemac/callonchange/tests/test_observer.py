# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import StringIO
import icemac.callonchange.observer
import os
import os.path
import shutil
import sys
import tempfile
import time
import unittest

_marker = object()

def grap_stdout(callable, *args, **kw):
    orig_stdout = sys.stdout
    sys.stdout = StringIO.StringIO()
    try:
        result = callable(*args, **kw)
        return sys.stdout.getvalue(), result
    finally:
        sys.stdout = orig_stdout

def grap_stderr(callable, *args, **kw):
    orig_stderr = sys.stderr
    sys.stderr = StringIO.StringIO()
    try:
        result = callable(*args, **kw)
        return sys.stderr.getvalue(), result
    except Exception, e:
        output = sys.stderr.getvalue()
        output += str(e)
        orig_stderr.write(output)
        return output, _marker
    finally:
        sys.stderr = orig_stderr


class TestMangle(unittest.TestCase):

    def callFUT(self, arg, argv=[]):
        return grap_stdout(
            icemac.callonchange.observer.mangle_call_args, arg, argv)

    def test_no_args(self):
        # With no arguments supplied, usage is shown.
        stdout, result = self.callFUT([])
        self.assertEqual((None, None, None), result)
        self.failUnless(stdout.startswith('USAGE'))

    def test_missing_params(self):
        # With not enough arguments supplied, usage is shown.
        stdout, result = self.callFUT(['.'])
        self.assertEqual((None, None, None), result)
        self.failUnless(stdout.startswith('USAGE'))

    def test_only_extension(self):
        # With only extensions supplied, usage is shown.
        stdout, result = self.callFUT(['-e', 'py'])
        self.assertEqual((None, None, None), result)
        self.failUnless(stdout.startswith('USAGE'))

    def test_no_additional_args(self):
        # Without additional arguments the default arguments are used.
        stdout, result = self.callFUT(['.', 'bin/test'])
        self.assertEqual(('.', ['bin/test'], []), result)
        self.assertEqual(stdout, '')

    def test_additional_args(self):
        # With additional arguments these are added to the default ones.
        stdout, result = self.callFUT(
            ['.', 'bin/test'], ['-t', 'TestMangle'])
        self.assertEqual(('.', ['bin/test', '-t', 'TestMangle'], []), result)
        self.assertEqual(stdout, '')

    def test_only_additional_args(self):
        # With only additional arguments supplied, they are used
        # instead of the default ones.
        stdout, result = self.callFUT([], ['.', 'bin/test', '-v'])
        self.assertEqual(('.', ['bin/test', '-v'], []), result)
        self.assertEqual(stdout, '')

    def test_one_extension(self):
        # With an extension supplied it is returned in the third
        # parameter of the return value.
        stdout, result = self.callFUT(['-e', 'py', '.', 'bin/test'])
        self.assertEqual(('.', ['bin/test'], ['py']), result)
        self.assertEqual(stdout, '')

    def test_two_extensions(self):
        # With more than one extension supplied they are returned in
        # the third parameter of the return value.
        stdout, result = self.callFUT(
            ['-e', 'py', '-e', 'txt', '.', 'bin/test'])
        self.assertEqual(('.', ['bin/test'], ['py', 'txt']), result)
        self.assertEqual(stdout, '')

    def test_wrong_order_of_extension_an_parameter(self):
        # The (optional) extensions must come before the positional
        # arguments of path and callable.
        stdout, result = self.callFUT(
            ['.', '-e', 'py',  'bin/test'])
        # Option specification becomes part of the callable.
        self.assertEqual(('.', ['-e', 'py',  'bin/test'], []), result)
        self.assertEqual(stdout, '')

    def test_extension_in_additional_params_not_accepted(self):
        # The extensions in the additional parameters are used as
        # options of the callable not ay arguments of
        # icemac.callonchange.
        stdout, result = self.callFUT(
            ['.', 'bin/test'], ['-e', 'py'])
        # Option specification becomes part of the callable.
        self.assertEqual(('.', ['bin/test', '-e', 'py'], []), result)
        self.assertEqual(stdout, '')


class TestObserver(unittest.TestCase):

    def createScript(self, dir=None):
        if dir is None:
            path = self.basedir
        else:
            path = os.path.join(self.basedir, dir)
            if not os.path.exists(path):
                os.mkdir(path)
        filename = os.path.join(path, 'script')
        file = open(filename, 'w')
        file.write('#! /bin/bash\n')
        file.write('echo -n "script called" > "%s"\n' % os.path.join(
            self.basedir, 'result'))
        file.close()
        os.chmod(filename, 0700)
        return filename

    def setUp(self):
        self.basedir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.basedir)

    def test_observer(self):
        # Assert that the script is called when something inside the
        # observed directory changes.
        observer = icemac.callonchange.observer.Observer(
            self.basedir, [self.createScript()], [])
        try:
            observer.start()
            os.mkdir(os.path.join(self.basedir, '1'))
            time.sleep(1)
            self.assertEqual('script called',
                             file(os.path.join(self.basedir, 'result')).read())
        finally:
            observer.stop()

    def test_observer_not_called(self):
        # Assert that the script is _not_ called when something
        # outside the observed directory changes.
        observe_dir = os.path.join(self.basedir, 'observe')
        os.mkdir(observe_dir)
        observer = icemac.callonchange.observer.Observer(
            observe_dir, [self.createScript()], [])
        try:
            observer.start()
            os.mkdir(os.path.join(self.basedir, '1'))
            time.sleep(1)
            self.failIf(os.path.exists(os.path.join(self.basedir, 'result')))
        finally:
            observer.stop()


    def test_not_existing_script(self):
        # When the script does not exist, an error message is
        # displayed.
        orig_stdout = sys.stdout
        try:
            sys.stdout = StringIO.StringIO()
            observer = icemac.callonchange.observer.Observer(
                self.basedir, ['asdf'], [])
            try:
                observer.start()
                os.mkdir(os.path.join(self.basedir, '1'))
                time.sleep(1)
                self.assertEqual(
                    "OSError: (2, 'No such file or directory')\n"
                    "Popen params were:  ('asdf',)\n", sys.stdout.getvalue())
            finally:
                observer.stop()
        finally:
            sys.stdout = orig_stdout


    def test_not_matching_extension(self):
        # When the extension of the changed file inside the observed
        # directory is not in the extenion list, script is not called
        observer = icemac.callonchange.observer.Observer(
            self.basedir, [self.createScript()], ['py'])
        try:
            observer.start()
            my_file = file(os.path.join(self.basedir, 'one.pyc'), 'w')
            my_file.write('asdf')
            my_file.close()
            time.sleep(1)
            self.failIf(os.path.exists(os.path.join(self.basedir, 'result')))
        finally:
            observer.stop()
