from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission for users view to allow edit if user is accessing his own profile else set to read only.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous:
            if request.user == obj:
                return True
        return False
