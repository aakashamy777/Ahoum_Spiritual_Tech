from rest_framework import permissions

class IsCreator(permissions.BasePermission):
    """
    Allows access only to users with the 'creator' role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'creator')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user
