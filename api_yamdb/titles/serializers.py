from rest_framework.serializers import ModelSerializer, SlugRelatedField

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
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )