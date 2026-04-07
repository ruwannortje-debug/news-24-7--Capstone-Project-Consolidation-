## News 24/7 Capstone Project

This project is a Django-based news platform built as part of the Capstone Project. It demonstrates:
Documentation was generated using Sphinx autodoc for the Django project modules.

-   Django development
-   REST API integration
-   Sphinx documentation
-   Docker containerisation
-   Git version control workflow

------------------------------------------------------------------------

## Features

-   User roles (Reader, Journalist, Editor)
-   Article creation and approval workflow
-   REST API endpoints
-   JWT Authentication
-   Sphinx-generated documentation
-   Docker support

------------------------------------------------------------------------

## Setup (Virtual Environment)

### 1. Clone the repository

    git clone <your-repo-link>
    cd news-24-7-capstone

### 2. Create virtual environment

    python -m venv venv

### 3. Activate environment (Windows)

    venv\Scripts\activate

### 4. Install dependencies

    pip install -r requirements.txt

### 5. Run migrations

    python manage.py migrate

### 6. Run server

    python manage.py runserver

------------------------------------------------------------------------

## Run with Docker

### Build image

    docker build -t news247 .

### Run container

    docker run -p 8000:8000 news247

------------------------------------------------------------------------

## Sphinx Documentation

### Location of generated docs

    docs/build/html/index.html

### To rebuild documentation

    cd docs
    .\make.bat clean
    .\make.bat html

Then open:

    docs/build/html/index.html

------------------------------------------------------------------------

## Project Structure

    news-24-7-capstone/
    │
    ├── news_portal/
    ├── newsapp/
    ├── docs/
    ├── Dockerfile
    ├── requirements.txt
    ├── README.md
    └── capstone.txt

------------------------------------------------------------------------

## Environment Variables

Create a `.env` file:

    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost

------------------------------------------------------------------------

## Notes

-   Do NOT commit secrets to GitHub
-   Documentation is generated using Sphinx and autodoc
-   Docker setup allows easy deployment on other machines

------------------------------------------------------------------------

## Repository Link

See `capstone.txt` for the GitHub repository link.

------------------------------------------------------------------------

## Submission Checklist

-   ✔ requirements.txt included\
-   ✔ Dockerfile working\
-   ✔ Sphinx docs generated\
-   ✔ README with full instructions\
-   ✔ capstone.txt included
