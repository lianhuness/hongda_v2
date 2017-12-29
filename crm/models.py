# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import pre_save



class Client(models.Model):
    user = models.ForeignKey(User)
    cid = models.CharField(max_length=10, unique=True)
    company = models.CharField(max_length=200, unique=True)
    district = models.CharField(max_length=100)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s"%(self.cid, self.company)
#
# def update_client_cid(sender, instance, **kwargs):
#     instance.cid = "C-%s"%(Client.objects.count())
#     print(" \n\n *** hello **** ")
#
# pre_save.connect(update_client_cid, sender=Client)

class Contactor(models.Model):
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True, default='N/A')

    def __str__(self):
        return self.name

def contact_upload_to(instance, filename):
    directory =  '/'.join(['Order', instance.orderID, 'contract', filename])
    return directory


ORDER_STATUS_CHOICES = (
    ('DRAFT', '草稿'),
    ('SUBMIT', '提交'),
    ('DELETE', '取消'),
    ('SEND', '发货'),
    ('COMPLETE', '完成')
)
class Order(models.Model):
    user = models.ForeignKey(User)
    client = models.ForeignKey(Client)
    contactor = models.ForeignKey(Contactor)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='DRAFT')

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='订单金额')
    currency = models.CharField(max_length=5, choices=(('RMB', 'RMB'), ('USD', 'USD')), default='RMB')
    trueAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    orderID = models.CharField(max_length=20, unique=True, help_text='订单号')
    contract = models.FileField(upload_to=contact_upload_to)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.orderID

    class Meta:
        ordering = ['created_date']



def update_trueAmount(sender, instance, **kwargs):
    instance.orderID = instance.orderID.upper()
    if instance.currency == 'USD':
        instance.trueAmount = instance.amount*6.6
    else:
        instance.trueAmount = instance.amount

    print(" \n\n *** hello **** ")

pre_save.connect(update_trueAmount, sender=Order)






