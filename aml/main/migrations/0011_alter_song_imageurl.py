# Generated by Django 4.0.1 on 2022-01-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_staff_role_delete_staffrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='imageUrl',
            field=models.URLField(max_length=100),
        ),
    ]
