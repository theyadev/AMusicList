from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime

from songs.models import Song, Artist


class User(AbstractUser):
    list = models.ManyToManyField(Song, through="Lists")
    email = models.EmailField('Addresse Email', unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    favourite_artists = models.ManyToManyField(Artist, related_name="user_favourites")
    activity = models.ManyToManyField(
        Song, through="Activities", related_name="activity"
    )
    follows = models.ManyToManyField("User", related_name="user_followers")
    notification = models.ManyToManyField("Activities", through="Notifications", related_name="user_notifications")


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifs")
    activity = models.ForeignKey("Activities", on_delete=models.CASCADE, related_name="notif")
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.archived
class Activities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    date = models.DateTimeField(blank=True)

    def valid_notifications_actions(self):
        return ["ADDED", "REMOVED"]

    def valid_actions(self):
        return ["ADDED", "REMOVED", "ADDED FAVOURITE", "REMOVED FAVOURITE"]

    def is_action_valid(self):
        return self.action in self.valid_actions() 

    def save(self, *args, **kwargs):
        if not self.is_action_valid():
            return

        self.date = datetime.now()
        super().save(*args, **kwargs)

        if not self.action in self.valid_notifications_actions():
            return
            
        for user in self.user.user_followers.all():
            notif = Notifications(user=user, activity=self)
            notif.save()

    def __str__(self) -> str:
        return f"{self.user} {self.action} {self.song}"


class Lists(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_list")
    favourite = models.BooleanField()
