# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013, 2018-2019 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools


def read(path):
    """Read a file from a path."""
    with open(os.path.join(*path.split('/'))) as f:
        return f.read()


version = '1.0.dev0'

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
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords=(
        'mac os event fs filesystem call change command tdd '
        'test driven development'),
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='https://github.com/icemac/icemac.callonchange',
    license='MIT',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'MacFSEvents < 0.8.1',
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
