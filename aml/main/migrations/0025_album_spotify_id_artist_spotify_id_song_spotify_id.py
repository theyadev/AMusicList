# Generated by Django 4.0.1 on 2022-01-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_remove_song_albums'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='spotify_id',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='spotify_id',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='spotify_id',
            field=models.CharField(default='a', max_length=250),
            preserve_default=False,
        ),
    ]
