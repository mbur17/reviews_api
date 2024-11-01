from django.db.models import (
    Model, CASCADE,
    CharField, IntegerField, TextField, SlugField, ManyToManyField, ForeignKey
)


class Genre(Model):
    name = CharField(max_length=256)
    slug = SlugField(max_length=50)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(Model):
    name = CharField(max_length=256)
    slug = SlugField(max_length=50)
    title = ForeignKey(to='Title', related_name='category', on_delete=CASCADE)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Title(Model):
    name = CharField(max_length=256)
    year = IntegerField()
    description = TextField(null=True)
    genre = ManyToManyField(to=Genre, through='TitleGenre')
