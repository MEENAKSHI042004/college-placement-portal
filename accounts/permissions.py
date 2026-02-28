from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allows access only to Admin/TPO users."""
    message = "Admin access required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsStudent(BasePermission):
    """Allows access only to Student users."""
    message = "Student access required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsAdminOrReadOnly(BasePermission):
    """Admins get full access; students get read-only."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_admin