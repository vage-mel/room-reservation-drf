from rest_framework import permissions


class IsOwnerOrIsStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (obj.id == request.user.id or request.user.is_staff)
