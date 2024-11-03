from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField, SerializerMethodField
)
from django.db.models import Sum
from datetime import datetime

from reviews.models import Comment, Review, Genre, Category, Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['author, title'],
            message='Разрешается остаиоть только 1 отзыв'
        ),]

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
    rating = SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'rating',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        """Вычисляет значение поля rating."""
        queryset = Review.objects.filter(title=obj.id)
        if not queryset:
            return 0
        summary = queryset.aggregate(
            total_score=Sum('score')
        )['total_score'] or 0
        reviews_count = queryset.count()
        return summary / reviews_count

    def validate_year(self, value):
        """Проверяет валидность поля year."""
        return datetime.now().year >= value
