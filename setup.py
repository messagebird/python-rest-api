from setuptools import setup

setup(
    name             = 'messagebird',
    packages         = ['messagebird'],
    version          = '1.0.0',
    description      = "MessageBird's REST API",
    author           = 'Maurice Nonnekes',
    author_email     = 'maurice@messagebird.com',
    url              = 'https://github.com/messagebird/python-rest-api',
    install_requires = ['requests>=2.4.1'],
    license          = 'BSD-2-Clause',
)
