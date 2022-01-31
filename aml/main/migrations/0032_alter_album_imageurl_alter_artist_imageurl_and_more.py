# Generated by Django 4.0.1 on 2022-01-31 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_user_favourite_artists_alter_song_artists_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='imageUrl',
            field=models.URLField(max_length=250),
        ),
        migrations.AlterField(
            model_name='artist',
            name='imageUrl',
            field=models.URLField(max_length=250),
        ),
        migrations.AlterField(
            model_name='song',
            name='imageUrl',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]