from rest_framework.permissions import BasePermission


class IsInEditorsGroup(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='IsEditor').exists()
