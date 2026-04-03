Setup Guide
===========

From the project directory, create and activate a virtual environment, install the dependencies, and run migrations.

.. code-block:: powershell

   cd news247_news_capstone_project
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
