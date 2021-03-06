# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 10:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_sentimentalanalysisdata_magnitude_normalized'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingTweetData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TwitterEntity')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100)),
                ('fcm_token', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='pendingtweetdata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.User'),
        ),
    ]
