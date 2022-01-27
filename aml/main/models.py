from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    spotifyId = models.CharField(max_length=250)
    name = models.CharField(max_length=40)
    description = models.TextField()
    imageUrl = models.URLField()

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    spotifyId = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    imageUrl = models.URLField(max_length=100)
    length = models.IntegerField()
    releaseDate = models.DateTimeField("date released", null=True)

    artists = models.ManyToManyField(Artist)

    def __str__(self) -> str:
        return f"{self.title}"


class User(AbstractUser):
    list = models.ManyToManyField(Song, through="Lists")
    activity = models.ManyToManyField(
        Song, through="Activities", related_name="activity"
    )
    follows = models.ManyToManyField("User")


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favourite = models.BooleanField()


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    spotifyId = models.CharField(max_length=250)
    name = models.CharField(max_length=150)
    releaseDate = models.DateTimeField(null=True)

    artists = models.ManyToManyField(Artist, related_name="artist_albums")
    songs = models.ManyToManyField(Song, related_name="song_albums")
