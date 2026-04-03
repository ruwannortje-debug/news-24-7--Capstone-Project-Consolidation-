"""Application configuration for the News 24/7 app."""

from django.apps import AppConfig


class NewsappConfig(AppConfig):
    """Configure the Django app and load signal handlers on startup."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "newsapp"

    def ready(self) -> None:
        """Import signal handlers when the application starts."""
        import newsapp.signals  # noqa: F401
