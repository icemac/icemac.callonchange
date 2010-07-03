# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.name, self.options = name, options

    def install(self):
        return []

    update = install
