# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.shortcuts import HttpResponse, render, redirect, reverse, get_object_or_404
# Create your views here.
from .models import Jihuadan, Item
from crm.models import Order
from django.contrib import messages

def list_jihuadan(request):
    jihuadans = request.user.jihuadan_set.all()
    return render(request, 'jihuadan/list_jihuadan.html', {'jihuadans': jihuadans})

from django.forms import inlineformset_factory
from .models import JihuadanForm, JhdItemForm
import time
import datetime

def add_jihuadan(request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == 'POST':
        form = JihuadanForm(request.POST)
        if form.is_valid():
            jhd = form.save()
            messages.success(request, '计划单创立成功: %s '% jhd.pk)
            return redirect(reverse('add_jhd_item', kwargs={'id': jhd.pk}))
    else:
        form = JihuadanForm()
        form.fields['user'].initial = request.user
        form.fields['order'].initial = order
        form.fields['deliver_date'].initial = datetime.datetime.now()+datetime.timedelta(days=30)

    return render(request, 'jihuadan/add_jihuadan.html', {'order': order, 'form': form})

def del_jhd_item(request, id):
    item = get_object_or_404(Item, pk=id)
    return HttpResponse(item.jihuadan.status)
    if item.jihuadan.status is not "DRAFT":
        return HttpResponse("No Permission to delete in current status!")
    item.delete()
    messages.success(request, '成功删除')
    return redirect(reverse('add_jhd_item', kwargs={'id': item.jihuadan.id}))

def add_jhd_item(request, id):
    jhd = get_object_or_404(Jihuadan, pk=id)
    if jhd.status != "DRAFT":
        return HttpResponse("No permission to edit in current status !")

    if request.method == "POST":
        form = JhdItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, '添加: %s  成功 '%item.id )
            if 'continue_add' in request.POST:
                return redirect(reverse('add_jhd_item', kwargs={'id': jhd.id}))
            else:
                return redirect(reverse('view_jihuadan', kwargs={'id': jhd.id}))
    else:
        form = JhdItemForm()
        form.fields['jihuadan'].initial = jhd


    return render(request, 'jihuadan/add_jhd_item.html', {'jhd': jhd, 'form': form})

def view_jihuadan(request, id):
    jhd = get_object_or_404(Jihuadan, pk=id)
    return render(request, 'jihuadan/view_jihuadan.html', {'jhd': jhd})

def view_jhd_log(request, id):
    jhd = get_object_or_404(Jihuadan, pk=id)
    return render(request, 'jihuadan/view_jhd_log.html', {'jhd': jhd})

def change_jhd_status(request, id, status):
    jhd = get_object_or_404(Jihuadan, pk=id)
    jhd.status = status
    jhd.save()
    messages.success(request, '计划单 %s 成功' % status)

    if jhd.status == 'SUBMIT':
        for item in jhd.item_set.all():
            item.status = jhd.status
            item.save()
            item.updateLog(request.user, '提交计划单 %s'%item.status)

    return redirect(reverse('view_jihuadan', kwargs={'id': jhd.id}))


from .models import SubscribeProduct, SubscribeProductForm

def subproducts(request):
    if request.method == 'POST':
        form = SubscribeProductForm(request.POST)
        if form.is_valid():
            request.user.subscribeproduct_set.filter(product = form.cleaned_data.get('product')).delete()
            form.save()
    else:
        form = SubscribeProductForm()
        form.fields['user'].initial = request.user

    return render(request, 'chejian/subscribe_product.html', {'form': form})

def del_subproducts(request, id):
    return HttpResponse("LIst all items")


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def cj_myitems(request):
    my_sub_products = request.user.subscribeproduct_set.all()

    product_list = []
    for p in my_sub_products:
        product_list.append(p.product)


    items = Item.objects.filter(status='SUBMIT').filter(product__in=product_list).all()


    paginator = Paginator(items, 25)

    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'chejian/my_items.html', {'items':items,
                                                     'subproducts': my_sub_products,
                                                      })



from django import forms
class SearchForm(forms.Form):
    # type = forms.ChoiceField(choices=[('externalID', '合同外部跟踪号号'), ('internalID', '合同内部跟踪号号')])
    search_key = forms.CharField(max_length=50)

    # def clean_search_key(self):
    #     if self.cleaned_data['type'] == 'client_po':
    #         if Order.objects.filter(externalID__contains = self.cleaned_data['search_key']).exist():
    #             return self.cleaned_data['search_key']
    #         raise forms.ValidationError("合同不存在")


def jhd_search(request):
    jhds = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['search_key']
            key_list = key.split('-')
            if len(key_list) == 1:
                # search contract
                order = Order.objects.filter(internalID=key_list[0].upper()).all()
                if order.exists():
                    jhds = order[0].jihuadan_set.all()
            else:
                jhd_id = key_list[1]
                if jhd_id.isdigit():
                    obj = Jihuadan.objects.filter(id=int(jhd_id)).first()
                    if obj and obj.order.internalID == key_list[0].upper():
                            jhds.append(obj)

    else:
        form = SearchForm()

    return render(request, 'jihuadan/jhd_search.html', {'form': form, 'jhds': jhds})

