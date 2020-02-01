#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages

with io.open("requirements.txt", 'r', encoding='utf-8') as req_file:
    requirements = req_file.read().splitlines()

with io.open("README.md", 'r', encoding='utf-8') as readme:
    readme_contents = readme.read()

setup(
    author="Sean Breckenridge",
    author_email='seanbrecke@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=requirements,
    description="Check your keepassxc database against previously breached haveibeenpwned passwords",
    license="MIT",
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='keepassxc password-strength password',
    name='keepassxc-pwned',
    packages=find_packages(include=['keepassxc_pwned']),
    entry_points = {
        'console_scripts': [
            "keepassxc_pwned = keepassxc_pwned.cli:main"
        ]
    },
    url='https://github.com/seanbreckenridge/keepassxc-pwned',
    version='0.3.0',
    zip_safe=True,
)
