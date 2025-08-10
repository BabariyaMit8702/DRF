from rest_framework.permissions import BasePermission,SAFE_METHODS

class Isonwerorreadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS):
            return True
        if obj.author_id == request.user:
            return True