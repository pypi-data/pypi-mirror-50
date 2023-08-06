# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['smolstore']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'smolstore',
    'version': '0.1.1a0',
    'description': 'A simple in-memory Python document store',
    'long_description': None,
    'author': 'Raymond Botha',
    'author_email': 'botha@riseup.net',
    'url': 'https://github.com/raybotha/smolstore',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
