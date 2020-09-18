# Generated by Django 3.1.1 on 2020-09-17 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cleverlyapi', '0004_auto_20200917_0210'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePostReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cleverlyapi.post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleverlyapi.profile')),
            ],
            options={
                'verbose_name': 'profile_post_reaction',
                'verbose_name_plural': 'profile_post_reactions',
            },
        ),
    ]