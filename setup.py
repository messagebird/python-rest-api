from os import path
from setuptools import setup

def get_description():
    working_directory = path.abspath(path.dirname(__file__))
    readme_path = path.join(working_directory, 'README.md')
    with open(readme_path, encoding='utf-8') as f:
        return (f.read(), 'text/markdown')

description, description_content_type = get_description()

setup(
    name                          = 'messagebird',
    packages                      = ['messagebird'],
    version                       = '1.3.1',
    description                   = "MessageBird's REST API",
    author                        = 'MessageBird',
    author_email                  = 'support@messagebird.com',
    long_description              = description,
    long_description_content_type = description_content_type,
    url                           = 'https://github.com/messagebird/python-rest-api',
    download_url                  = 'https://github.com/messagebird/python-rest-api/tarball/1.3.1',
    keywords                      = ['messagebird', 'sms'],
    install_requires              = ['requests>=2.4.1'],
    license                       = 'BSD-2-Clause',
    classifiers                   = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
