from rest_framework import permissions


class IsTaskListCreatorOrNone(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.created_by:
            return True
        return False


class IsAllowedToEditTaskOrNone(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.house == obj.tasklist.house:
            return True
        return False


class IsAllowedToEditAttachmentOrNone(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            if request.user.house == obj.task.tasklist.house:
                return True
        return False
