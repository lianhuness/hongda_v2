# -*- coding: UTF-8 -*-
from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponse
from .models import Rule, RuleForm
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

def list_rules(request):
    rules = Rule.objects.all()

    return render(request, 'rules/list_rules.html', {'rules': rules})

@permission_required('finance.add_rule')
def add_rule(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            rule = form.save()
            messages.success(request, u'考核添加成功: %s '%rule)
            return redirect(reverse('list_rules'))
    else:
        form = RuleForm()
        form.fields['user'].initial = request.user


    return render(request, 'rules/add_rule.html', {'form': form})

@permission_required('finance.add_rule')
def edit_rule(request, id):
    rule = get_object_or_404(Rule, pk=id)
    if request.method == 'POST':
        form = RuleForm(request.POST, instance=rule)
        if form.is_valid():
            rule = form.save()
            messages.success(request, u'考核更新成功: %s '%rule)
            return redirect(reverse('list_rules'))
    else:
        form = RuleForm(instance=rule)
    return render(request, 'rules/edit_rule.html', {'form': form, 'rule': rule})

from .models import RuleUser, RuleUserForm

@permission_required('finance.add_rule')
def my_yuangong(request):
    yuangong = RuleUser.objects.filter(kaoheyuan=request.user).all()

    form = RuleUserForm()
    form.fields['kaoheyuan'].initial = request.user

    return  render(request, 'rules/my_yuangong.html', {'yuangong': yuangong, 'form': form})

@permission_required('finance.add_rule')
def add_yuangong(request):
    if request.method == "POST":
        form = RuleUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Add success')
    return redirect(reverse('my_yuangong'))

@permission_required('finance.add_rule')
def del_yuangong(request, id):
    yuangong = get_object_or_404(RuleUser,pk=id)
    yuangong.delete()
    messages.success(request, "Success delete")
    return redirect(reverse('my_yuangong'))


from .models import WeekStat, WeekStatForm
def list_weeks(request):
    weeks = WeekStat.objects.all()
    form = WeekStatForm()
    return render(request, 'rules/list_weeks.html', {'weeks': weeks, 'form': form})

def add_week(request):
    if request.method == "POST":
        form = WeekStatForm(request.POST)
        if form.is_valid():
            week = request.user.weekstat_set.create(name=form.cleaned_data['name'])
            messages.success(request, 'Add week success.')
    return redirect(reverse('list_weeks'))

def edit_week(request, id):
    return redirect(reverse('list_weeks'))

from django import forms
class KaoheRecordForm(forms.Form):
    yuangong = forms.ModelChoiceField(label=u'员工', queryset=RuleUser.objects.all())
    rule = forms.ModelChoiceField(label = u'规格', queryset=Rule.objects.all())
    image = forms.ImageField(label=u'记录', allow_empty_file=True, required=False)

from django.db.models import Sum

def view_week(request, id):
    week = get_object_or_404(WeekStat, pk=id)
    form = KaoheRecordForm()
    form.fields['yuangong'].queryset = RuleUser.objects.filter(kaoheyuan=request.user)
    form.fields['rule'].queryset = request.user.rule_set.all()

    order_by_score = week.kaoherecord_set.values('yuangong__username').annotate(total_point=Sum('point')).order_by('total_point')


    return render(request, 'rules/view_week.html', {'week': week, 'form': form, 'order_by_score': order_by_score})

from .models import KaoheRecord
def add_kaohe_record(request, id):
    week = get_object_or_404(WeekStat, pk=id)
    if request.method == "POST":
        form = KaoheRecordForm(request.POST, request.FILES)
        if form.is_valid():
            KaoheRecord.objects.create(week=week,
                                       user=request.user,
                                       yuangong=form.cleaned_data['yuangong'].yuangong,
                                       rule="%s"%(form.cleaned_data['rule']),
                                       point = form.cleaned_data['rule'].points,
                                       image = form.cleaned_data['image'])
            messages.success(request, 'Add success')
    return redirect(reverse('view_week', kwargs={'id': week.id}))

def del_kaohe_record(request, id):
    record = get_object_or_404(KaoheRecord, pk=id)
    record.delete()
    messages.success(request, 'Del success')
    return redirect(reverse('view_week', kwargs={'id': record.week.id}))

