# Generated by Django 4.0.1 on 2022-02-02 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_activities_song_alter_lists_song_and_more'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='artists',
        ),
        migrations.DeleteModel(
            name='Album',
        ),
        migrations.DeleteModel(
            name='Artist',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
    ]