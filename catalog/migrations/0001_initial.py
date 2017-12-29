# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 12:57
from __future__ import unicode_literals

import catalog.models
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
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=catalog.models.itemphoto_upload_to)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('test', models.CharField(max_length=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Item')),
            ],
        ),
        migrations.CreateModel(
            name='SubItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subsku', models.CharField(max_length=20, unique=True)),
                ('material', models.CharField(blank=True, max_length=100)),
                ('specs', models.CharField(blank=True, max_length=100)),
                ('color', models.CharField(blank=True, max_length=100)),
                ('weight', models.IntegerField(blank=True, help_text='克重')),
                ('MOQ', models.IntegerField(blank=True, help_text='最小起订量')),
                ('unitprice', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('cartonsize', models.CharField(blank=True, help_text='装箱外箱尺寸', max_length=50)),
                ('qtypercarton', models.IntegerField(blank=True, help_text='每箱的数量')),
                ('cartongw', models.IntegerField(blank=True, help_text='毛重')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubItemPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=catalog.models.subitemphoto_upload_to)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('subitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.SubItem')),
            ],
        ),
        migrations.CreateModel(
            name='SubItemSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='供应商名称', max_length=100)),
                ('city', models.CharField(help_text='城市', max_length=50)),
                ('moq', models.IntegerField(blank=True, help_text='最小起订量')),
                ('unitprice', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='单价', max_digits=8)),
                ('other', models.TextField(blank=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('subitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.SubItem')),
            ],
        ),
    ]
