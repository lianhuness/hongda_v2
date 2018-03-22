# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-04 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='名字'),
        ),
    ]
