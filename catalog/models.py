# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from crm.models import Client
from django.contrib import messages
# Create your models here.


def product_image_uploadto(instance, filename):
    directory = '/'.join(['catelogs', instance.catelog, instance.name, filename])
    return directory

def product_log_image_uploadto(instance, filename):
    directory = '/'.join(['catelogs', instance.product.catelog, instance.product.name, filename])
    return directory

class Product(models.Model):
    user = models.ForeignKey(User)
    catelog = models.CharField(max_length=300, verbose_name=u'产品分类')
    name = models.CharField(max_length=300, verbose_name=u'名称')
    image = models.ImageField(upload_to=product_image_uploadto, blank=True, null=True, verbose_name=u'图片')
    weight = models.IntegerField(verbose_name=u'重量(g)', default=0)
    size = models.CharField(max_length=100, verbose_name=u'尺寸', default='N/A')
    material = models.CharField(max_length=100, verbose_name=u'材质', default='N/A')
    costprice = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=u'成本价格')
    suggestprice = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=u'建议销售价格(RMB)')
    suggestmoq = models.IntegerField(default=0, verbose_name=u'建议最少起订量')
    note = models.TextField(blank=True, null=True, verbose_name=u'其他说明')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

    def addLog(self, request, log):
        messages.success(request, log)
        self.productlog_set.create( user = request.user, log=u'%s-%s'%(request.user, log ))

class ProductLog(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    log = models.TextField(max_length=500, verbose_name=u'记录', blank=True, null=True)
    image = models.ImageField(upload_to=product_log_image_uploadto, blank=True, null=True, verbose_name=u'图片')
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.log
    def __str__(self):
        return self.__unicode__()




def catelog_image_uploadto(instance, filename):
    directory = '/'.join(['catelog', instance.catelog.name, instance.name, filename])
    return directory


def itemphoto_upload_to(instance, filename):
    directory =  '/'.join(['Items', instance.item.sku, 'originals', filename])
    return directory

#
# class ItemPhoto(models.Model):
#     item = models.ForeignKey(Item)
#     image = models.ImageField(upload_to=itemphoto_upload_to)
#     created_date = models.DateTimeField(auto_now=True)
#
#
# class SubItem(models.Model):
#     user = models.ForeignKey(User)
#     item = models.ForeignKey(Item)
#     subsku = models.CharField(max_length=20, unique=True)
#
#     material = models.CharField(max_length=100, blank=True)
#     specs = models.CharField(max_length=100, blank=True)
#     color = models.CharField(max_length=100, blank=True)
#     weight = models.IntegerField(help_text='克重',  default=0)
#     MOQ = models.IntegerField(help_text='最小起订量',  default=0)
#     unitprice = models.DecimalField(max_digits=8, decimal_places=2,   default=0)
#     cartonsize = models.CharField(max_length=50, help_text='装箱外箱尺寸',   default=0)
#     qtypercarton = models.IntegerField(help_text='每箱的数量',  default=0)
#     cartongw = models.DecimalField(max_digits=8, decimal_places=2, help_text='毛重',  default=0)
#
#     updated_date = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):
#         return "SKU: %s"%self.subsku
#
def subitemphoto_upload_to(instance, filename):
    directory =  '/'.join(['Items', instance.subitem.item.sku, instance.subitem.subsku, filename])
    print("\n\n\n\n ******************* \n\n\n\n")
    print(directory)
    return directory
#
# class SubItemPhoto(models.Model):
#     subitem = models.ForeignKey(SubItem)
#     image = models.ImageField(upload_to=subitemphoto_upload_to)
#     created_date = models.DateTimeField(auto_now=True)
#
# class SubItemSupplier(models.Model):
#     subitem = models.ForeignKey(SubItem)
#     name = models.CharField(max_length=100, help_text='供应商名称')
#     city = models.CharField(max_length=50, help_text='城市')
#     moq = models.IntegerField(help_text='最小起订量', default=0)
#     unitprice = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text='单价', blank=True)
#     other = models.TextField(blank=True)
#     updated_date = models.DateTimeField(auto_now = True)
#
#     def _str__(self):
#         return "%s" %(self.name)
#
#
