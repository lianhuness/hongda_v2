# -*- coding: UTF-8 -*-

from django.db import models

# Create your models here.
from crm.models import Order
from django.contrib.auth.models import User


class Jihuadan(models.Model):
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='DRAFT')
    deliver_date = models.DateField()

    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return "%s-%s"%(self.order, self.pk)

    def getNextStatus(self):
        if self.status == 'DRAFT':
            return ['SUBMIT','CANCEL']
        elif self.status == 'SUBMIT':
            return ['DELIVER', 'CANCEL']
        elif self.status == 'DELIVER':
            return ['COMPLETE', 'CANCEL']

        return []

SOURCE_CHOICES = (
    ('HONGDA', u'宏大'),
    ('OUT', u'外购'),
    ('CLIENT', u'客户提供'),
)

PRODUCT_GROUP = (
    ('BAND', u'拉力带'),
    ('POWERBAND', u'208圈'),
    ('101BAND', u'101圈'),
    ('MINIBAND', u'小圈(101以下)'),
    ('OLDLATEX', u'老产品'),
    ('BALLOON', u'气球'),
    ('CARTON', u'外箱'),
    ('BOX', u'彩盒'),
    ('BAG', u'网袋/编织袋'),
    ('OPP', u'OPP/EPP袋'),
    ('STICK', u'贴标'),
    ('VALVE', u'前阀/尾阀'),
    ('OTHER',u'其他'),
)

def item_logo_upload_to(instance, filename):
    directory =  '/'.join(['JIHUADAN', '%s'%instance.jihuadan.id, filename])
    return directory


class Item(models.Model):
    jihuadan = models.ForeignKey(Jihuadan)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='HONGDA')
    product = models.CharField(max_length=100, choices=PRODUCT_GROUP)
    specs = models.CharField(max_length=200)
    color = models.CharField(max_length=50)
    qty = models.PositiveIntegerField()
    note = models.CharField(max_length=200)
    image = models.ImageField(upload_to=item_logo_upload_to, blank=True)

    status = models.CharField(max_length=10, default='DRAFT')



    def __str__(self):
        return "%s-%s" %(self.jihuadan, self.id)

    def updateLog(self, user, log):
        self.itemlog_set.create(user=user, log=log)

    def getNextStatus(self):
        return ["CANCEL"]


class ItemLog(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    created_date = models.DateTimeField(auto_now_add=True)
    log = models.TextField()

    def __str__(self):
        return "%s 在 %s 跟新： %s "%(self.user, self.created_date, self.log)


from django.forms import ModelForm
from django import forms


class JihuadanForm(ModelForm):
    class Meta:
        model = Jihuadan
        fields=('user', 'order', 'deliver_date')
        labels = {
            'order': '订单',
            'deliver_date': '交货日期',
        }

    def __init__(self, *args, **kwargs):
        super(JihuadanForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['order'].widget = forms.HiddenInput()


class JhdItemForm(ModelForm):
    class Meta:
        model = Item
        fields=('jihuadan', 'status', 'source', 'product', 'specs', 'color','qty', 'note', 'image')

    def __init__(self, *args, **kwargs):
        super(JhdItemForm, self).__init__(*args, **kwargs)
        self.fields['jihuadan'].widget = forms.HiddenInput()
        self.fields['status'].widget=forms.HiddenInput()


class SubscribeProduct(models.Model):
    user = models.ForeignKey(User)
    product = models.CharField(max_length=100, choices=PRODUCT_GROUP)

class SubscribeProductForm(ModelForm):
    class Meta:
        model = SubscribeProduct
        fields = ('user', 'product')
    def __init__(self, *args, **kwargs):
        super(SubscribeProductForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
