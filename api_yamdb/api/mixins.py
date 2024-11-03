from rest_framework.exceptions import PermissionDenied

from users.models import User
from .utils import rating


class UpdateDestroyMixin:
    """Миксин для функции удаления и изменения обЪекта."""

    def perform_update(self, serializer):
        """Функция изменяет объект ."""
        if (serializer.instance.author != self.request.user and
                self.request.user.role != User.MODERATOR):
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)
        rating(self)

    def perform_destroy(self, serializer):
        """Функция удаляет объект."""
        if (serializer.author != self.request.user and
                self.request.user.role != User.MODERATOR):
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(serializer)
        rating(self)
