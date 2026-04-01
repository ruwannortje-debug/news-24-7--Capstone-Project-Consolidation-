from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ApprovedArticleLog, Article, CustomUser, Newsletter, Publisher


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
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
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("editors", "journalists")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "approved", "created_at")
    list_filter = ("approved", "publisher")
    search_fields = ("title", "content", "author__username")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    filter_horizontal = ("articles",)


@admin.register(ApprovedArticleLog)
class ApprovedArticleLogAdmin(admin.ModelAdmin):
    list_display = ("title", "author_username", "publisher_name", "approved_at")
