# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('abstractuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.AbstractUser')),
            ],
            bases=('medical.abstractuser',),
        ),
        migrations.CreateModel(
            name='AbstractBusinessUser',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.BaseUser')),
            ],
            bases=('medical.baseuser',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.BaseUser')),
            ],
            bases=('medical.baseuser',),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('abstractbusinessuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.AbstractBusinessUser')),
            ],
            bases=('medical.abstractbusinessuser',),
        ),
        migrations.CreateModel(
            name='Pharmacist',
            fields=[
                ('abstractbusinessuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.AbstractBusinessUser')),
            ],
            bases=('medical.abstractbusinessuser',),
        ),
    ]
