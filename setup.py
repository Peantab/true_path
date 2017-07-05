#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click>=6.7',
    'requests>=2.9.1',
    'beautifulsoup4>=4.6.0',
]

test_requirements = [
    'click>=6.7',
    'requests>=2.9.1',
    'beautifulsoup4>=4.6.0',
    'flake8>=3.3.0',
    'pytest>=3.1.1'
]

setup(
    name='true_path',
    version='0.1.0',
    description="Package providing tools that aim at protecting from phishing "
                "by verifying a path (and a content of the webpage "
                "behind it).",
    long_description=readme + '\n\n' + history,
    author="Pawel Taborowski",
    author_email='peantab@gmail.com',
    url='https://github.com/Peantab/true_path',
    packages=[
        'true_path',
    ],
    package_dir={'true_path':
                 'true_path'},
    package_data={'true_path': ['api_key']},
    entry_points={
        'console_scripts': [
            'true_path=true_path.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='true_path',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
