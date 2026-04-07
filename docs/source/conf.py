"""Sphinx configuration for the News 24/7 project documentation."""

import os
import sys
from pathlib import Path

import django
from django.core.management import call_command

PROJECT_ROOT = Path(__file__).resolve().parents[2] / "news247_news_capstone_project"
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_portal.settings")
django.setup()

# Ensure database-backed model introspection works during autodoc builds.
call_command("migrate", run_syncdb=True, verbosity=0)

project = 'News 24/7'
copyright = '2026, Ruwan Nortje'
author = 'Ruwan Nortje'
release = '2026-04-02'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'show-inheritance': True,
    'exclude-members': 'objects,DoesNotExist,MultipleObjectsReturned,reader_publishers,reader_journalists,independent_articles,independent_newsletters',
}

autoclass_content = 'both'
napoleon_google_docstring = False
napoleon_numpy_docstring = False
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'alabaster'
html_static_path = ['_static']
