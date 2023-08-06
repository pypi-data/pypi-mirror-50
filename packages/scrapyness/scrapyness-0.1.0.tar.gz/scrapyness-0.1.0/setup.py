# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['scrapyness']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scrapyness',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Hayk Khachatryan',
    'author_email': 'hi@hayk.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
