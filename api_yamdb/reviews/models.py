from django.contrib.auth import get_user_model
from django.db import models
<<<<<<< HEAD
from django.db.models import (
    Model, CASCADE, ManyToManyField, ForeignKey,
    CharField, SlugField, IntegerField, TextField,
)
=======
from django.contrib.auth import get_user_model


User = get_user_model()
>>>>>>> cfe172e02b541d814fbd51e58e5da65576d2e030


User = get_user_model()


<<<<<<< HEAD
class Genre(Model):
    """Модель жанра."""
    name = CharField(max_length=256, verbose_name='Название')
    slug = SlugField(max_length=50, verbose_name='Слаг')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(Model):
    """Модель категории."""
    name = CharField(max_length=256, verbose_name='Название')
    slug = SlugField(max_length=50, verbose_name='Слаг')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Title(Model):
    """Модель произведения."""
    name = CharField(max_length=256, verbose_name='Название')
    year = IntegerField(verbose_name='Год')
    description = TextField(null=True, verbose_name='Описание')
    genre = ManyToManyField(
        to=Genre, through='TitleGenre', verbose_name='Жанр'
    )
    category = ForeignKey(
        to=Category, related_name='title',
        on_delete=CASCADE, verbose_name='Категория'
    )


class TitleGenre(Model):
    """Модель для связи Title и Genre."""
    title = ForeignKey(Title, on_delete=CASCADE)
    genre = ForeignKey(Genre, on_delete=CASCADE)


=======
>>>>>>> cfe172e02b541d814fbd51e58e5da65576d2e030
class Review(models.Model):
    text = models.TextField(blank=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
<<<<<<< HEAD
    score = models.IntegerField(blank=False)
=======
    score = models.IntegerField(blank=True, null=True)
>>>>>>> cfe172e02b541d814fbd51e58e5da65576d2e030
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
