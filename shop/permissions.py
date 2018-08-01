from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_active


class DocTypePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.available_types is not None

    def has_object_permission(self, request, view, obj):
        available_types = request.user.available_types
        if available_types is None or obj.doc_type_id not in list(available_types):
            return False
        return True
