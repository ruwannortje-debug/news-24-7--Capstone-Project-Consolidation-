"""Signal handlers and startup helpers for the News 24/7 application.

This module keeps Django groups in sync with application roles, assigns
permissions after migrations, emails subscribers when an article is approved,
and posts approved-article events to the internal API log endpoint.
"""

from __future__ import annotations

import requests
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import ApprovedArticleLog, Article, Newsletter

User = get_user_model()

ROLE_TO_GROUP = {
    "reader": "Reader",
    "editor": "Editor",
    "journalist": "Journalist",
}


def _set_group_permissions() -> None:
    """Create and assign the expected model permissions to each role group.

    The capstone brief requires a role-based workflow. This helper ensures the
    Reader, Editor, and Journalist groups exist and that each group receives the
    correct model permissions after migrations have completed.
    """
    article_ct = ContentType.objects.get_for_model(Article)
    newsletter_ct = ContentType.objects.get_for_model(Newsletter)
    perms = {
        "view_article": Permission.objects.get(codename="view_article", content_type=article_ct),
        "add_article": Permission.objects.get(codename="add_article", content_type=article_ct),
        "change_article": Permission.objects.get(codename="change_article", content_type=article_ct),
        "delete_article": Permission.objects.get(codename="delete_article", content_type=article_ct),
        "can_approve_article": Permission.objects.get(codename="can_approve_article", content_type=article_ct),
        "view_newsletter": Permission.objects.get(codename="view_newsletter", content_type=newsletter_ct),
        "add_newsletter": Permission.objects.get(codename="add_newsletter", content_type=newsletter_ct),
        "change_newsletter": Permission.objects.get(codename="change_newsletter", content_type=newsletter_ct),
        "delete_newsletter": Permission.objects.get(codename="delete_newsletter", content_type=newsletter_ct),
    }

    reader_group, _ = Group.objects.get_or_create(name="Reader")
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    journalist_group, _ = Group.objects.get_or_create(name="Journalist")

    reader_group.permissions.set([
        perms["view_article"],
        perms["view_newsletter"],
    ])
    editor_group.permissions.set([
        perms["view_article"],
        perms["change_article"],
        perms["delete_article"],
        perms["can_approve_article"],
        perms["view_newsletter"],
        perms["change_newsletter"],
        perms["delete_newsletter"],
    ])
    journalist_group.permissions.set([
        perms["view_article"],
        perms["add_article"],
        perms["change_article"],
        perms["delete_article"],
        perms["view_newsletter"],
        perms["add_newsletter"],
        perms["change_newsletter"],
        perms["delete_newsletter"],
    ])


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs) -> None:
    """Create groups and refresh role permissions after migrations complete."""
    app_config = apps.get_app_config("newsapp")
    create_permissions(app_config, verbosity=0)
    _set_group_permissions()


@receiver(post_save, sender=User)
def assign_group_by_role(sender, instance, created, **kwargs) -> None:
    """Keep the user's Django group aligned with the selected application role.

    :param sender: The user model class that fired the signal.
    :param instance: The saved user instance.
    :param created: Indicates whether the user was created in this save call.
    :return: None
    """
    group_name = ROLE_TO_GROUP.get(instance.role)
    if not group_name:
        return
    group, _ = Group.objects.get_or_create(name=group_name)
    existing = set(instance.groups.values_list("name", flat=True))
    if existing != {group_name}:
        instance.groups.clear()
        instance.groups.add(group)


def _get_approval_recipients(article: Article) -> list[str]:
    """Collect subscriber email addresses for an approved article.

    :param article: The article that has been approved.
    :return: A sorted list of unique recipient email addresses.
    :rtype: list[str]
    """
    recipients: set[str] = set()
    journalist_subscribers = User.objects.filter(
        role=User.ROLE_READER,
        subscribed_journalists=article.author,
    ).exclude(email="")
    recipients.update(journalist_subscribers.values_list("email", flat=True))

    if article.publisher_id:
        publisher_subscribers = User.objects.filter(
            role=User.ROLE_READER,
            subscribed_publishers=article.publisher,
        ).exclude(email="")
        recipients.update(publisher_subscribers.values_list("email", flat=True))
    return sorted(recipients)


@receiver(post_save, sender=Article)
def notify_on_article_approval(sender, instance: Article, created: bool, **kwargs) -> None:
    """Send notifications and create an internal log when an article is approved.

    :param sender: The model class that fired the signal.
    :param instance: The saved article instance.
    :param created: Indicates whether the article was newly created.
    :return: None
    """
    if not instance.approved or instance.approval_notified:
        return

    if not instance.approved_at:
        from django.utils import timezone
        instance.approved_at = timezone.now()
        Article.objects.filter(pk=instance.pk, approved_at__isnull=True).update(approved_at=instance.approved_at)

    recipient_list = _get_approval_recipients(instance)
    if recipient_list:
        send_mail(
            subject=f"Approved article: {instance.title}",
            message=(
                f"{instance.title}\n\n"
                f"Summary: {instance.summary or 'No summary provided.'}\n\n"
                f"{instance.content}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    payload = {
        "article": instance.pk,
        "title": instance.title,
        "author_username": instance.author.username,
        "publisher_name": instance.publisher.name if instance.publisher else "",
        "approved_at": instance.approved_at.isoformat() if instance.approved_at else None,
    }

    try:
        requests.post(
            f"{settings.SITE_BASE_URL.rstrip('/')}/api/approved/",
            json=payload,
            timeout=5,
        )
    except requests.RequestException:
        pass

    Article.objects.filter(pk=instance.pk, approval_notified=False).update(approval_notified=True)
    ApprovedArticleLog.objects.get_or_create(
        article=instance,
        defaults={
            "title": instance.title,
            "author_username": instance.author.username,
            "publisher_name": instance.publisher.name if instance.publisher else "",
            "approved_at": instance.approved_at,
        },
    )
