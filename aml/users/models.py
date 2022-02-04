from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime

from songs.models import Song, Artist


class User(AbstractUser):
    list = models.ManyToManyField(Song, through="Lists")
    email = models.EmailField('Addresse Email', unique=True)
    favourite_artists = models.ManyToManyField(Artist, related_name="user_favourites")
    activity = models.ManyToManyField(
        Song, through="Activities", related_name="activity"
    )
    follows = models.ManyToManyField("User", related_name="user_followers")


class Activities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.date = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} {self.action} {self.song}"


class Lists(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_list")
    favourite = models.BooleanField()
