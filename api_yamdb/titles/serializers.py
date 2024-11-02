from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField, SerializerMethodField
)
from django.db.models import Sum

from .models import Genre, Category, Title
from reviews.models import Review


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
