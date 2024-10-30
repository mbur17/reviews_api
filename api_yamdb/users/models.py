from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    email = models.EmailField(unique=True, blank=False, null=False)
    bio = models.TextField(blank=True)
    role = models.CharField(choices=ROLE_CHOICES, default=USER)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # Свойства для проверки роли:
    # Проверка, является ли пользователь аутентифицированным пользователем.
    @property
    def is_user(self):
        return self.role == self.USER

    # Проверка, является ли пользователь модератором.
    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    # Проверка, является ли пользователь администратором,
    # включая суперпользователя.
    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def clean(self):
        """Запрещаем использовать 'me' в качестве имени пользователя."""
        if self.username.lower() == 'me':
            raise ValidationError(
                'Использовать "me" в качестве username запрещено.'
            )
        super().clean()
