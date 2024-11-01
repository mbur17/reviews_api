from django.urls import path

from .views import SignupView, TokenView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenView.as_view(), name='token_obtain'),
]
