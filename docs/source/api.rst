API Documentation
=================

Authentication
--------------
- POST /api/token/
- POST /api/token/refresh/

Articles
--------
- GET /api/articles/
- POST /api/articles/
- PUT /api/articles/<id>/
- DELETE /api/articles/<id>/

Example
-------

.. code-block:: bash

   curl -X GET http://127.0.0.1:8000/api/articles/