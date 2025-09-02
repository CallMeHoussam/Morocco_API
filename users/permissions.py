from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Read for anyone, write only for owners of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

class IsProfileOwner(permissions.BasePermission):
    """
    Only allow users to access their own profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user