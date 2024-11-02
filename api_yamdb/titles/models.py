from django.db.models import (
    Model, CASCADE,
    CharField, IntegerField, TextField, SlugField, ManyToManyField,
    ForeignKey
)


class Genre(Model):
    """Модель жанра."""
    name = CharField(max_length=256)
    slug = SlugField(max_length=50)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(Model):
    """Модель категории."""
    name = CharField(max_length=256)
    slug = SlugField(max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Title(Model):
    """Модель произведения."""
    name = CharField(max_length=256)
    year = IntegerField()
    description = TextField(null=True)
    genre = ManyToManyField(to=Genre, through='TitleGenre')
    category = ForeignKey(to=Category, related_name='title', on_delete=CASCADE)


class TitleGenre(Model):
    """Модель для связи Title и Genre."""
    title = ForeignKey(Title, on_delete=CASCADE)
    genre = ForeignKey(Genre, on_delete=CASCADE)
