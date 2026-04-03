"""Custom permission helpers used by the web and API layers."""

from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


def user_in_group(user, group_name: str) -> bool:
    """Return whether the authenticated user belongs to the named group."""
    return bool(getattr(user, "is_authenticated", False) and user.groups.filter(name=group_name).exists())


def is_effective_editor(user) -> bool:
    """Return whether a user should be treated as an editor."""
    return bool(
        getattr(user, "is_authenticated", False)
        and (getattr(user, "role", None) == "editor" or user_in_group(user, "Editor"))
    )


def is_effective_journalist(user) -> bool:
    """Return whether a user should be treated as a journalist."""
    return bool(
        getattr(user, "is_authenticated", False)
        and (getattr(user, "role", None) == "journalist" or user_in_group(user, "Journalist"))
    )


class IsJournalist(BasePermission):
    """Allow access only to effective journalists."""

    def has_permission(self, request, view):
        """Return True when the request user is a journalist."""
        return is_effective_journalist(request.user)


class IsEditor(BasePermission):
    """Allow access only to effective editors."""

    def has_permission(self, request, view):
        """Return True when the request user is an editor."""
        return is_effective_editor(request.user)


class IsEditorOrJournalist(BasePermission):
    """Allow access to editors and journalists."""

    def has_permission(self, request, view):
        """Return True when the request user is an editor or journalist."""
        return is_effective_editor(request.user) or is_effective_journalist(request.user)
