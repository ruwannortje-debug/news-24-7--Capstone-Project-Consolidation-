API Guide
=========

Authentication
--------------

- ``POST /api/token/`` obtains a JWT access and refresh token.
- ``POST /api/token/refresh/`` refreshes an access token.

Articles
--------

- ``GET /api/articles/`` lists approved articles.
- ``POST /api/articles/`` creates an article for an authenticated journalist.
- ``GET /api/articles/<id>/`` returns a single article.
- ``PUT /api/articles/<id>/`` updates an article.
- ``DELETE /api/articles/<id>/`` deletes an article.
- ``POST /api/articles/<id>/approve/`` approves an article as an editor.
- ``GET /api/articles/subscribed/`` lists approved articles from subscriptions.

Newsletters
-----------

- ``GET /api/newsletters/`` lists newsletters and their linked articles.

Approved article log
--------------------

- ``POST /api/approved/`` creates or updates the approval log record used by
  the internal notification flow.

Example request
---------------

.. code-block:: bash

   curl -X GET http://127.0.0.1:8000/api/articles/      -H "Authorization: Bearer <access_token>"
