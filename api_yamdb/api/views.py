from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title
from users.permissions import IsModeratorOrAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorOrAuthorOrReadOnly,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title())
        self.rating()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.rating()

    def perform_destroy(self, serializer):
        super().perform_destroy(serializer)
        self.rating()

    def rating(self):
        """Функция высчитывает и записывает среднюю оценку произведения"""
        title = self.get_title()
        average_rating = Review.objects.filter(
            title=title).aggregate(avg=Avg('score'))['avg']
        if average_rating is not None:
            average_rating = round(average_rating)
        title.rating = average_rating
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorOrAuthorOrReadOnly,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review())
