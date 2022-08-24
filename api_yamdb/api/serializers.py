from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.db.models import Avg
from django.utils import timezone

from reviews.models import User, Category, Genre, Title


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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(self, value):
        current_year = timezone.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                'Укажите год создания произведения.'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('__all__')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 1)