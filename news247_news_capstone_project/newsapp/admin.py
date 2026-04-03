"""Admin registrations for News 24/7 models."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ApprovedArticleLog, Article, CustomUser, Newsletter, Publisher


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Customize admin display for application users."""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Role and subscriptions",
            {
                "fields": (
                    "role",
                    "subscribed_publishers",
                    "subscribed_journalists",
                )
            },
        ),
    )
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Admin configuration for publishers."""

    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("editors", "journalists")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for news articles."""

    list_display = ("title", "author", "publisher", "approved", "created_at")
    list_filter = ("approved", "publisher")
    search_fields = ("title", "content", "author__username")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin configuration for newsletters."""

    list_display = ("title", "author", "created_at")
    filter_horizontal = ("articles",)


@admin.register(ApprovedArticleLog)
class ApprovedArticleLogAdmin(admin.ModelAdmin):
    """Admin configuration for approval log entries."""

    list_display = ("title", "author_username", "publisher_name", "approved_at")
