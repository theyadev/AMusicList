# Generated by Django 4.0.1 on 2022-01-27 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_activities_action_delete_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.DeleteModel(
            name='UserRole',
        ),
    ]