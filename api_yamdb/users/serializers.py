from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    def validate_username(self, value):
        """Запрещаем использование 'me' в качестве username."""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать "me" в качестве username запрещено.'
            )
        return value

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        # Генерируем случайный код подтверждения.
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
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден.')
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError('Неверный код подтверждения.')
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

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
