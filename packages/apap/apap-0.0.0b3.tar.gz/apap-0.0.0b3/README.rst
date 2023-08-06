|version| |ci-status|

.. |version| image:: https://img.shields.io/badge/python-3.7-blue.svg?style=flat
    :alt: version
    :scale: 100%
    :target: https://www.python.org/downloads/release/python-370/


.. |ci-status| image:: https://circleci.com/gh/mtwtkman/apap.svg?style=svg
    :alt: circleci status
    :scale: 100%
    :target: https://circleci.com/gh/mtwtkman/apap


====
What
====

`apap` makes you can **ap** ply RESTful **ap** i to your client handy.

========
Required
========

python3.7+


=====
About
=====

This exposes `apap.Client` class to define your api client.
`apap.Client` must be defining `api_base_url` and `_method_map` as class attribute.


.. code:: python

   import apap


   class YourAPI(apap.Client):
      api_base_url = 'https://your.api.com/v1'

      _method_map = apap.MethodMap(
         ('get_all', apap.Method.Get, 'things'),  # all resources from GET http method.
         ('get_one', apap.Method.Get, 'things/:id'),  # one of resources filterd by id from GET http method.
         ('create', apap.Method.Post, 'things'),  # create a new item from POST http method.
         ('update', apap.Method.Put, 'things/:id'),  # update something filterd by id from PUT http method.
         ('delete', apap.Method.Delete, 'things/:id'),  # delete something filterd by id from Delete http method.
      )

      ...


You know `apap.MethodMap` makes your client declarative.

`apap.MethodMap` is just a tuple of client method name, HTTP method and endpoint url.

At last, you need to register your client to entrypoint via `apap.apply`.

Those request returns `requests's Response object <https://2.python-requests.org/en/master/api/#requests.Response>`_ (because `apap` uses `requests` internally).

.. code:: python

   import apap


   client = apap.apply(YourAPI)()

   client.get_all() # same as `curl https://your.api.com/v1/things`
   client.get_one(id=1)()  # same as `curl https://your.api.com/things/1`
   client.create(x=1, y=2)  # same as `curl -X POST -d "x=1" -d "y=2" https://your.api.com/things`
   client.update(id=1)(x=10)  # same as `curl -X PUT -d "x=1" https://your.api.com/things/1`
   client.delete(id=1)()  # same as `curl -X DELETE https://your.api.com/things/1`


When you need to set any headers for requesting, you can use `header_map` attribute to translate actual header from python world.

So if you want to use `Authorization` as http-header, please define `header_map` looks like below.

.. code:: python

   class YourAPI(apap.Client):
      header_map = {'Authorization': 'auth_key'}
      ...


   apap.apply(YourAPI)(headers={'auth_key': 'token xxxxx'})



=======
Example
=======

All you need is just creating a class which inherits `apap.Client` class.

.. code:: python

   import os

   from apap import MethodMap, Client, Method, apply


   class GithubAPI(Client):
     api_base_url = 'https://api.github.com'
     header_map = {'Authorization': 'access_token'}


   class UserRepo(GithubAPI):
     name = 'user_repo'

     _method_map = MethodMap(
        ('get', Method.Get, 'users/:username/repos'),
     )


   class MyRepo(GithubAPI):
       name = 'my_repo'

       _method_map = MethodMap(
           ('get', Method.Get, 'user/repos'),
       )


   access_token = os.environ['ACCESS_TOKEN']

   endpoints = [UserRepo, MyRepo]

   gh_client = apply(*endpoints)(headers={'access_token': f'token {access_token}'})
   user_repo_resp = gh_client.user_repo.get(username='mtwtkman')()
   my_repo_resp = gh_client.my_repo.get(visibility='private')
