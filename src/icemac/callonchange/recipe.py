# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import zc.buildout.easy_install


DEFAULT_ARGUMENTS = "'src', 'bin/test', '-cv'"


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        self.executable = buildout['buildout']['executable']
        self.bin_directory = buildout['buildout']['bin-directory']
        self.eggs_directory = buildout['buildout']['eggs-directory']
        self.develop_eggs_directory = buildout['buildout']['develop-eggs-directory']
        self.links = buildout['buildout'].get('find-links', ())
        self.index = buildout['buildout'].get('index')
        self.newest = buildout['buildout'].get('newest') == 'true'
        self.arguments = self.options.get('arguments', DEFAULT_ARGUMENTS)

    def install(self):
        distributions = ['icemac.callonchange']
        ws = zc.buildout.easy_install.install(
            distributions, self.eggs_directory,
            links=self.links,
            index=self.index,
            executable=self.executable,
            path=[self.develop_eggs_directory],
            newest=self.newest)

        return zc.buildout.easy_install.scripts(
            distributions,
            ws,
            self.executable,
            self.bin_directory,
            arguments=self.arguments,
            )


    update = install
