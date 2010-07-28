# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools

def read(*path_elements):
    return "\n\n" + file(os.path.join(*path_elements)).read()


version = '0.6'

tests_require = ['zc.buildout',
                ]

setuptools.setup(
    name='icemac.callonchange',
    version=version,
    description=(
        "Call a command when a directory or file has changed. (Mac OS only)"),
    long_description=(
        read('README.txt') +
        read('TODO.txt') +
        read('CHANGES.txt')
        ),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        ],
    keywords=(
        'mac os event fs filesystem call change command tdd '
        'test driven development'),
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='http://pypi.python.org/icemac.callonchange',
    license='ZPL 2.1',
    packages=setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['icemac'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'MacFSEvents > 0.2.2',
        'setuptools',
        ],
    extras_require=dict(
        test=tests_require),
    entry_points="""
      [console_scripts]
      callonchange = icemac.callonchange.script:callonchange
      [zc.buildout]
      default = icemac.callonchange.recipe:Recipe
      """,
    tests_require=tests_require,
    test_suite="icemac.callonchange.tests",
    )
