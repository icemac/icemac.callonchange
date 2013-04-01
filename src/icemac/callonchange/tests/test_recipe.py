# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt
from zope.testing import renormalizing
import doctest
import re
import zc.buildout.testing


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop("MacFSEvents", test)
    zc.buildout.testing.install_develop("icemac.callonchange", test)


def test_suite():
    return doctest.DocFileSuite(
        'bugfix.txt',
        'recipe.txt',
        setUp=setUp,
        tearDown=zc.buildout.testing.buildoutTearDown,
        optionflags=doctest.ELLIPSIS,
        checker=renormalizing.RENormalizing([
            (re.compile('Not found: /.*/\n'), '')
            ]))
