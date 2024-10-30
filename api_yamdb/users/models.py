from django.contrib.auth.models import AbstractUser
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

    email = models.EmailField(unique=True)
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
