from setuptools import setup
from os import path

import authicola as meta

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=meta.__name__,
    version='0.0.2',
    packages=['authicola'],
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    description=meta.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=meta.__author__,
    author_email=meta.__author_email__,
    url=meta.__url__,
    license=meta.__license__,
    python_requires=">=3.4",
    keywords=['oauth', 'oauth2.0', 'authentication', 'python3', 'google'],
)
