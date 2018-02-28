# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import pre_save
import datetime

CLIENT_LEVEL = (
    (1, u'潜在客人'),
    (2, u'进展中的客人'),
    (3, u'重要的客人'),
    (4, u'有问题的客人'),
)

CLIENT_SOURCE = (
    (0, u'老客户'),
    (1, u'1688询盘'),
    (2, u'Alibaba询盘'),
    (3, u'Alibaba RFQ'),
    (4, u'客人联系我们'),
    (5, u'网上发掘的客户信息'),
    (6, u'展会联系'),
    (7, u'其他渠道'),
)

class Client(models.Model):
    user = models.ForeignKey(User)
    cid = models.CharField(max_length=10, unique=True)
    company = models.CharField(max_length=200, unique=True)
    district = models.CharField(max_length=100)
    source = models.IntegerField(choices=CLIENT_SOURCE, default=0)
    update_date = models.DateTimeField(auto_now=True)
    level = models.PositiveSmallIntegerField(choices=CLIENT_LEVEL, default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.cid, self.company)

    def __str__(self):
        return self.__unicode__()

    def addLog(self, request, log):
        self.clientlog_set.create(user=request.user, note=log)

    def level_display(self):

        for (i,k) in CLIENT_LEVEL:
            if self.level == i:
                return k
        return 'NONE'


    def needUpdate(self):
        log = self.clientlog_set.first()
        if log and log.next_date:
            return log.next_date <= datetime.datetime.today().date()
        return False

#
# def update_client_cid(sender, instance, **kwargs):
#     instance.cid = "C-%s"%(Client.objects.count())
#     print(" \n\n *** hello **** ")
#
# pre_save.connect(update_client_cid, sender=Client)

def client_file_upload_to(instance, filename):
    directory =  '/'.join(['Client', instance.client.cid, 'files', filename])
    return directory

class ClientLog(models.Model):
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    note = models.TextField()
    file = models.FileField(upload_to=client_file_upload_to, blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    next_date = models.DateField(blank=True,null=True)

    def __unicode__(self):
        return u"%s:%s"%(self.created_date.date(), self.note)

    def __str__(self):
        return self.__unicode__()
    class Meta:
        ordering=['-created_date']



class Contactor(models.Model):
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True, default='N/A')

    def __str__(self):
        return self.name

def contact_upload_to(instance, filename):
    directory =  '/'.join(['Order', instance.internalID, 'contract', filename])
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

    externalID = models.CharField(max_length=50, default='N/A', help_text='客户订单号')
    internalID = models.CharField(max_length=20, unique=True, help_text='内部跟踪号')
    contract = models.FileField(upload_to=contact_upload_to)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.internalID

    class Meta:
        ordering = ['created_date']


def update_trueAmount(sender, instance, **kwargs):
    instance.externalID = instance.externalID.upper()
    instance.internalID = instance.internalID.upper()
    if instance.currency == 'USD':
        instance.trueAmount = instance.amount*6.6
    else:
        instance.trueAmount = instance.amount

    print(" \n\n *** hello **** ")

pre_save.connect(update_trueAmount, sender=Order)








