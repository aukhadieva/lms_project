from rest_framework import permissions


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, авторизован ли пользователь.
        """
        if obj.email == request.user.email:
            return True
        return False
