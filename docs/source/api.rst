API Testing Guide
=================

Authentication
--------------

- ``POST /api/token/``
- ``POST /api/token/refresh/``

Articles
--------

- ``GET /api/articles/``
- ``POST /api/articles/``
- ``GET /api/articles/<id>/``
- ``PUT /api/articles/<id>/``
- ``DELETE /api/articles/<id>/``
- ``POST /api/articles/<id>/approve/``

Example curl request
--------------------

.. code-block:: bash

   curl -X GET http://127.0.0.1:8000/api/articles/ \
     -H "Authorization: Bearer <access_token>"
