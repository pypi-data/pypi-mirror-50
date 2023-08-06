# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['apap']

package_data = \
{'': ['*']}

install_requires = \
['mypy_extensions==0.4.1', 'requests==2.22.0']

setup_kwargs = {
    'name': 'apap',
    'version': '0.0.0b3',
    'description': 'Declarative and handy RESTful client factory',
    'long_description': '|version| |ci-status|\n\n.. |version| image:: https://img.shields.io/badge/python-3.7-blue.svg?style=flat\n    :alt: version\n    :scale: 100%\n    :target: https://www.python.org/downloads/release/python-370/\n\n\n.. |ci-status| image:: https://circleci.com/gh/mtwtkman/apap.svg?style=svg\n    :alt: circleci status\n    :scale: 100%\n    :target: https://circleci.com/gh/mtwtkman/apap\n\n\n====\nWhat\n====\n\n`apap` makes you can **ap** ply RESTful **ap** i to your client handy.\n\n========\nRequired\n========\n\npython3.7+\n\n\n=====\nAbout\n=====\n\nThis exposes `apap.Client` class to define your api client.\n`apap.Client` must be defining `api_base_url` and `_method_map` as class attribute.\n\n\n.. code:: python\n\n   import apap\n\n\n   class YourAPI(apap.Client):\n      api_base_url = \'https://your.api.com/v1\'\n\n      _method_map = apap.MethodMap(\n         (\'get_all\', apap.Method.Get, \'things\'),  # all resources from GET http method.\n         (\'get_one\', apap.Method.Get, \'things/:id\'),  # one of resources filterd by id from GET http method.\n         (\'create\', apap.Method.Post, \'things\'),  # create a new item from POST http method.\n         (\'update\', apap.Method.Put, \'things/:id\'),  # update something filterd by id from PUT http method.\n         (\'delete\', apap.Method.Delete, \'things/:id\'),  # delete something filterd by id from Delete http method.\n      )\n\n      ...\n\n\nYou know `apap.MethodMap` makes your client declarative.\n\n`apap.MethodMap` is just a tuple of client method name, HTTP method and endpoint url.\n\nAt last, you need to register your client to entrypoint via `apap.apply`.\n\nThose request returns `requests\'s Response object <https://2.python-requests.org/en/master/api/#requests.Response>`_ (because `apap` uses `requests` internally).\n\n.. code:: python\n\n   import apap\n\n\n   client = apap.apply(YourAPI)()\n\n   client.get_all() # same as `curl https://your.api.com/v1/things`\n   client.get_one(id=1)()  # same as `curl https://your.api.com/things/1`\n   client.create(x=1, y=2)  # same as `curl -X POST -d "x=1" -d "y=2" https://your.api.com/things`\n   client.update(id=1)(x=10)  # same as `curl -X PUT -d "x=1" https://your.api.com/things/1`\n   client.delete(id=1)()  # same as `curl -X DELETE https://your.api.com/things/1`\n\n\nWhen you need to set any headers for requesting, you can use `header_map` attribute to translate actual header from python world.\n\nSo if you want to use `Authorization` as http-header, please define `header_map` looks like below.\n\n.. code:: python\n\n   class YourAPI(apap.Client):\n      header_map = {\'Authorization\': \'auth_key\'}\n      ...\n\n\n   apap.apply(YourAPI)(headers={\'auth_key\': \'token xxxxx\'})\n\n\n\n=======\nExample\n=======\n\nAll you need is just creating a class which inherits `apap.Client` class.\n\n.. code:: python\n\n   import os\n\n   from apap import MethodMap, Client, Method, apply\n\n\n   class GithubAPI(Client):\n     api_base_url = \'https://api.github.com\'\n     header_map = {\'Authorization\': \'access_token\'}\n\n\n   class UserRepo(GithubAPI):\n     name = \'user_repo\'\n\n     _method_map = MethodMap(\n        (\'get\', Method.Get, \'users/:username/repos\'),\n     )\n\n\n   class MyRepo(GithubAPI):\n       name = \'my_repo\'\n\n       _method_map = MethodMap(\n           (\'get\', Method.Get, \'user/repos\'),\n       )\n\n\n   access_token = os.environ[\'ACCESS_TOKEN\']\n\n   endpoints = [UserRepo, MyRepo]\n\n   gh_client = apply(*endpoints)(headers={\'access_token\': f\'token {access_token}\'})\n   user_repo_resp = gh_client.user_repo.get(username=\'mtwtkman\')()\n   my_repo_resp = gh_client.my_repo.get(visibility=\'private\')\n',
    'author': 'mtwtkman',
    'author_email': 'yo@mtwtkman.dev',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
