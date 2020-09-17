# Generated by Django 3.1.1 on 2020-09-15 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cleverlyapi', '0002_comment_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileLikesComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.comment')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.profile')),
            ],
            options={
                'verbose_name': 'profile_likes_comment',
                'verbose_name_plural': 'profile_likes_comments',
            },
        ),
    ]
