from django_filters.rest_framework import (
    CharFilter, FilterSet, NumberFilter
)

from reviews.models import Category, Genre, Title


class CategoryFilter(FilterSet):
    """Класс для фильтрации категорий."""
    search = CharFilter(field_name='name', lookup_expr='exact')

    class Meta:
        model = Category
        fields = ('search', )


class GenreFilter(FilterSet):
    """Класс для фильтрации жанров."""
    search = CharFilter(field_name='name', lookup_expr='exact')

    class Meta:
        model = Genre
        fields = ('name', )


class TitleFilter(FilterSet):
    """Класс для фильтрации произведений."""
    category = CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='contains')
    year = NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year', )
