import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../news247_news_capstone_project'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_portal.settings'
django.setup()

project = 'News 24/7'
copyright = '2026, Ruwan Nortje'
author = 'Ruwan Nortje'
release = '2026-04-02'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
