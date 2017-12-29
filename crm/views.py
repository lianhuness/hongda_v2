# -*- coding: UTF-8 -*-

from django.shortcuts import HttpResponse, render, redirect, reverse, get_object_or_404

from django.contrib import messages
# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Client, Contactor, Order
from .forms import ClientForm, ContactorForm, OrderForm
from django import forms

def list_clients(request):
    clients = request.user.client_set.all()

    return render(request, 'clients/list_clients.html', {'clients': clients})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.cid = "C-%s"%Client.objects.count()
            client.save()
            messages.success(request, '客户信息添加成功!')
            return redirect(reverse('add_contactor', kwargs={'id': client.id}))
    else:
        form = ClientForm()
        form.fields['user'].initial = request.user

    return render(request, 'clients/add_client.html', {'form': form})

def edit_client(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, '客户信息修改成功!')
            return redirect(reverse('view_client', kwargs={'id': client.id}))
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/edit_client.html', {'form': form, 'client': client})


def view_client(request, id):
    client = get_object_or_404(Client, pk=id)

    return render(request, 'clients/view_client.html', {'client': client})

def add_contactor(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == 'POST':
        form = ContactorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '客户联系人添加成功!')
            return redirect(reverse('view_client', kwargs={'id': client.id}))
    else:
        form = ContactorForm()
        form.fields['client'].initial = client
    return render(request, 'clients/add_contactor.html', {'form': form, 'client': client})


def edit_contactor(request, id):
    contactor = get_object_or_404(Contactor, pk=id)
    if request.method == 'POST':
        form = ContactorForm(request.POST, instance=contactor)
        if form.is_valid():
            form.save()
            messages.success(request, '客户联系人跟新成功!')
            return redirect(reverse('view_client', kwargs={'id': contactor.client.id}))
    else:
        form = ContactorForm(instance=contactor)

    return render(request, 'clients/edit_contactor.html', {'form': form, 'contactor': contactor})



# Orders
def list_orders(request):
    order_list = request.user.order_set.all()
    return render(request, 'orders/list_orders.html', {'order_list': order_list})

def addOrderRecord(request, order,  msg):
    messages.success(request, msg)

def add_order(request, id):
    client = get_object_or_404(Client, pk=id)

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            addOrderRecord(request, order, '订单(%s) 创立成功')
            return redirect(reverse('view_order', kwargs={'id': order.id}))
    else:
        form = OrderForm()
        form.fields['user'].initial = request.user
        form.fields['client'].initial = client
        form.fields['contactor'].queryset = client.contactor_set.all()
        form.fields['contactor'].initial = client.contactor_set.first()

    return render(request, 'orders/add_order.html', {'client': client, 'form': form})

def edit_order(request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save()
            addOrderRecord(request, order, '%s 修改订单成功 '%request.user)
            return redirect(reverse('view_order', kwargs={'id': order.id}))
    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/edit_order.html', {'order': order, 'form': form})

def view_order(request, id):
    order = get_object_or_404(Order, pk=id)
    return render(request, 'orders/view_order.html', {'order': order})
