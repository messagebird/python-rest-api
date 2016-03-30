from setuptools import setup

setup(
    name             = 'messagebird',
    packages         = ['messagebird'],
    version          = '1.2.0',
    description      = "MessageBird's REST API",
    author           = 'MessageBird',
    author_email     = 'support@messagebird.com',
    url              = 'https://github.com/messagebird/python-rest-api',
    download_url     = 'https://github.com/messagebird/python-rest-api/tarball/1.2.0',
    keywords         = ['messagebird', 'sms'],
    install_requires = ['requests>=2.4.1'],
    license          = 'BSD-2-Clause',
)
