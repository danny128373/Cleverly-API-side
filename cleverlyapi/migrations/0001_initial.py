# Generated by Django 3.1.1 on 2020-09-09 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('image', models.CharField(default='', max_length=500)),
            ],
            options={
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.CharField(max_length=500)),
                ('about', models.CharField(max_length=255)),
                ('likes', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('friendee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='friendee', to='cleverlyapi.profile')),
                ('friender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='friender', to='cleverlyapi.profile')),
            ],
            options={
                'verbose_name': 'relationship',
                'verbose_name_plural': 'relationships',
            },
        ),
        migrations.CreateModel(
            name='ProfileCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cleverlyapi.community')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.profile')),
            ],
            options={
                'verbose_name': 'profile_community',
                'verbose_name_plural': 'profile_communities',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('likes', models.IntegerField(default=0)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.community')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.profile')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.conversation')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.profile')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.AddField(
            model_name='conversation',
            name='profile1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile1', to='cleverlyapi.profile'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='profile2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile2', to='cleverlyapi.profile'),
        ),
        migrations.AddField(
            model_name='community',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.profile'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.profile')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
