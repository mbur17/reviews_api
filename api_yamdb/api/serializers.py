from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


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
