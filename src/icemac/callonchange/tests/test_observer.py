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
        stdout, result = self.callFUT([])
        self.assertEqual((None, None), result)
        self.failUnless(stdout.startswith('USAGE'))

    def test_missing_params(self):
        stdout, result = self.callFUT(['.'])
        self.assertEqual((None, None), result)
        self.failUnless(stdout.startswith('USAGE'))

    def test_no_additional_args(self):
        stdout, result = self.callFUT(['.', 'bin/test'])
        self.assertEqual(('.', ('bin/test', )), result)
        self.assertEqual(stdout, '')

    def test_additional_args(self):
        stdout, result = self.callFUT(
            ['.', 'bin/test'], ['-t', 'TestMangle'])
        self.assertEqual(('.', ('bin/test', '-t', 'TestMangle')), result)
        self.assertEqual(stdout, '')

    def test_only_additional_args(self):
        stdout, result = self.callFUT([], ['.', 'bin/test', '-v'])
        self.assertEqual(('.', ('bin/test', '-v')), result)
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
        observer = icemac.callonchange.observer.Observer(
            self.basedir, [self.createScript()])
        observer.start()
        os.mkdir(os.path.join(self.basedir, '1'))
        time.sleep(1)
        try:
            self.assertEqual('script called',
                             file(os.path.join(self.basedir, 'result')).read())
        finally:
            observer.stop()

    def test_not_existing_script(self):
        try:
            orig_stdout = sys.stdout
            sys.stderr = StringIO.StringIO()
            sys.stdout = StringIO.StringIO()
            observer = icemac.callonchange.observer.Observer(
                self.basedir, ['asdf'])
            observer.start()
            os.mkdir(os.path.join(self.basedir, '1'))
            time.sleep(1)
            self.assertEqual(
                "OSError: (2, 'No such file or directory')\n"
                "Popen params were:  ('asdf',)\n", sys.stdout.getvalue())
        finally:
            observer.stop()
            sys.stdout = orig_stdout

