from django.db import models


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

