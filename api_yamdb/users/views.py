from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .serializers import (
    SignupSerializer, TokenSerializer, UserSerializer, MeSerializer
)

User = get_user_model()


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'user' in serializer.validated_data:
            return Response(
                {'detail': serializer.validated_data['detail']},
                status=status.HTTP_200_OK
            )
        user = serializer.save()
        return Response(
            {'username': user.username, 'email': user.email},
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MeSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
