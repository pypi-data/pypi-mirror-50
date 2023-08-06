# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pfun']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pfun',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sune Debel',
    'author_email': 'sad@archii.ai',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
