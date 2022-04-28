import os
import re
from setuptools import setup
from io import open

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'messagebird/version.py'), 'r') as fd:
    VERSION = re.search(r'^VERSION = [\']([^\']*)[\']',
                        fd.read(), re.MULTILINE).group(1)

if not VERSION:
    raise RuntimeError('Ensure `VERSION` is correctly set in ./messagebird/version.py')

with open('README.md', encoding='utf-8') as f:
    description = f.read()

setup(
    name                          = 'messagebird',
    packages                      = ['messagebird'],
    version                       = VERSION,
    description                   = "MessageBird's REST API",
    author                        = 'MessageBird',
    author_email                  = 'support@messagebird.com',
    long_description              = description,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/messagebird/python-rest-api',
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
