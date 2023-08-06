##############################################################################
#
# Copyright (c) 2019 Jens Vagelpohl and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os

from setuptools import find_packages
from setuptools import setup


NAME = 'dataflake.wsgi.bjoern'
URL = 'https://github.com/dataflake/%s' % NAME
VERSION = '1.1'


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name=NAME,
    version=VERSION,
    url=URL,
    project_urls={
        'Documentation': 'https://dataflakewsgibjoern.readthedocs.io',
        'Issue Tracker': '%s/issues' % URL,
        'Sources': URL,
    },
    license='ZPL 2.1',
    description='PasteDeploy entry point for the bjoern WSGI server',
    author='Jens Vagelpohl and Contributors',
    author_email='jens@netz.ooo',
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
    packages=find_packages(),
    namespace_packages=['dataflake', 'dataflake.wsgi'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope',
        'Framework :: Zope :: 4',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        'setuptools',
        'bjoern',
        'paste',  # For the translogger logging filter
        'Zope',  # To avoid reinventing the skeleton creation
    ],
    extras_require={
        'docs': [
            'Sphinx < 2;python_version < "3"',
            'Sphinx;python_version >= "3"',
            'sphinx_rtd_theme',
        ],
    },
    entry_points={
        'paste.server_runner': [
            'main=dataflake.wsgi.bjoern:serve_paste',
        ],
        'console_scripts': [
            'mkbjoerninstance=dataflake.wsgi.bjoern.configurator:mkzope',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
