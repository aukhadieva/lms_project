from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Проверяет принадлежность пользователя к группе 'moderator'.
        """
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, является ли пользователь - владельцем курса/ урока.
        """
        if obj.owner == request.user:
            return True
        return False
