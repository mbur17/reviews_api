from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from reviews.models import Review, Title, Category, Genre
from users.permissions import (
    IsModeratorOrAuthorOrReadOnly, IsAdminOrReadOnly
)
from api.mixins import UpdateMixin
from .serializers import (
    CommentSerializer, ReviewSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer, TitleGETSerializer
)
from .filters import TitleFilter, CategoryFilter, GenreFilter

User = get_user_model()


class ReviewViewSet(UpdateMixin, viewsets.ModelViewSet):
    """Вьюсет для эндпоинта reviews/."""

    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorOrAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        author = self.request.user
        title = self.get_title()
        if Review.objects.filter(author=author, title=title):
            raise ParseError('Разрешается только 1 отзыв на произведение')
        serializer.save(
            author=author,
            title=title)


class CommentViewSet(UpdateMixin, viewsets.ModelViewSet):
    """Вьюсет для эндпоинта comments/."""

    serializer_class = CommentSerializer
    permission_classes = (IsModeratorOrAuthorOrReadOnly, permissions.
                          IsAuthenticatedOrReadOnly)

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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CategoryFilter
    lookup_url_kwarg = 'slug'

    def destroy(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        obj = get_object_or_404(Category, slug=slug)
        obj.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class GenreViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для эндпоинта genres/."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = GenreFilter
    lookup_url_kwarg = 'slug'

    def destroy(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        obj = get_object_or_404(Genre, slug=slug)
        obj.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинта titles/."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer

    def update(self, request, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        name_length = len(request.data.get('name'))
        if name_length > 256:
            raise ValidationError(
                'Название произведения не может быть длиннее 256 символов.'
            )

        title = get_object_or_404(Title, pk=kwargs.get('pk'))
        serializer = TitleSerializer(title, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
