Installation
============

.. code:: bash

    pip install fastapi-jsonrpc

Usage
=====

.. code:: bash

    pip install uvicorn

.. code:: python

    import fastapi_jsonrpc as jsonrpc
    from fastapi_jsonrpc import Param

    app = jsonrpc.API()

    api_v1 = jsonrpc.Entrypoint('/api/v1/jsonrpc')

    @api_v1.method()
    def echo(
        data: str = Param(..., example="123"),
    ) -> str:
        return data

    app.bind_entrypoint(api_v1)

    if __name__ == '__main__':
        import uvicorn
        uvicorn.run(app, port=5000, debug=True, access_log=False)

Go to:

    http://127.0.0.1:5000/docs

Development
===========

1. Install poetry

    https://github.com/sdispater/poetry#installation

2. Install dependencies

    .. code:: bash

        poetry update

3. Install dephell

    .. code:: bash

        pip install dephell

4. Regenerate setup.py

    .. code:: bash

        dephell deps convert

Changelog
=========

[0.1.3] fix README.rst

[0.1.2] Add usage example to README.rst

[0.1.1] README.rst

[0.1.0] Initial commit
