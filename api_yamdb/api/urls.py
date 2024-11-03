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
    path('v1/categories/<slug:category_slug>/', categories),
    path('v1/genres/<slug:genre_slug>/', genres),
    path('v1/titles/', titles),
    path('v1/titles/<slug:title_slug>/', title),
]
