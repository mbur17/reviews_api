from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField, IntegerField
)

from reviews.models import Comment, Review, Genre, Category, Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise ParseError('Рейтинг должен быть от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        model = Comment


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


class TitleGETSerializer:
    """Сериализатор для GET запросов."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


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
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def to_representation(self, instance):
        serializer = TitleGETSerializer(instance)
        return serializer.data
