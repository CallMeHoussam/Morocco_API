from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Read for anyone, write only for owners of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "created_by_id", None) == getattr(request.user, "id", None)
