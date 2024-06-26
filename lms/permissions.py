from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Проверяет права принадлежность пользователя к группе 'moderator'.
        """
        return request.user.groups.filter(name='moderator').exists()
