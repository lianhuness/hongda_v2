# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-23 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20180123_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='externalID',
            field=models.CharField(default='N/A', help_text='客户订单号', max_length=50),
        ),
    ]
