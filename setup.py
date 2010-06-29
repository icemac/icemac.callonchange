# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import setuptools

version = '0.1'

setuptools.setup(
    name='icemac.callonchange',
    version=version,
    description="Call a command when a directory changes. (Mac OS only)",
    long_description="""\
""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='mac os event fs filesystem call command',
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='http://pypi.python.org/icemac.callonchange',
    license='ZPL',
    packages=setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['icemac'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'MacFSEvents',
        'setuptools',
        ],
    entry_points="""
      [console_scripts]
      callonchange = icemac.callonchange:callonchange
      """,
    test_suite="icemac.tests",
    )
