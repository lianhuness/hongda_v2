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
    jihuadan = models.CharField(max_length=10, null=True, blank=True)
    group = models.PositiveSmallIntegerField(choices=JIHUADAN_GROUP, default=1)
    line = models.PositiveIntegerField()
    worker = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    jihua_dapian = models.PositiveIntegerField(default=0)
    shiji_dapian = models.PositiveIntegerField(default=0)
    start_date = models.DateField(default=get_next_day)

    is_delete = models.BooleanField(default=False, choices=IS_DELETE_CHOICE)

    def __unicode__(self):
        return self.id
    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-id']

# 厚圈流程单
class HouquanLiuchenForm(ModelForm):
    class Meta:
        model = HouquanLiuchen
        fields=('user', 'jihuadan', 'group', 'line', 'worker', 'color', 'jihua_dapian', 'shiji_dapian', 'start_date', 'is_delete')
        labels={
            'jihuadan': u'计划单号',
            'group': u'分类',
            'line': u'几号线',
            'worker': u'操作工',
            'color': u'颜色',
            'jihua_dapian': u'计划大片数',
            'shiji_dapian': u'实际大片数',
            'start_date': u'一线生产日期',
            'is_delete': u'此流程单是否有效',
        }

    def __init__(self, *args, **kwargs):
        super(HouquanLiuchenForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

