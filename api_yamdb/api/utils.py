from django.db.models import Avg

from reviews.models import Review


def rating(self):
    """Функция высчитывает и записывает среднюю оценку произведения"""
    title = self.get_title()
    average_rating = Review.objects.filter(
            title=title).aggregate(avg=Avg('score'))
    title.rating = round(average_rating['avg'])
    title.save()
