from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet, ReviewViewSet,
    categories, genres, titles, title
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


urlpatterns = [
    path('v1/', include(router.urls)),
    path('categories/<slug:category_slug>/', categories),
    path('genres/<slug:genre_slug>/', genres),
    path('titles/<slug:title_slug>/', title),

    path('categories/', categories),
    path('genres/', genres),
    path('titles/', titles),
]
