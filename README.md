# News 24/7 Capstone Project

This repository contains the News 24/7 Django Capstone Project.

---

## Project Structure

```
news-24-7-capstone/
├── README.md
├── capstone.txt
├── docs/
└── news247_news_capstone_project/
    ├── .env.example
    ├── Dockerfile
    ├── manage.py
    ├── news_portal/
    ├── newsapp/
    ├── requirements.txt
    ├── static/
    └── templates/
```

---

## Project Overview

News 24/7 is a Django-based news platform that supports multiple user roles and provides both a web interface and REST API.

### Key Features

- Custom user model with role-based access
- Roles: Reader, Journalist, and Editor
- Article lifecycle: create, edit, review, approve, and publish
- Newsletter management
- JWT authentication for API security
- Email notifications for approved articles
- SQLite (default) and MariaDB support
- Docker support

---

## Prerequisites

- Python 3.12+
- pip
- Git

---

## Local Setup

Navigate to the project folder:

```powershell
cd news247_news_capstone_project
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the environment (Windows):

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Database Setup

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Run the Application

```powershell
python manage.py runserver
```

Open in browser:

```text
http://127.0.0.1:8000/
```

---

## API Endpoints

All API endpoints require authentication using a JWT access token unless stated otherwise.

### Authentication
- POST /api/token/

### Articles
- GET /api/articles/
- POST /api/articles/
- GET /api/articles/<id>/
- PUT /api/articles/<id>/
- DELETE /api/articles/<id>/

### Example request

```json
{
  "title": "Example Article",
  "content": "Article content",
  "summary": "Short summary"
}
```

### Example curl

```bash
curl -X GET http://127.0.0.1:8000/api/articles/
```

Authentication header:

```text
Authorization: Bearer <access_token>
```

---

## Sphinx Documentation

The project includes Sphinx-generated documentation in the top-level docs folder.

To rebuild the documentation:

```powershell
cd docs
.\make.bat html
```

The generated HTML entry point is:

```text
docs/build/html/index.html
```

Open this file in your browser to view the documentation.
