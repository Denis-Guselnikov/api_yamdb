from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg
from django.utils import timezone

from reviews.models import User, Category, Genre, Title, Review, Comments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio',
                  'role')
        validators = [UniqueTogetherValidator(
                      queryset=User.objects.all(),
                      fields=("email",),
                      message="Данная почта уже числится в БД",)]

    def validate_username(self, value):
        """Проверяем, пытается ли пользователь
         использовать "me" в качестве имени пользователя"""
        if value == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя")
        return value


class UserAuthorSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio',
                  'role', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('username', 'email',)

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
        fields = ('username', 'confirmation_code')


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
    
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Нельзя добавить второй отзыв на то же самое произведение'
            ),
        )


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review', )
