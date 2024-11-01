from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from .models import Genre, Category, Title


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class TitleSerializer(ModelSerializer):
    """Сериализатор для модели Title."""
    genre = GenreSerializer(required=True, many=True)
    category = CategorySerializer(required=True)
    rating = IntegerField(blank=True, default=0)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
