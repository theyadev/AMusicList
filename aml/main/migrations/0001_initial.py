# Generated by Django 4.0.1 on 2022-01-31 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spotifyId', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('imageUrl', models.URLField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spotifyId', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=200)),
                ('imageUrl', models.URLField()),
                ('length', models.IntegerField()),
                ('releaseDate', models.DateTimeField(null=True, verbose_name='date released')),
                ('artists', models.ManyToManyField(related_name='artist_songs', to='main.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spotifyId', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=150)),
                ('releaseDate', models.DateTimeField(null=True)),
                ('imageUrl', models.URLField(max_length=250)),
                ('artists', models.ManyToManyField(related_name='artist_albums', to='main.Artist')),
                ('songs', models.ManyToManyField(related_name='song_albums', to='main.Song')),
            ],
        ),
    ]
