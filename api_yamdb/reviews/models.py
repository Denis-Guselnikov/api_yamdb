from django.db import models


class Review(models.Model):
    title_id = models.ForeignKey()
    text = models.TextField()
    score = models.IntegerField()

class Comments(models.Model):
    pass
