# News 24/7 Capstone Project

News 24/7 is a Django-based news platform built for the capstone
project.\
It demonstrates Django development, role-based access control, REST API
usage,\
Sphinx documentation, Docker containerisation, and Git workflow.

------------------------------------------------------------------------

## Features

-   Role-based access for Readers, Journalists, and Editors
-   Article drafting, editing, and approval workflow
-   Newsletter support
-   JWT authentication for API access
-   Sphinx documentation generated from project docstrings
-   Docker support for local containerised runs

------------------------------------------------------------------------

## Repository Layout

    news-24-7--Capstone-Project-Consolidation-/
    ├── README.md
    ├── capstone.txt
    ├── docs/                              # Sphinx project + generated HTML docs
    └── news247_news_capstone_project/     # Django application source
        ├── manage.py
        ├── requirements.txt
        ├── Dockerfile
        ├── .env.example
        ├── news_portal/
        ├── newsapp/
        ├── static/
        └── templates/

------------------------------------------------------------------------

## Run the Project (Virtual Environment)

### 1. Clone the repository

    git clone https://github.com/ruwannortje-debug/news-24-7--Capstone-Project-Consolidation-.git
    cd news-24-7--Capstone-Project-Consolidation-
    cd news247_news_capstone_project

------------------------------------------------------------------------

### 2. Create and activate a virtual environment

    python -m venv venv
    venv\Scripts\activate

------------------------------------------------------------------------

### 3. Install dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

### 4. Configure environment variables

Create a `.env` file from the template:

    copy .env.example .env

Then update the values inside `.env` with your configuration.

------------------------------------------------------------------------

### 5. Create the database (IMPORTANT)

Before running migrations, create your database manually (e.g. MySQL).

Example: - Create a database in MySQL using a tool like MySQL Workbench
or CLI - Ensure your `.env` file contains the correct database
credentials

------------------------------------------------------------------------

### 6. Run migrations

    python manage.py migrate

------------------------------------------------------------------------

### 7. Start the development server

    python manage.py runserver

Open:

    http://127.0.0.1:8000/

------------------------------------------------------------------------

## Run with Docker

Make sure you are inside:

    news247_news_capstone_project

### Build the image

    docker build -t news247 .

### Run the container

    docker run -p 8000:8000 news247

Then open:

    http://127.0.0.1:8000/

------------------------------------------------------------------------

## Sphinx Documentation

The Sphinx documentation project is stored in the top-level `docs`
folder.\
Generated HTML output is included for review.

### Rebuild documentation

From the repository root:

    cd docs
    .\make.bat clean
    .\make.bat html

Then open:

    docs\build\html\index.html

------------------------------------------------------------------------

## Notes

-   Do not commit secrets such as passwords or tokens
-   Generated Sphinx HTML docs are included intentionally for reviewer
    access
-   The GitHub repository link required for submission is included in
    `capstone.txt`
