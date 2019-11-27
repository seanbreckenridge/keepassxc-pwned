#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = ['requests', 'docopt']

setup(
    author="Sean Breckenridge",
    author_email='seanbrecke@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=requirements,
    description="Check your keepassxc database against previously breached haveibeenpwned passwords",
    license="MIT",
    include_package_data=True,
    keywords='keepassxc password-strength password',
    name='keepassxc-pwned',
    packages=find_packages(include=['keepassxc_pwned']),
    entry_points = {
        'console_scripts': [
            "keepassxc_pwned = keepassxc_pwned.keepassxc_pwned:main"
        ]
    },
    url='https://github.com/seanbreckenridge/keepassxc-pwned',
    version='0.2.2',
    zip_safe=True,
)
