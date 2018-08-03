# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt

import icemac.callonchange.observer
import icemac.callonchange.testing
import unittest


# Options which are set by default by the mangle function when no
# options are set. After adding new options enter them here:
DEFAULT_OPTIONS = {'extensions': [], 'quite': False, 'immediate': False}


def expected_options(**options):
    """Expected options which differ from default."""
    # Expected options are the default ones updated by the ones
    # different:
    expected = DEFAULT_OPTIONS.copy()
    expected.update(options)
    return expected


class TestMangle(unittest.TestCase):

    def callFUT(self, arg, argv=None):
        if not argv:
            argv = []
        return icemac.callonchange.testing.grapStdout(
            icemac.callonchange.observer.mangle_call_args, arg, argv)

    def test_no_args(self):
        # With no arguments supplied, usage is shown.
        stdout, result = self.callFUT([])
        self.assertEqual((None, None, None), result)
        self.assertTrue(stdout.lower().startswith('usage:'))

    def test_missing_params(self):
        # With not enough arguments supplied, usage is shown.
        stdout, result = self.callFUT(['.'])
        self.assertEqual((None, None, None), result)
        self.assertTrue(stdout.lower().startswith('usage:'))

    def test_only_extension(self):
        # With only extensions supplied, usage is shown.
        stdout, result = self.callFUT(['-e', '.py'])
        self.assertEqual((None, None, None), result)
        self.assertTrue(stdout.lower().startswith('usage:'))

    def test_no_additional_args(self):
        # Without additional arguments the default arguments are used.
        stdout, result = self.callFUT(['.', 'bin/test'])
        self.assertEqual(('.', ['bin/test'], expected_options()), result)
        self.assertEqual(stdout, '')

    def test_additional_args(self):
        # With additional arguments these are added to the default ones.
        stdout, result = self.callFUT(
            ['.', 'bin/test'], ['-t', 'TestMangle'])
        self.assertEqual(('.',
                          ['bin/test', '-t', 'TestMangle'],
                          expected_options()), result)
        self.assertEqual(stdout, '')

    def test_only_additional_args(self):
        # With only additional arguments supplied, they are used
        # instead of the default ones.
        stdout, result = self.callFUT([], ['.', 'bin/test', '-v'])
        self.assertEqual(('.', ['bin/test', '-v'], expected_options()), result)
        self.assertEqual(stdout, '')

    def test_one_extension(self):
        # With an extension supplied it is returned in the third
        # parameter of the return value.
        stdout, result = self.callFUT(['-e', '.py', '.', 'bin/test'])
        self.assertEqual(('.',
                          ['bin/test'],
                          expected_options(extensions=['.py'])), result)
        self.assertEqual(stdout, '')

    def test_two_extensions(self):
        # With more than one extension supplied they are returned in
        # the third parameter of the return value.
        stdout, result = self.callFUT(
            ['-e', '.py', '-e', '.txt', '.', 'bin/test'])
        self.assertEqual(('.',
                          ['bin/test'],
                          expected_options(extensions=['.py', '.txt'])),
                         result)
        self.assertEqual(stdout, '')

    def test_wrong_order_of_extension_an_parameter(self):
        # The (optional) extensions must come before the positional
        # arguments of path and callable.
        stdout, result = self.callFUT(
            ['.', '-e', '.py', 'bin/test'])
        # Option specification becomes part of the callable.
        self.assertEqual(('.', ['-e', '.py', 'bin/test'], expected_options()),
                         result)
        self.assertEqual(stdout, '')

    def test_extension_in_additional_params_not_accepted(self):
        # The extensions in the additional parameters are used as
        # options of the callable not ay arguments of
        # icemac.callonchange.
        stdout, result = self.callFUT(
            ['.', 'bin/test'], ['-e', '.py'])
        # Option specification becomes part of the callable.
        self.assertEqual(('.', ['bin/test', '-e', '.py'], expected_options()),
                         result)
        self.assertEqual(stdout, '')

    def test_extension_without_dot_gets_dot_added(self):
        # When the extension is specified without the leading dot it
        # gets added.
        stdout, result = self.callFUT(
            ['-e', 'py', '.', 'bin/test'])
        # In the result the extensions list contains the extension
        # including a leading dot. This is for convinience.
        self.assertEqual(('.',
                          ['bin/test'],
                          expected_options(extensions=['.py'])), result)
        self.assertEqual(stdout, '')

    def test_quite(self):
        # The option -q makes callonchange quite.
        stdout, result = self.callFUT(['-q', '.', 'bin/test'])
        # The result the options dict contains a key for "quite":
        self.assertEqual(('.',
                          ['bin/test'],
                          expected_options(quite=True)), result)
        self.assertEqual(stdout, '')

    def test_immediate(self):
        # The option -i makes callonchange running immediately after start.
        stdout, result = self.callFUT(['-i', '.', 'bin/test'])
        # The result the options dict contains a key for "immediate":
        self.assertEqual(('.',
                          ['bin/test'],
                          expected_options(immediate=True)), result)
        self.assertEqual(stdout, '')
