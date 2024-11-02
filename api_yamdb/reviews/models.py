from django.db import models
from users.models import User


class Title(models.Model):
    ...


class Category(models.Model):
    ...


class Genre(models.Model):
    ...


class Review(models.Model):
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
