# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fastapi_jsonrpc']

package_data = \
{'': ['*']}

install_requires = \
['aiojobs>=0.2.2,<0.3.0',
 'fastapi>=0.35.0,<0.36.0',
 'pydantic>=0.30,<0.31',
 'starlette>=0.12.7,<0.13.0']

setup_kwargs = {
    'name': 'fastapi-jsonrpc',
    'version': '0.1.15',
    'description': 'JSON-RPC server based on fastapi',
    'long_description': "Description\n===========\n\nJSON-RPC server based on fastapi:\n\n    https://fastapi.tiangolo.com\n\nInstallation\n============\n\n.. code:: bash\n\n    pip install fastapi-jsonrpc\n\nUsage\n=====\n\n.. code:: bash\n\n    pip install uvicorn\n\n.. code:: python\n\n    import fastapi_jsonrpc as jsonrpc\n    from fastapi_jsonrpc import Param\n    from pydantic import BaseModel\n\n\n    app = jsonrpc.API()\n\n    api_v1 = jsonrpc.Entrypoint('/api/v1/jsonrpc')\n\n\n    class MyError(jsonrpc.BaseError):\n        CODE = 5000\n        MESSAGE = 'My error'\n\n        class DataModel(BaseModel):\n            details: str\n\n\n    @api_v1.method(errors=[MyError])\n    def echo(\n        data: str = Param(..., example='123'),\n    ) -> str:\n        if data == 'error':\n            raise MyError(data={'details': 'error'})\n        else:\n            return data\n\n\n    app.bind_entrypoint(api_v1)\n\n\n    if __name__ == '__main__':\n        import uvicorn\n        uvicorn.run(app, port=5000, debug=True, access_log=False)\n\nGo to:\n\n    http://127.0.0.1:5000/docs\n\nDevelopment\n===========\n\n1. Install poetry\n\n    https://github.com/sdispater/poetry#installation\n\n2. Install dependencies\n\n    .. code:: bash\n\n        poetry update\n\n3. Install dephell\n\n    .. code:: bash\n\n        pip install dephell\n\n4. Regenerate setup.py\n\n    .. code:: bash\n\n        dephell deps convert\n",
    'author': 'Sergey Magafurov',
    'author_email': 'magafurov@tochka.com',
    'url': 'https://github.com/smagafurov/fastapi-jsonrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
