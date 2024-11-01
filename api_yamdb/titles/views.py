from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from http import HTTPStatus

from .models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)


@api_view(['GET', 'POST', 'DELETE'])
def categories(request, category_slug=None):
    """
    Функция, обрабатывающая запросы к эндпоинтам:
    categories/
    categories/<slug:category_slug>/.
    Обрабатываемые методы: GET, POST, DELETE
    """
    method = request.method
    if method == 'GET':
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)
    elif method == 'POST':
        serializer = CategorySerializer(request.data)
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
    Обрабатываемые методы: GET, POST, DELETE
    """
    method = request.method
    if method == 'GET':
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)
    elif method == 'POST':
        serializer = GenreSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    genre = get_object_or_404(Genre, slug=genre_slug)
    genre.delete()
    return Response(status=HTTPStatus.NO_CONTENT)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def title(request, title_slug=None):
    """
    Функция, обрабатывающая запросы к эндпоинту
    titles/<slug:title_slug>/.
    Обрабатываемые методы: GET, POST, PATCH, DELETE
    """
    method = request.method
    _title = get_object_or_404(Title, slug=title_slug)
    if method == 'GET':
        serializer = TitleSerializer(_title)
        return Response(serializer.data, status=HTTPStatus.OK)
    elif method == 'POST' or method == 'PATCH':
        if method == 'POST':
            serializer = TitleSerializer(request.data)
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


@api_view(['GET'])
def titles(request):
    """
    Функция, обрабатывающая запросы к эндпоинту titles/.
    Обрабатываемые методы: GET
    """
    queryset = Title.objects.all()
    serializer = TitleSerializer(queryset, many=True)
    return Response(serializer.data)
