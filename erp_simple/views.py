from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import Jhd, JhdForm, JhdFile_form, JhdLog_form
from crm.models import Order
from django.contrib import messages

# Create your views here.



def list_jihuadan(request):
    return HttpResponse("List Jihuadan")


def add_jihuadan(request, id):
    order = get_object_or_404(Order, pk=id)
    if request.user != order.user:
        return HttpResponse("You cannot add JHD in this order!")

    if request.method == 'POST':
        form = JhdForm(request.POST, request.FILES)
        if form.is_valid():
            jhd=form.save()
            jhd.add_log(request, u'添加计划单成功， 单号:%s'%jhd.id)
            return redirect(reverse('erp_view_jihuadan', kwargs={'id': jhd.id}))
    else:
        form = JhdForm()
        form.fields['order'].initial=order
        form.fields['user'].initial = request.user

    return render(request, 'jhd/add_jhd.html', {'order': order, 'form': form})

    return HttpResponse("Add Jihuadan")

def view_jihuadan(request, id):
    jhd = get_object_or_404(Jhd, pk=id)

    jhdfile_form = JhdFile_form()
    jhdfile_form.fields['user'].initial=request.user
    jhdfile_form.fields['jhd'].initial=jhd

    jhdlog_form = JhdLog_form()

    return render(request, 'jhd/view_jhd.html', {'jhd': jhd, 'file_form': jhdfile_form, 'log_form': jhdlog_form})

def add_jhd_file(request, id):
    jhd = get_object_or_404(Jhd, pk=id)

    if request.method == 'POST':
        fileForm = JhdFile_form(request.POST, request.FILES)
        if fileForm.is_valid():
            file = fileForm.save()
            jhd.add_log(request, u'添加文件： %s'% file.title)

    return redirect(reverse('erp_view_jihuadan', kwargs={'id': jhd.id}))


def add_jhd_log(request, id):
    jhd = get_object_or_404(Jhd, pk=id)

    if request.method == 'POST':
        logform = JhdLog_form(request.POST)
        if logform.is_valid():
            jhd.add_log(request, logform.cleaned_data['message'])

    return redirect(reverse('erp_view_jihuadan', kwargs={'id': jhd.id}))


def complete_jihuadan(request, id):
    jhd = get_object_or_404(Jhd, pk=id)

    if jhd.user != request.user:
        return HttpResponse("No rights to complete!")

    jhd.is_complete=True
    jhd.save()
    jhd.add_log(request, '状态 改成 完成！！！ ')
    return redirect(reverse('erp_view_jihuadan', kwargs={'id': jhd.id}))

def delete_jihuadan(request, id):
    jhd = get_object_or_404(Jhd, pk=id)

    if jhd.user != request.user:
        return HttpResponse("No rights to delete!")

    jhd.is_delete=True
    jhd.save()
    jhd.add_log(request, '状态 改成 取消！！！ ')
    return redirect(reverse('erp_view_jihuadan', kwargs={'id': jhd.id}))

def my_jhd(request, show):
    if show == 'DELETE':
        jhds = request.user.jhd_set.filter(is_delete=True).all()
    elif show == 'COMPLETE':
        jhds = request.user.jhd_set.filter(is_complete=True).all()
    else:
        jhds = request.user.jhd_set.filter(is_complete=False).filter(is_delete=False).all()

    return render(request, 'jhd/my_jhds.html', {'jhds': jhds, 'show': show })



from django import forms
class SearchForm(forms.Form):
    type = forms.ChoiceField(choices=[('jhd', '计划单号'), ('sales', '业务员')])
    search_key = forms.CharField(max_length=50)


def search_jhd(request):
    orders = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['type']=='jhd':
                import pdb
                pdb.set_trace()
                jhds = Jhd.objects.filter( id = form.cleaned_data['jhd']).all()
            elif form.cleaned_data['type']=='sales':
                jhds = Jhd.objects.filter(user_username = form.cleaned_data['sales']).all()
    else:
        form = SearchForm()

    return render(request, 'jhd/search_jhd.html', {'form': form, 'jhds': orders})

