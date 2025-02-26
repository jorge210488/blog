from rest_framework.permissions import BasePermission


class IsAdminUserOnly(BasePermission):
    """
    Permiso que permite solo a usuarios con rol 'admin' acceder a la vista.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
