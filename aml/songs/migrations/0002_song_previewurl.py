# Generated by Django 4.0.1 on 2022-02-21 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='previewUrl',
            field=models.CharField(default='none', max_length=250),
            preserve_default=False,
        ),
    ]
