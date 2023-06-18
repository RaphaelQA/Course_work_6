# TODO здесь производится настройка пермишенов для нашего проекта
from rest_framework.permissions import BasePermission

from users.models import UserRoles


class AdAdminPermission(BasePermission):
    message = "You must be a SITE ADMINISTRATOR"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.ADMIN:
            return True
        return False


class IsExecutor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
