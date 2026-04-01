# News 24/7 Capstone Project

This repository contains the News 24/7 Django capstone project from the previous course level.

## Project structure

```text
news-24-7-capstone/
├── README.md
├── capstone.txt
└── news247_news_capstone_project/
    ├── .env.example
    ├── .gitignore
    ├── Dockerfile
    ├── docs/
    ├── manage.py
    ├── news_portal/
    ├── newsapp/
    ├── requirements.txt
    ├── static/
    └── templates/
```

## What the application does

News 24/7 is a role-based Django news platform with:

- custom users and role-based access
- **Reader**, **Editor**, and **Journalist** roles
- article creation, editing, approval, and publishing workflows
- newsletter management
- REST API endpoints protected with JWT authentication
- email notification logic for approved articles
- SQLite support for quick local testing
- MariaDB support through environment variables

## Prerequisites

Install these before running the project:

- Python **3.12+**
- pip
- Git
- Optional: MariaDB if you want to use MariaDB instead of SQLite
- Optional: Docker Desktop if you want to run the project in a container

## Local setup with virtual environment

Open a terminal in `news247_news_capstone_project/` and run:

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment configuration

Copy the example environment file:

**Windows**
```bash
copy .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

### Default local database

By default, the project uses **SQLite**, so you can run it immediately without setting up MariaDB.

### MariaDB setup

If you want to use MariaDB:

1. Install and start MariaDB.
2. Create a database named `news_capstone`.
3. Open `.env` and set the correct database username, password, host, and port.
4. Set `USE_MARIADB=1`.

## Database setup

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

## Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Running tests

```bash
python manage.py test
```

## Role-based access

The application supports these roles:

- **Reader**: can view approved content.
- **Journalist**: can create and manage their own articles.
- **Editor**: can review and approve pending articles.

## Main features

### Web app
- user registration and login
- dashboard view
- article list and detail pages
- create, update, and delete article flows
- editor review page for pending articles
- newsletter creation and listing

### API
- `POST /api/token/`
- `POST /api/token/refresh/`
- `GET /api/articles/`
- `GET /api/articles/subscribed/`
- `GET /api/articles/<id>/`
- `POST /api/articles/`
- `PUT /api/articles/<id>/`
- `DELETE /api/articles/<id>/`
- `POST /api/articles/<id>/approve/`
- `GET /api/newsletters/`
- `POST /api/approved/`

## Docker

From inside `news247_news_capstone_project/`, run:

```bash
docker build -t news247-capstone .
docker run -p 8000:8000 news247-capstone
```

Then open:

```text
http://127.0.0.1:8000/
```

## Included supporting documentation

The `docs/` folder contains supporting project notes such as:

- requirements
- normalization notes
- ERD source
- API testing checklist
