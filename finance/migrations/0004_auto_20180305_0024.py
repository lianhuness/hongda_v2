# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-04 16:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import finance.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0003_auto_20180305_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='KaoheRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=100)),
                ('point', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=finance.models.kaoherecord_upload_to)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recorduser', to=settings.AUTH_USER_MODEL)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.WeekStat')),
                ('yuangong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordyuangong', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='ruleuser',
            name='yuangong',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yuangong', to=settings.AUTH_USER_MODEL, verbose_name='考核人员'),
        ),
    ]
