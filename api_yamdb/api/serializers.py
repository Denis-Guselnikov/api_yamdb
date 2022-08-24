from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio',
                  'role', 'confirmation_code')
        validators = [UniqueTogetherValidator(
                      queryset=User.objects.all(),
                      fields=("email",),
                      message="Данная почта уже числится в БЗ",)]

    def validate_username(self, value):
        """Проверяем, пытается ли пользователь
         использовать "me" в качестве имени пользователя"""
        if value == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя")
        return value


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(
                                       queryset=User.objects.all()), ])
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all()), ])

    class Meta:
        model = User
        fields = ('__all__')

    def validate_username(self, value):
        """Проверяем, пытается ли пользователь
         использовать "me" в качестве имени пользователя"""
        if value == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя")
        return value


class TokenGetSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('__all__')