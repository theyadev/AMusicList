# Generated by Django 4.0.1 on 2022-01-21 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StaffRole',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('imageUrl', models.URLField()),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staffrole')),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='genres',
            field=models.ManyToManyField(to='main.Genre'),
        ),
        migrations.AddField(
            model_name='song',
            name='staffs',
            field=models.ManyToManyField(to='main.Staff'),
        ),
    ]
