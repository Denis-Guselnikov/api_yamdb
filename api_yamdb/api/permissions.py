from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminOnly(BasePermission):
    """Доступно только для Админа"""
    def has_permission(self, request, view):
        return (request.user.is_admin)


class AdminOrReadOnlyPermission(permissions.BasePermission):
    """Для categories, genres и titles"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))
