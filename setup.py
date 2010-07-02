# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools

def read(*path_elements):
    return "\n\n" + file(os.path.join(*path_elements)).read()


version = '0.1'


setuptools.setup(
    name='icemac.callonchange',
    version=version,
    description="Call a command when a directory changes. (Mac OS only)",
    long_description=(
        read('README.txt') +
        read('TODO.txt') +
        read('CHANGES.txt')
        ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
#        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        ],
    keywords=(
        'mac os event fs filesystem call command tdd test driven development'),
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
        'MacFSEvents',
        'setuptools',
        ],
    entry_points="""
      [console_scripts]
      callonchange = icemac.callonchange:callonchange
      """,
    test_suite="icemac.tests",
    )
