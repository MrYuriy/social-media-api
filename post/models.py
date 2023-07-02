from django.db import models

from social_media_api import settings


class Hashtag(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True)

    def __str__(self):
        return self.title
