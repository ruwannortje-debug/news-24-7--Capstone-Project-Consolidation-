Setup Guide
===========

The project should be run from the ``news247_news_capstone_project`` folder.
The commands below follow the same Sphinx workflow described in the supplied
HyperionDev documentation PDF.

Run the application
-------------------

.. code-block:: powershell

   cd news247_news_capstone_project
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

Build the documentation
-----------------------

.. code-block:: powershell

   cd ..\docs
   .\make.bat clean
   .\make.bat html

Open ``docs\build\html\index.html`` in a browser to view the generated
project documentation.
