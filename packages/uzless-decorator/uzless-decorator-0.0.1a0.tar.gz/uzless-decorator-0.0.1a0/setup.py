# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['uzless_decorator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'uzless-decorator',
    'version': '0.0.1a0',
    'description': 'this project aim to simplify architecture description using decorators',
    'long_description': None,
    'author': 'Tigran Tchougourian',
    'author_email': 'nargitinthenight@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
