from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    """Полный доступ администраторам."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_staff
        )


class IsModeratorOrAuthorOrReadOnly(BasePermission):
    """
    Право на редактирование и удаление для модераторов и владельцев контента.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user.is_moderator or obj.author == request.user
            )
        )
