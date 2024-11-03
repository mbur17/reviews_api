from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from http import HTTPStatus

from .mixins import UpdateDestroyMixin
from .utils import rating
from reviews.models import Review, Title, Category, Genre, Title
from .serializers import (
    CommentSerializer, ReviewSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer
)

User = get_user_model()


class ReviewViewSet(UpdateDestroyMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
        rating(self)


class CommentViewSet(UpdateDestroyMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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


@api_view(['GET', 'POST', 'DELETE'])
def categories(request, category_slug=None):
    """
    Функция, обрабатывающая запросы к эндпоинту:
    categories/<slug:category_slug>/.
    Обрабатываемые методы:
    - GET: Получение списка всех категорий(Без токена)
    - POST: Добавление новой категории(Администратор)
    - DELETE: Удаление категории(Администратор)
    """
    method = request.method
    if method == 'GET':
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)
    elif method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    category = get_object_or_404(Category, slug=category_slug)
    category.delete()
    return Response(status=HTTPStatus.NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
def genres(request, genre_slug=None):
    """
    Функция, обрабатывающая запросы к эндпоинту
    genres/<slug:genre_slug>/.
    Обрабатываемые методы:
    - GET: Получение Списка всех жанров(Без токена)
    - POST: Добавить жанр(Администратор)
    - DELETE: Удаление жанра(Администратор).
    """
    method = request.method
    if method == 'GET':
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)
    elif method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    genre = get_object_or_404(Genre, slug=genre_slug)
    genre.delete()
    return Response(status=HTTPStatus.NO_CONTENT)


@api_view(['GET', 'PATCH', 'DELETE'])
def title(request, title_slug):
    """
    Функция, обрабатывающая запросы к эндпоинту
    titles/<slug:title_slug>/.
    Обрабатываемые методы:
    - GET: Получение произведения(Без токена)
    - PATCH: Частичное обновление информации о произведении(Администратор)
    - DELETE: Удаление произведения(Администратор).
    """
    method = request.method
    _title = get_object_or_404(Title, slug=title_slug)
    if method == 'GET':
        serializer = TitleSerializer(_title)
        return Response(serializer.data, status=HTTPStatus.OK)
    elif method == 'POST' or method == 'PATCH':
        if method == 'POST':
            serializer = TitleSerializer(data=request.data)
        else:
            serializer = TitleSerializer(
                _title, data=request.data, partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    _title.delete()
    return Response(status=HTTPStatus.NO_CONTENT)


@api_view(['GET', 'POST'])
def titles(request):
    """
    Функция, обрабатывающая запросы к эндпоинту titles/.
    Обрабатываемые методы:
    - GET: Получение списка всех произведений(Без токена)
    - POST: Добавление произведения(Администратор).
    """
    if request.method == 'POST':
        serializer = TitleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    queryset = Title.objects.all()
    serializer = TitleSerializer(queryset, many=True)
    return Response(serializer.data)

