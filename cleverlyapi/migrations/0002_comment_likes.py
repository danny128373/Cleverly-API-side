# Generated by Django 3.1.1 on 2020-09-15 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleverlyapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]