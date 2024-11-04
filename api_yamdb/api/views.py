from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from http import HTTPStatus
from reviews.models import Review, Title, Category, Genre, Title
from .serializers import (
    CommentSerializer, ReviewSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer, TitleGETSerializer
)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from users.permissions import (
    IsModeratorOrAuthorOrReadOnly, IsAdminOrReadOnly
)

User = get_user_model()


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


class CategoryViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для эндпоинта categories/."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для эндпоинта genres/."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинта titles/."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer

