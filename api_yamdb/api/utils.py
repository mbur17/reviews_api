from django.db.models import Avg

from reviews.models import Review


def rating(self):
    title = self.get_title()
    average_rating = Review.objects.filter(
            title=title.id).aggregate(avg=Avg('core'))
    title.rating = average_rating
    title.save()
