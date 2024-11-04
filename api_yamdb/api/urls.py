from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet, ReviewViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet
)


router = DefaultRouter()

router.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
]
