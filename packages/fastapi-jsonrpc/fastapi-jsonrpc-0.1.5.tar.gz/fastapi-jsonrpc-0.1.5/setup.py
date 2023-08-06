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
    'version': '0.1.5',
    'description': '',
    'long_description': "Description\n===========\n\nJSON-RPC server based on fastapi:\n\n    https://fastapi.tiangolo.com\n\nInstallation\n============\n\n.. code:: bash\n\n    pip install fastapi-jsonrpc\n\nUsage\n=====\n\n.. code:: bash\n\n    pip install uvicorn\n\n.. code:: python\n\n    import fastapi_jsonrpc as jsonrpc\n    from fastapi_jsonrpc import Param\n\n    app = jsonrpc.API()\n\n    api_v1 = jsonrpc.Entrypoint('/api/v1/jsonrpc')\n\n    class MyErrorDataModel(BaseModel):\n        details: str\n\n    class MyError(jsonrpc.BaseError):\n        CODE = 5000\n        MESSAGE = 'My error'\n        data_model = MyErrorDataModel\n\n    @api_v1.method(errors=[MyError])\n    def echo(\n        data: str = Param(..., example='123'),\n    ) -> str:\n        if data == 'error':\n            raise MyError(data={'details': 'error'})\n        return data\n\n    app.bind_entrypoint(api_v1)\n\n    if __name__ == '__main__':\n        import uvicorn\n        uvicorn.run(app, port=5000, debug=True, access_log=False)\n\nGo to:\n\n    http://127.0.0.1:5000/docs\n\nDevelopment\n===========\n\n1. Install poetry\n\n    https://github.com/sdispater/poetry#installation\n\n2. Install dependencies\n\n    .. code:: bash\n\n        poetry update\n\n3. Install dephell\n\n    .. code:: bash\n\n        pip install dephell\n\n4. Regenerate setup.py\n\n    .. code:: bash\n\n        dephell deps convert\n\nChangelog\n=========\n\n[0.1.5] Add error usage example to README.rst\n\n[0.1.4] Add description to README.rst\n\n[0.1.3] Fix README.rst\n\n[0.1.2] Add usage example to README.rst\n\n[0.1.1] README.rst\n\n[0.1.0] Initial commit\n",
    'author': 'Sergey Magafurov',
    'author_email': 'magafurov@tochka.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
