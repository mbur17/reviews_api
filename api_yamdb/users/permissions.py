from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Полный доступ администраторам."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    """Доступ администраторам, анонимам на чтение"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_staff
        )


class IsModeratorOrAdminOrAuthorOrReadOnly(BasePermission):
    """
    Право на редактирование и удаление для модераторов,
    администраторов и владельцев контента.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user.is_moderator or obj.author == request.user
                or request.user.is_staff
            ))
