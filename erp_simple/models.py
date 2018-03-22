# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from crm.models import Order
from django.contrib import messages

def jihuadan_upload_to(instance, filename):
    directory =  '/'.join(['JIHUADAN', '%s'%instance.id, filename])
    return directory

class Jhd(models.Model):
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    file = models.FileField(upload_to=jihuadan_upload_to)
    is_delete = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)

    class Meta:
        ordering=['-updated_date']

    def __unicode__(self):
        return str(self.id)
    def __str__(self):
        return self.__unicode__()

    def add_log(self, request, message):
        self.jhd_log_set.create(user=request.user, message=message)
        messages.success(request, message)

    def status(self):
        if self.is_delete:
            return u'已取消'
        elif self.is_complete:
            return u'已完成'
        else:
            return u'进行中'

    def lastUpdate(self):
        return self.jhd_log_set.first()



from django.forms import ModelForm
from django import forms


class JhdForm(ModelForm):
    class Meta:
        model = Jhd
        fields=('user', 'order', 'file')
        labels = {
            'order': '订单',
            'file': '生产计划单',
        }

    def __init__(self, *args, **kwargs):
        super(JhdForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['order'].widget = forms.HiddenInput()


class Jhd_log(models.Model):
    jhd = models.ForeignKey(Jhd)
    user = models.ForeignKey(User)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u"%s:%s:%s"%(self.user, self.created_date.date(), self.message)

    class Meta:
        ordering=['-created_date']

def jihuadan_file_upload_to(instance, filename):
    directory =  '/'.join(['JIHUADAN', '%s'%instance.jhd.id, filename])
    return directory

class Jhd_file(models.Model):
    jhd = models.ForeignKey(Jhd)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=jihuadan_file_upload_to)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_date']

class JhdLog_form(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class JhdFile_form(ModelForm):
    class Meta:
        model = Jhd_file
        fields=('user', 'jhd', 'title', 'file')
        labels = {
            'title': '文件描述',
            'file': '文件',
        }

    def __init__(self, *args, **kwargs):
        super(JhdFile_form, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['jhd'].widget = forms.HiddenInput()

JIHUADAN_GROUP = (
    (1, u'常规货'),
    (2, u'迪卡侬'),
)

IS_DELETE_CHOICE=(
    (False, u'有效流程单'),
    (True, u'无效流程单'),
)

import datetime

def get_next_day():
    return datetime.date.today() + datetime.timedelta(days=1)

class HouquanLiuchen(models.Model):
    user = models.ForeignKey(User)
    created_date = models.DateField(auto_now_add=True)
    shengchan_riqi = models.DateField(default=get_next_day, verbose_name=u'生产日期')
    group = models.PositiveSmallIntegerField(choices=JIHUADAN_GROUP, default=1, verbose_name=u'分类')
    line = models.PositiveIntegerField(verbose_name=u'制作线')
    caozuogong = models.CharField(max_length=50, verbose_name=u'操作工')
    fuzhugong = models.CharField(max_length=50, verbose_name=u'辅助工')
    jihuadan = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'订单号')
    color = models.CharField(max_length=10, verbose_name=u'颜色')
    jihua_dapian = models.PositiveIntegerField(default=0, verbose_name=u'计划大片数')
    shiji_dapian = models.PositiveIntegerField(default=0, verbose_name=u'实际大片数')

    is_delete = models.BooleanField(default=False, choices=IS_DELETE_CHOICE, verbose_name=u'已经删除')

    def __unicode__(self):
        return u"%s"%self.id
    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-id']

# 厚圈流程单
class HouquanLiuchenForm(ModelForm):
    class Meta:
        model = HouquanLiuchen
        fields='__all__'


    def __init__(self, *args, **kwargs):
        super(HouquanLiuchenForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

