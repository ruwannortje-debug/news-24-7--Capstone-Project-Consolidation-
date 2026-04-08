# News 24/7 Capstone Project

News 24/7 is a Django-based news platform built for the capstone.
It demonstrates Django development, role-based access control, REST API usage,
Sphinx documentation, Docker containerisation, and Git workflow.

## Features

- Role-based access for Readers, Journalists, and Editors
- Article drafting, editing, and approval workflow
- Newsletter support
- JWT authentication for API access
- Sphinx documentation generated from project docstrings
- Docker support for local containerised runs

## Repository layout

```text
news-24-7--Capstone-Project-Consolidation-/
├── README.md
├── capstone.txt
├── docs/                              # Sphinx project + generated HTML docs
└── news247_news_capstone_project/     # Django application source
    ├── manage.py
    ├── requirements.txt
    ├── Dockerfile
    ├── news_portal/
    ├── newsapp/
    ├── static/
    └── templates/
```

## Run the project with a virtual environment

### 1. Clone the repository

```bash
git clone https://github.com/ruwannortje-debug/news-24-7--Capstone-Project-Consolidation-.git
cd news-24-7--Capstone-Project-Consolidation-
cd news247_news_capstone_project
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run migrations

```powershell
python manage.py migrate
```

### 5. Start the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Run with Docker

Run these commands from the `news247_news_capstone_project` folder.

### Build the image

```powershell
docker build -t news247 .
```

### Run the container

```powershell
docker run -p 8000:8000 news247
```

Then open `http://127.0.0.1:8000/` in your browser.

## Sphinx documentation

The Sphinx documentation project is stored in the top-level `docs` folder.
Generated HTML output is included in this submission.

### Rebuild the docs

From the repository root:

```powershell
cd docs
.\make.bat clean
.\make.bat html
```

Then open:

```text
docs\build\html\index.html
```

## Environment variables

Create a `.env` file inside `news247_news_capstone_project` if needed.

```text
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

A sample file is also included as `.env.example` in the Django project folder.

## Notes

- Do not commit secrets such as passwords or tokens.
- Generated Sphinx HTML docs are intentionally included for reviewer access.
- The GitHub repository link required for submission is included in `capstone.txt`.
