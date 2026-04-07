"""Root URL configuration for the News 24/7 project.

The application routes the Django admin to ``/admin/`` and mounts the web and
API routes from ``newsapp.urls`` at the site root.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("newsapp.urls")),
]
