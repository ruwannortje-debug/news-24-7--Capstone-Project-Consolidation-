from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


def user_in_group(user, group_name: str) -> bool:
    """Return True when the authenticated user belongs to the given group."""
    return bool(getattr(user, "is_authenticated", False) and user.groups.filter(name=group_name).exists())


def is_effective_editor(user) -> bool:
    """Allow editor access by role or Editor group membership."""
    return bool(
        getattr(user, "is_authenticated", False)
        and (getattr(user, "role", None) == "editor" or user_in_group(user, "Editor"))
    )


def is_effective_journalist(user) -> bool:
    """Allow journalist access by role or Journalist group membership."""
    return bool(
        getattr(user, "is_authenticated", False)
        and (getattr(user, "role", None) == "journalist" or user_in_group(user, "Journalist"))
    )


class IsJournalist(BasePermission):
    def has_permission(self, request, view):
        return is_effective_journalist(request.user)


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return is_effective_editor(request.user)


class IsEditorOrJournalist(BasePermission):
    def has_permission(self, request, view):
        return is_effective_editor(request.user) or is_effective_journalist(request.user)
