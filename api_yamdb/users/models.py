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
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default=USER)
    # Поле для хранения кода подтверждения
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # Проверка, является ли пользователь модератором
    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def clean(self):
        """Запрещаем использовать 'me' в качестве имени пользователя."""
        if self.username.lower() == 'me':
            raise ValidationError(
                'Использовать "me" в качестве username запрещено.'
            )
        super().clean()

    def save(self, *args, **kwargs):
        # Если суперпользователь, автоматически присваивается роль ADMIN.
        self.role = self.ADMIN if self.is_superuser else self.role
        # Для роли ADMIN устанавливаем is_staff в True.
        self.is_staff = self.role == self.ADMIN
        super().save(*args, **kwargs)
