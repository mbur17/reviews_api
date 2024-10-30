from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(username_validator,),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(blank=True)

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
