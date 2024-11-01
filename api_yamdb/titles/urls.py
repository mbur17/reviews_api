from django.urls import path

from .views import (
    categories, genres, titles, title
)

urlpatterns = [
    path('categories/<slug:category_slug>/', categories),
    path('genres/<slug:genre_slug>/', genres),
    path('titles/<slug:title_slug>/', title),
    path('titles/', titles),
]
