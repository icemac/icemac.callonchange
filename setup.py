# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013, 2018 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools


def read(path):
    """Read a file from a path."""
    with open(os.path.join(*path.split('/'))) as f:
        return f.read()


version = '0.8'

tests_require = [
    'zc.buildout',
    'zope.testing',
]

setuptools.setup(
    name='icemac.callonchange',
    version=version,
    description=(
        "Call a command when a directory or file has changed. (Mac OS only)"),
    long_description=('\n\n'.join([
        read('README.rst'),
        read('CHANGES.rst'),
        read('DOCS.rst'),
        read('TODO.rst'),
        read('HACKING.rst'),
    ])),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Framework :: Buildout :: Recipe',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords=(
        'mac os event fs filesystem call change command tdd '
        'test driven development'),
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='http://pypi.python.org/icemac.callonchange',
    license='MIT',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'MacFSEvents > 0.2.2, <= 0.2.6',
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
