# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibility', models.BooleanField()),
            ],
        ),
    ]
