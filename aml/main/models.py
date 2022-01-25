from django.db import models
from django.contrib.auth.models import AbstractUser


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()
    imageUrl = models.URLField()

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    imageUrl = models.URLField(max_length=100)
    length = models.IntegerField()
    releaseDate = models.DateTimeField("date released", null=True)
    albumName = models.CharField(max_length=100, null=True)

    staffs = models.ManyToManyField(Staff)

    def __str__(self) -> str:
        return f"{self.title}"


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    description = models.TextField()
    privileges = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True)
    list = models.ManyToManyField(Song, through="Lists")


class Lists(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favourite = models.BooleanField()
