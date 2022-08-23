from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Первое имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=255,
        choices=ROLES,
        default='user',
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default=''
    )


class Review(models.Model):
    title_id = models.ForeignKey()
    text = models.TextField()
    score = models.IntegerField()


class Comments(models.Model):
    pass


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name='Жанр')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    def __str__(self):
        return self.title


class Title(models.Model):
    title = models.CharField(max_length=255, verbose_name='Произведение')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='category'        
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='genre'
    )

    def __str__(self):
        return self.title
