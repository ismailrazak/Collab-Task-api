from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsHouseManagerOrNone(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous:
            if request.user == obj.manager:
                return True
            return False
