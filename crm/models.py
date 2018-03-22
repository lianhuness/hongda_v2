# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import pre_save
import datetime
from django.contrib import messages

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
    (8, u'2018 Taispo 展会'),
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
        messages.success(request,log )
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

def client_log_file_upload_to(instance, filename):
    directory =  '/'.join(['Client', instance.client.cid, 'logs', filename])
    return directory

class ClientFile(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    client = models.ForeignKey(Client)
    description = models.CharField(max_length=500, verbose_name=u'说明')
    file = models.FileField(upload_to=client_file_upload_to, verbose_name=u'文件')

    def __unicode__(self):
        return self.description
    def __str__(self):
        return self.__unicode__()


class ClientLog(models.Model):
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    note = models.TextField()
    file = models.FileField(upload_to=client_log_file_upload_to, blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    next_date = models.DateField(blank=True,null=True)

    def __unicode__(self):
        return u"%s:%s"%(self.created_date.date(), self.note)

    def __str__(self):
        return self.__unicode__()
    class Meta:
        ordering=['-created_date']


def namecard_upload_to(instance, filename):
    directory =  '/'.join(['Client', instance.client.cid, 'namecard', filename])
    return directory

class Contactor(models.Model):
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=50, blank=True, verbose_name=u'电话')
    address = models.TextField(blank=True, default='N/A', verbose_name=u'地址')
    namecard_front = models.ImageField(upload_to=namecard_upload_to, verbose_name=u'名片正面', blank=True, null=True)
    namecard_back = models.ImageField(upload_to=namecard_upload_to, verbose_name=u'名片反面', blank=True, null=True)

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


from django.db.models import Sum
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

    def totalExpense(self):
        exp = self.orderexpense_set.aggregate(Sum('amount'))
        return exp['amount__sum']

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

COLOR_PRODUCT_TYPE_CHOICE = (
    (1, u'乳胶片'),
    (2, u'乳胶薄圈'),
    (3, u'乳胶厚圈'),
    (4, u'单色乳胶管'),
    (5, u'多色乳胶管'),
    (20, u'其他')
)

EXPENSE_TYPE_CHOICE=(
    (1, u'制版费'),
    (2, u'运费'),
    (3, u'进仓费'),
    (4, u'返工费'),
    (5, u'快递费'),
    (6, u'采购费用'),
    (7, u'其他'),

)

class OrderExpense(models.Model):
    order = models.ForeignKey(Order)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)

    type = models.IntegerField(choices=EXPENSE_TYPE_CHOICE, default=7, verbose_name=u'费用种类')
    amount = models.DecimalField(decimal_places=2, max_digits=7, verbose_name=u'金额')
    note = models.CharField(max_length = 100, blank=True, null=True, verbose_name=u'备注(可空白)')

    def __unicode__(self):
        return u"%s - %s" %(self.get_type_display(), self.amount)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-created_date']

# class Color(models.Model):
#     user = models.ForeignKey(User)
#     client = models.ForeignKey(Client, verbose_name=u'客户')
#     producttype = models.SmallIntegerField(default=1,  verbose_name=u'产品分类', choices=COLOR_PRODUCT_TYPE_CHOICE)
#     pantom = models.CharField(max_length=50, verbose_name=u'潘通色号')
#     hongdacode = models.CharField(max_length=10, verbose_name=u'宏大色号',blank=True, null=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now_add=True)
#
#
#     def __unicode__(self):
#         return u'%s - %s - %s'%(self.id, self.get_producttype_display(), self.pantom)
#
#     def __str__(self):
#         return self.__unicode__()
#
# from django import forms
# class ColorForm(forms.ModelForm):
#     class Meta:
#         model = Color
#         fields='__all__'
#     def __init__(self, *args, **kwargs):
#         super(ColorForm, self).__init__(*args, **kwargs)
#         for i in ['user', 'client']:
#             self.fields[i].widget = forms.HiddenInput()






