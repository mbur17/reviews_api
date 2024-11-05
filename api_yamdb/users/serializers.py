from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.validators import UniqueValidator


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, value):
        """Запрещаем использование 'me' в качестве username."""
        if value.lower() == 'me':
            raise ValidationError(
                'Использовать "me" в качестве username запрещено.'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        try:
            user = User.objects.get(username=username, email=email)
            self.create_or_update_confirmation_code(user)
            data['user'] = user
            data['detail'] = 'Код подтверждения был отправлен.'
            return data
        except User.DoesNotExist:
            if User.objects.filter(username=username).exists():
                raise ValidationError({
                    'username': 'Пользователь с таким username уже существует.'
                })
            if User.objects.filter(email=email).exists():
                raise ValidationError({
                    'email': 'Пользователь с таким email уже существует.'
                })
        return data

    def create(self, validated_data):
        """Создаём нового пользователя и генерируем код подтверждения."""
        user = User.objects.create(**validated_data)
        self.create_or_update_confirmation_code(user)
        return user

    def create_or_update_confirmation_code(self, user):
        confirmation_code = get_random_string(length=6)
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            subject='Код подтверждения для YaMDB',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False,
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('Пользователь не найден.')
        if user.confirmation_code != confirmation_code:
            raise ValidationError('Неверный код подтверждения.')
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES, required=False, default=User.USER
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        max_length=254,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
