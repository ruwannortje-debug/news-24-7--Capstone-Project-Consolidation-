from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """Application user with role-based access and optional subscriptions."""

    ROLE_READER = "reader"
    ROLE_EDITOR = "editor"
    ROLE_JOURNALIST = "journalist"
    ROLE_CHOICES = (
        (ROLE_READER, "Reader"),
        (ROLE_EDITOR, "Editor"),
        (ROLE_JOURNALIST, "Journalist"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_READER)
    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        blank=True,
        related_name="subscribers",
    )
    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="reader_subscribers",
        limit_choices_to={"role": ROLE_JOURNALIST},
    )

    def clean(self) -> None:
        super().clean()
        if self.pk and self.role != self.ROLE_READER and (
            self.subscribed_publishers.exists() or self.subscribed_journalists.exists()
        ):
            raise ValidationError(
                "Only readers can hold subscriptions to publishers or journalists."
            )

    def save(self, *args, **kwargs):
        """Persist the user and clear role-incompatible relationship fields.

        The brief asks for reader-only subscription fields to be effectively absent for
        journalists and journalist-specific publication relations to be absent for
        readers. In Django, reverse relations cannot literally be set to None, so this
        method keeps the stored data equivalent by clearing reader subscriptions for all
        non-reader roles. The journalist publication fields remain reverse relations and
        naturally resolve to empty querysets for non-journalists.
        """
        super().save(*args, **kwargs)
        if self.role != self.ROLE_READER:
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()

    @property
    def is_reader(self) -> bool:
        return self.role == self.ROLE_READER

    @property
    def is_editor(self) -> bool:
        return self.role == self.ROLE_EDITOR

    @property
    def is_journalist(self) -> bool:
        return self.role == self.ROLE_JOURNALIST


class Publisher(models.Model):
    """News publisher with assigned editors and journalists."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="editor_publishers",
        blank=True,
        limit_choices_to={"role": CustomUser.ROLE_EDITOR},
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="journalist_publishers",
        blank=True,
        limit_choices_to={"role": CustomUser.ROLE_JOURNALIST},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Article(models.Model):
    """News article submitted by a journalist and optionally tied to a publisher."""

    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=280, blank=True)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
        limit_choices_to={"role": CustomUser.ROLE_JOURNALIST},
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_articles",
        limit_choices_to={"role": CustomUser.ROLE_EDITOR},
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("can_approve_article", "Can approve article"),
        ]

    def clean(self) -> None:
        super().clean()
        if self.author_id is None:
            return
        if self.author.role != CustomUser.ROLE_JOURNALIST:
            raise ValidationError("Only journalists can author articles.")

    def mark_approved(self, editor: CustomUser) -> None:
        """Approve the article and store approval metadata."""
        self.approved = True
        self.approved_by = editor
        self.approved_at = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.title


class Newsletter(models.Model):
    """Curated collection of articles created by journalists or editors."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="newsletters",
        limit_choices_to={"role__in": [CustomUser.ROLE_JOURNALIST, CustomUser.ROLE_EDITOR]},
    )
    articles = models.ManyToManyField(Article, related_name="newsletters", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class ApprovedArticleLog(models.Model):
    """Internal API log for approved article events."""

    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="approval_log")
    title = models.CharField(max_length=255)
    author_username = models.CharField(max_length=150)
    publisher_name = models.CharField(max_length=255, blank=True)
    approved_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-approved_at"]

    def __str__(self) -> str:
        return f"Approved article log: {self.title}"


# Role-specific convenience accessors used by documentation and templates.
CustomUser.reader_publishers = property(lambda self: self.subscribed_publishers if self.role == CustomUser.ROLE_READER else None)
CustomUser.reader_journalists = property(lambda self: self.subscribed_journalists if self.role == CustomUser.ROLE_READER else None)
CustomUser.independent_articles = property(lambda self: self.articles if self.role == CustomUser.ROLE_JOURNALIST else None)
CustomUser.independent_newsletters = property(lambda self: self.newsletters if self.role == CustomUser.ROLE_JOURNALIST else None)
