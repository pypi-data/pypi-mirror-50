#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always use setuptools over distutils.
from setuptools import setup, find_packages
import os
# from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

from sphinx_content_filter import *


current_dir = os.path.dirname(os.path.abspath(__file__))

def read_text_lines(fname):
    with io.open(os.path.join(current_dir, fname)) as fd:
        return fd.readlines()


print(">>> STARTING PACKAGE SETUP <<<\n")

print("... PARSING CONFIG FILES ...\n")

print("... PARSING DESCRIPTION RST ...\n")

# with open('DESCRIPTION.rst') as description_file:
#     description_text = str(description_file.read())

description_lines = read_text_lines('DESCRIPTION.rst')
filtered_description_lines = ''.join(yield_sphinx_only_markup(description_lines)),

print("... PARSING README RST ...\n")

with open('README.rst') as readme_file:
    readme = readme_file.read()

# readme_lines = read_text_lines('README.rst')
# filtered_readme_lines = ''.join(yield_sphinx_only_markup(readme_lines)),

print("... PARSING HISTORY RST ...\n")

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# history_lines = read_text_lines('HISTORY.rst')
# filtered_history_lines = ''.join(yield_sphinx_only_markup(history_lines)),
# filtered_long_description = filtered_readme_lines + filtered_history_lines

print("\n... ASSIGNING CONFIGURATION VALUES ...\n")

# Configuration for package when publishing.
# Edit these values to reflect your package details.
# -->>> !!!! IMPORTANT: BUMP THE VERSION WITH EVERY COMMIT USING SEMVER CONVENTIONS  <Major.minor.patch> !!!! <<<--
module_version                          = '0.0.36'    # This value MUST be aligned with the value in .genome-dashboard-python/genomedashboard/__init__.py!!!
module_name                             = 'genomedashboard'
module_authors                          = 'Zilong Li, Ran Sun, Thomas C. Bishop'
module_authors_email                    = 'zli007@latech.edu, rsu007@latech.edu, bishop@latech.edu'
module_license                          = "MIT license"
module_url                              = 'https://github.com/genomeDashboard/genomedashboard'
module_project_urls                     = {
                                            'PyPI': 'https://pypi.org/project/genomedashboard/0.0.34/',
                                            'Documentation': 'https://genomedashboard.readthedocs.io/en/latest/readme.html',
                                            'Source Code': 'https://github.com/genomeDashboard/genomedashboard',
                                            'Issue Tracker': 'https://github.com/genome-dashboard/genome-dashboard-python/issues',
                                            'Demo': 'http://dna.engr.latech.edu/~gdash/GDash-landing-page/',
                                            # 'Funding': 'https://donate.pypi.org',
                                            # 'Say Thanks!': 'http://saythanks.io/to/example',
                                        }
module_keywords                         = 'python biology genomics genome dashboard'
module_python                           = '>=3.5'
# module_description                      = description_text
module_description                      = filtered_description_lines

# 'text/plain',  'text/markdown' or 'text/x-rst'.
# module_long_description_content_type    = 'text/plain'
# module_long_description_content_type    = 'text/markdown'
module_long_description_content_type    = 'text/x-rst'
# module_long_description                 = readme
module_long_description                 = readme + '\n\n' + history
# module_long_description                 = filtered_long_description
# module_long_description                 = module_description
# module_long_description                 = "THIS DOESNT WORK IN BUILD"
# module_long_description                 = "See description."

module_data_included                    = True
module_enable_compression               = False
module_test_suite                       = 'tests'

module_includes                         = [
                                            'genomedashboard',
                                            'cli',
                                            'genomedashboard.convert',
                                            'genomedashboard.data',
                                            'genomedashboard.ds',
                                            'genomedashboard.io',
                                        ]

module_excludes                         = [
                                            'contrib',
                                            'docs',
                                            'tests'

                                        ]

module_install_requires                 = [
                                            'Click>=6.0',
                                            'peppercorn',
                                        ]

module_setup_requires                   = [ ]
module_test_requires                    = [ ]

module_classifiers                      = [
                                            'Development Status :: 2 - Pre-Alpha',
                                            'Intended Audience :: Developers',
                                            'Intended Audience :: Science/Research',
                                            'Intended Audience :: Healthcare Industry',
                                            'Intended Audience :: Education',
                                            'Topic :: Software Development :: Libraries',
                                            'License :: OSI Approved :: MIT License',
                                            'Natural Language :: English',
                                            "Programming Language :: Python :: 2",
                                            'Programming Language :: Python :: 2.7',
                                            'Programming Language :: Python :: 3',
                                            'Programming Language :: Python :: 3.4',
                                            'Programming Language :: Python :: 3.5',
                                            'Programming Language :: Python :: 3.6',
                                            'Programming Language :: Python :: 3.7',
                                        ]

module_entry_points                     = {
                                            'console_scripts': [
                                                'genomedashboard=genomedashboard.cli:main',
                                            ],
                                        }

module_package_data                     = {
                                            '': ['*.txt'],
                                            'genomedashboard': ['data/*.dat'],
                                        }

module_extras_require                   = {
                                            'dev': ['check-manifest'],
                                            'test': ['coverage'],
                                        }


print("\n... BUILDING PACKAGE ...\n")

# Setup method to publish package.
# DO NOT EDIT BELOW THIS LINE.
setup(
    name                            = module_name,
    version                         = module_version,
    description                     = module_description,
    packages                        = find_packages(include = module_includes, exclude = module_excludes),
    python_requires                 = module_python,
    author                          = module_authors,
    author_email                    = module_authors_email,
    long_description_content_type   = module_long_description_content_type,
    long_description                = module_long_description,
    license                         = module_license,
    url                             = module_url,
    project_urls                    = module_project_urls,
    classifiers                     = module_classifiers,
    keywords                        = module_keywords,
    install_requires                = module_install_requires,
    extras_require                  = module_extras_require,
    package_data                    = module_package_data,
    entry_points                    = module_entry_points,
    include_package_data            = module_data_included,
    zip_safe                        = module_enable_compression,
    setup_requires                  = module_setup_requires,
    test_suite                      = module_test_suite,
    tests_require                   = module_test_requires,
)

print("\n>>> PACKAGE SETUP FINISHED <<<\n")
