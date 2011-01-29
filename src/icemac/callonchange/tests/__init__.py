# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt


def additional_tests():
    # needed function to find doctests when runing `python setup.py test`
    import test_recipe
    return test_recipe.test_suite()
