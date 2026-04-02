Setup Guide
===========

Steps
-----

.. code-block:: powershell

   python -m venv venv
   venv\Scripts\activate
   pip install -r ..\news247_news_capstone_project\requirements.txt
   python ..\news247_news_capstone_project\manage.py migrate
   python ..\news247_news_capstone_project\manage.py runserver