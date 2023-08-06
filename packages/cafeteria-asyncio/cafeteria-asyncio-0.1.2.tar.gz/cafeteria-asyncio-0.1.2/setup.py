# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cafeteria', 'cafeteria.asyncio', 'cafeteria.asyncio.patterns']

package_data = \
{'': ['*']}

install_requires = \
['cafeteria>=0,<1']

setup_kwargs = {
    'name': 'cafeteria-asyncio',
    'version': '0.1.2',
    'description': 'An extension to the cafeteria package to enable asyncio specific patterns for python 3.7 and above applications/libraries.',
    'long_description': '[![Build Status](https://travis-ci.org/abn/cafeteria-asyncio.svg?branch=master)](https://travis-ci.org/abn/cafeteria-asyncio)\n[![image](https://img.shields.io/pypi/v/cafeteria-asyncio.svg)](https://pypi.org/project/cafeteria-asyncio/)\n[![image](https://img.shields.io/pypi/l/cafeteria-asyncio.svg)](https://pypi.org/project/cafeteria-asyncio/)\n[![image](https://img.shields.io/pypi/pyversions/cafeteria-asyncio.svg)](https://pypi.org/project/cafeteria-asyncio/)\n[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n# Asyncio Patterns and Utilities\nAn extension to the cafeteria package to enable asyncio specific patterns for python 3.7 and above applications/libraries.\n\n## Installation\n`pip install cafeteria-asyncio`\n',
    'author': 'Arun Babu Neelicattu',
    'author_email': 'arun.neelicattu@gmail.com',
    'url': 'https://github.com/abn/cafeteria-asyncio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
