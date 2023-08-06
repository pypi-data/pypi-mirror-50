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
    'version': '0.1.1',
    'description': '',
    'long_description': 'Installation\n============\n\npip install fastapi-jsonrpc\n\nDevelopment\n===========\n\n1. Install poetry\n\n    https://github.com/sdispater/poetry#installation\n\n2. Update dependencies\n\n.. code:: bash\n\n    poetry update\n\n3. Install dependencies\n\n.. code:: bash\n\n    poetry install\n\n4. Install dephell\n\n.. code:: bash\n\n    pip install dephell\n\n5. Regenerate setup.py\n\n.. code:: bash\n\n    dephell deps convert\n\nChangelog\n=========\n\n[0.1.1] README.rst\n\n[0.1.0] Initial commit\n',
    'author': 'Sergey Magafurov',
    'author_email': 'magafurov@tochka.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
