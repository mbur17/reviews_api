from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignupView, TokenView, UserViewSet, UserMeView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

auth_patterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenView.as_view(), name='token_obtain'),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('users/me/', UserMeView.as_view(), name='user-me'),
    path('', include(router.urls)),
]
