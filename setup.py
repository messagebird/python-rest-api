from os import path
from setuptools import setup
from io import open

with open('README.md', encoding='utf-8') as f:
    description = f.read()

setup(
    name                          = 'messagebird',
    packages                      = ['messagebird'],
    version                       = '2.0.0',
    description                   = "MessageBird's REST API",
    author                        = 'MessageBird',
    author_email                  = 'support@messagebird.com',
    long_description              = description,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/messagebird/python-rest-api',
    download_url                  = 'https://github.com/messagebird/python-rest-api/tarball/2.0.0',
    keywords                      = ['messagebird', 'sms'],
    install_requires              = ['requests>=2.4.1', 'python-dateutil>=2.6.0', 'pyjwt>=2.1.0'],
    extras_require               = {
        'dev': [
            'pytest',
            'pytest-cov',
            'mock>=2.0',
            'codecov',
            'pycodestyle',
        ]
    },
    license                       = 'BSD-2-Clause',
    classifiers                   = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
