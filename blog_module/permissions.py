from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            user = request.user
            return getattr(user, 'author', False) or user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_superuser
