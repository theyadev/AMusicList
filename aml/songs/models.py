from django.db import models


class Artist(models.Model):
    """Artist model"""

    id = models.AutoField(primary_key=True)
    spotifyId = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    description = models.TextField()
    imageUrl = models.URLField(max_length=250)

    def __str__(self) -> str:
        """Returns the name of the artist"""
        return self.name


class Song(models.Model):
    """Song model"""

    id = models.AutoField(primary_key=True)
    spotifyId = models.CharField(max_length=250)
    title = models.CharField(max_length=200)
    imageUrl = models.URLField(max_length=200)
    length = models.IntegerField()
    releaseDate = models.DateTimeField("date released", null=True)
    previewUrl = models.CharField(max_length=250, null=True)

    artists = models.ManyToManyField(Artist, related_name="artist_songs")

    def __str__(self) -> str:
        """Returns the title of the song"""
        return self.title


class Album(models.Model):
    """Album model"""

    id = models.AutoField(primary_key=True)
    spotifyId = models.CharField(max_length=250)
    name = models.CharField(max_length=150)
    releaseDate = models.DateTimeField(null=True)
    imageUrl = models.URLField(max_length=250)

    artists = models.ManyToManyField(Artist, related_name="artist_albums")
    songs = models.ManyToManyField(Song, related_name="song_albums")

    def __str__(self) -> str:
        """Returns the album name"""
        return self.name
