from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class Rule(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100, verbose_name=u'考核简述', unique=True)
    points = models.IntegerField(verbose_name=u'分数')
    details = models.TextField(verbose_name=u'说明')
    updated_date= models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return u'%s (%s)'%(self.name, self.points)
    def __str__(self):
        return self.__unicode__()

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

class RuleUser(models.Model):
    kaoheyuan = models.ForeignKey(User, related_name='kaoheyuan')
    yuangong = models.ForeignKey(User, related_name='yuangong', verbose_name=u'考核人员')

    def __unicode__(self):
        return u'%s (%s)'%(self.kaoheyuan, self.yuangong)
    def __str__(self):
        return self.__unicode__()

class RuleUserForm(forms.ModelForm):
    class Meta:
        model = RuleUser
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(RuleUserForm, self).__init__(*args, **kwargs)
        self.fields['kaoheyuan'].widget = forms.HiddenInput()

class WeekStat(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100, verbose_name=u'20XX年-X周/X月', default=u'20XX年-X周/X月')
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()

class WeekStatForm(forms.ModelForm):
    class Meta:
        model = WeekStat
        fields=('name',)

def kaoherecord_upload_to(instance, filename):
    directory =  '/'.join(['KAOHE', '%s'%instance.yuangong, filename])
    return directory

class KaoheRecord(models.Model):
    user = models.ForeignKey(User, related_name='recorduser')
    week = models.ForeignKey(WeekStat)
    yuangong = models.ForeignKey(User, related_name='recordyuangong')
    rule = models.CharField(max_length=100)
    point = models.IntegerField()
    image = models.ImageField(upload_to=kaoherecord_upload_to, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_date']

    def __unicode__(self):
        return u"%s: %s 违反 %s 分数 %s "%(self.id, self.yuangong, self.rule, self.point)
    def __str__(self):
        return self.__unicode__()


