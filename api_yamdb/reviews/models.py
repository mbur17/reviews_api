from datetime import datetime

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import (
    Model, CASCADE, ManyToManyField, ForeignKey,
    CharField, SlugField, IntegerField, TextField, SET_NULL,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(Model):
    """Класс Категории."""
    name = CharField(max_length=256, verbose_name='Название', db_index=True)
    slug = SlugField(
        max_length=50, verbose_name='slug', unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Слаг содержит недопустимый символ'
            )
        ]
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(Model):
    """Класс жанра."""

    name = CharField(max_length=256, verbose_name='Hазвание', db_index=True)
    slug = SlugField(
        max_length=50, verbose_name='slug', unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Слаг содержит недопустимый символ'
            )
        ]
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(Model):
    """Класс произведения."""
    name = CharField(
        max_length=256, verbose_name='Название', db_index=True,

    )
    year = IntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(0, 'Значение не может быть меньше 0'),
            MaxValueValidator(
                datetime.now().year,
                message=f'Значение не может быть больше '
                        f'{datetime.now().year}')
        ],
        db_index=True
    )
    description = TextField(verbose_name='Описание', blank=True)
    genre = ManyToManyField(
        Genre, through='GenreTitle',
        related_name='titles', verbose_name='Жанр'
    )
    category = ForeignKey(
        Category, on_delete=SET_NULL,
        related_name='titles', verbose_name='Категория', null=True
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')


class GenreTitle(Model):
    """Вспомогательный класс, связывающий Genre и Title."""
    genre = ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
    title = ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='произведение'
    )


class Review(models.Model):
    """Класс отзыва."""
    text = models.TextField(blank=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.IntegerField(blank=True, null=True)
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review'),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс комментария."""
    text = models.TextField(blank=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text
