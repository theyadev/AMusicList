# Generated by Django 4.0.1 on 2022-01-21 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_status_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffrole',
            name='name',
            field=models.TextField(max_length=25),
        ),
    ]
