# News 24/7 Capstone Project

This repository contains the **News 24/7 Django Capstone Project**.
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

**News 24/7** is a Django-based news platform that supports multiple user roles and provides both a web interface and REST API.

### Key Features

- Custom user model with role-based access
- Roles: **Reader**, **Journalist**, and **Editor**
- Article lifecycle: create → edit → review → approve → publish
- Newsletter management
- JWT authentication
- Email notifications
- SQLite and MariaDB support
- Docker support

---

## Prerequisites

- Python 3.12+
- pip
- Git

---

## Setup

```
cd news247_news_capstone_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Database

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Run

```
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

---

## API

- POST /api/token/
- GET /api/articles/
- POST /api/articles/
- PUT /api/articles/<id>/
- DELETE /api/articles/<id>/

---

## Sphinx Docs

```
cd docs
.\make.bat html
```

Open:
docs/build/html/index.html
