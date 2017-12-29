# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):
    user = models.ForeignKey(User)
    sku = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def itemphoto_upload_to(instance, filename):
    directory =  '/'.join(['Items', instance.item.sku, 'originals', filename])
    return directory


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item)
    image = models.ImageField(upload_to=itemphoto_upload_to)
    created_date = models.DateTimeField(auto_now=True)


class SubItem(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    subsku = models.CharField(max_length=20, unique=True)

    material = models.CharField(max_length=100, blank=True)
    specs = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    weight = models.IntegerField(help_text='克重',  default=0)
    MOQ = models.IntegerField(help_text='最小起订量',  default=0)
    unitprice = models.DecimalField(max_digits=8, decimal_places=2,   default=0)
    cartonsize = models.CharField(max_length=50, help_text='装箱外箱尺寸',   default=0)
    qtypercarton = models.IntegerField(help_text='每箱的数量',  default=0)
    cartongw = models.IntegerField(help_text='毛重',  default=0)

    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "SKU: %s"%self.subsku

def subitemphoto_upload_to(instance, filename):
    directory =  '/'.join(['Items', instance.subitem.item.sku, instance.subitem.subsku, filename])
    print("\n\n\n\n ******************* \n\n\n\n")
    print(directory)
    return directory

class SubItemPhoto(models.Model):
    subitem = models.ForeignKey(SubItem)
    image = models.ImageField(upload_to=subitemphoto_upload_to)
    created_date = models.DateTimeField(auto_now=True)

class SubItemSupplier(models.Model):
    subitem = models.ForeignKey(SubItem)
    name = models.CharField(max_length=100, help_text='供应商名称')
    city = models.CharField(max_length=50, help_text='城市')
    moq = models.IntegerField(help_text='最小起订量', default=0)
    unitprice = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text='单价', blank=True)
    other = models.TextField(blank=True)
    updated_date = models.DateTimeField(auto_now = True)

    def _str__(self):
        return "%s" %(self.name)
