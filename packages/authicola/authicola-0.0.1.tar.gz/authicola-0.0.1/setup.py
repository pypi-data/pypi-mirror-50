import os
from setuptools import setup

import authicola as meta

setup(
    name=meta.__name__,
    version=meta.__version__,
    packages=['authicola'],
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    description=meta.__description__,
    author=meta.__author__,
    author_email=meta.__author_email__,
    url=meta.__url__,
    license=meta.__license__,
    python_requires=">=3.4",
    keywords=['oauth', 'oauth2.0', 'authentication', 'python3', 'google'],
)
