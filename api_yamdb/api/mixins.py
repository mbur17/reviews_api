from rest_framework.exceptions import PermissionDenied

from api.utils import rating
from users.models import User


class UpdateDestroyMixin:
    """Миксин для функции удаления и изменения комментария."""

    def perform_update(self, serializer):
        """Функция изменяет комментарий."""
        if (serializer.instance.author != self.request.user and
                self.request.user.role != User.MODERATOR):
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, serializer):
        """Функция удаляет комментарий."""
        if (serializer.author != self.request.user and
                self.request.user.role != User.MODERATOR):
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(serializer)


class UpdateDestroyRatingMixin(UpdateDestroyMixin):
    """Миксин для функции удаления и изменения отзыва."""

    def perform_update(self, serializer):
        """Функция изменяет отзыв и обнавляет рейтинг произведения."""
        super().perform_update(serializer)
        rating(self)

    def perform_destroy(self, serializer):
        """Функция удаляет отзыв и обнавляет рейтинг произведения."""
        super().perform_destroy(serializer)
        rating(self)
