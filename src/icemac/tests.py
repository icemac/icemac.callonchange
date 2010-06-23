# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import StringIO
import icemac.callonchange
import os
import os.path
import shutil
import sys
import tempfile
import time
import unittest


def grap_stdout(callable, *args, **kw):
    orig_stdout = sys.stdout
    sys.stdout = StringIO.StringIO()
    try:
        result = callable(*args, **kw)
        return sys.stdout.getvalue(), result
    finally:
        sys.stdout = orig_stdout


class TestMangle(unittest.TestCase):

    def read_stdout(self):
        return sys.stdout.getvalue()

    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    def callFUT(self, *args):
        return grap_stdout(
            icemac.callonchange.mangle_call_args(*args))

    def test_no_args(self):
        stdout, result = self.callFUT(None, None, [])
        self.assertEqual((None, None), result)
        self.failUnless(stdout.startswith('USAGE'))

# XXX

    def test_missing_params(self):
        self.assertEqual((None, None),
                         icemac.callonchange.mangle_call_args('.', None, []))
        self.failUnless(self.read_stdout().startswith('USAGE'))

    def test_no_additional_args(self):
        self.assertEqual(
            ('.', ['bin/test']),
            icemac.callonchange.mangle_call_args('.', 'bin/test', []))
        self.assertEqual(self.read_stdout(), '')

    def test_additional_args(self):
        self.assertEqual(
            ('.', ['bin/test', '-t', 'TestMangle']),
            icemac.callonchange.mangle_call_args(
                '.', 'bin/test', ['-t', 'TestMangle']))
        self.assertEqual(self.read_stdout(), '')

    def test_only_additional_args(self):
        self.assertEqual(
            ('.', ['bin/test', '-v']),
            icemac.callonchange.mangle_call_args(
                None, None, ['.', 'bin/test', '-v']))
        self.assertEqual(self.read_stdout(), '')


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
        super(TestObserver, self).setUp()

    def tearDown(self):
        super(TestObserver, self).tearDown()
        shutil.rmtree(self.basedir)

    def test_observer(self):
        observer = icemac.callonchange.Observer(
            self.basedir, [self.createScript()])
        observer.start()
        os.mkdir(os.path.join(self.basedir, '1'))
        time.sleep(0.5)
        try:
            self.assertEqual('script called',
                             file(os.path.join(self.basedir, 'result')). read())
        finally:
            observer.stop()

    def test_script_error(self):
        observer = icemac.callonchange.Observer(
            self.basedir, ['asdf'])
        observer.start()
        os.mkdir(os.path.join(self.basedir, '1'))
        time.sleep(0.5)

