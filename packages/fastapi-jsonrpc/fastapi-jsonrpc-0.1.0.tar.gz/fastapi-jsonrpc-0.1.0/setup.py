# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fastapi_jsonrpc']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.34.0']

setup_kwargs = {
    'name': 'fastapi-jsonrpc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sergey Magafurov',
    'author_email': 'magafurov@tochka.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
