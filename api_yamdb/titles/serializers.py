from rest_framework.serializers import ModelSerializer

from .models import Genre, Category, Title


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class TitleSerializer(ModelSerializer):
    genre = GenreSerializer(required=True, many=True)
    category = CategorySerializer(reuired=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            # 'rating',
            'description',
            'genre',
            'category',
        )
