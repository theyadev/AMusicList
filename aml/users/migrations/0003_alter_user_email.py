# Generated by Django 4.0.1 on 2022-02-04 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_activities_song_alter_lists_song_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Addresse Email'),
        ),
    ]
