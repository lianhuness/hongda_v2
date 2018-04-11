# -*- coding: UTF-8 -*-

from django.shortcuts import HttpResponse, render, redirect, reverse, get_object_or_404

from django.contrib import messages
# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Client, Contactor, Order
from .forms import ClientForm, OrderForm
from django import forms
from django.contrib.auth.decorators import permission_required
import datetime

@permission_required('crm.add_order')
def crm_home(request):
    outdate_logs = []

    today = datetime.date.today()

    for c in request.user.client_set.all():
        fl = c.clientlog_set.first()
        if fl and fl.next_date and fl.next_date <= today:
            outdate_logs.append(fl)
            # need_todo.append(
            #     {'display': "%s(%s): %s" % (fl.client, fl.next_date, fl.note),
            #      'id': fl.id,
            #      'url': reverse('view_client_log', kwargs={'id': fl.client.id})}
            # )


    return render(request, 'clients/crm_home.html', {'outdate_logs': outdate_logs})


class DateForm(forms.Form):
    date = forms.DateField(label = u'日期')

@permission_required('crm.add_order')
def daily_report(request):
    date = datetime.date.today()
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
    else:
        form = DateForm()
        form.fields['date'].initial = date

    new_clients = request.user.client_set.filter(created_date__date=date).all()
    new_updates = request.user.clientlog_set.filter(created_date__date=date).all()

    return render(request, 'clients/daily_report.html',
                  {'date': date,
                   'form': form,
                   'new_clients': new_clients,
                   'new_updates': new_updates})


from .models import CLIENT_SOURCE, CLIENT_LEVEL
class Listclient_form(forms.Form):
    source = forms.ChoiceField(label=u'客户来源')
    level = forms.ChoiceField(label = u'客户等级')
    user = forms.CharField(label=u'销售代表', required=False)
    name = forms.CharField(label=u'客户', max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(Listclient_form, self).__init__(*args, **kwargs)
        clientchoice = [(-1, 'ALL')]
        clientchoice.extend(CLIENT_SOURCE)
        levelchoice = [(-1, 'ALL')]
        levelchoice.extend(CLIENT_LEVEL)
        self.fields['source'].choices = clientchoice
        self.fields['source'].initial =clientchoice[0]
        self.fields['level'].choices = levelchoice
        self.fields['level'].initial = levelchoice[0]

@permission_required('crm.add_order')
def list_all_clients(request):
    clients = request.user.client_set.all()
    form = Listclient_form()

    if request.user.isManager():
        clients = Client.objects.all()
    else:
        form.fields['user'].widget = forms.HiddenInput()

    if request.method == 'POST':
        form = Listclient_form(request.POST)
        if form.is_valid():
            source = int(form.cleaned_data['source'])
            level = int(form.cleaned_data['level'])
            name = form.cleaned_data['name']
            user = form.cleaned_data['user']
            if source>= 0:
                clients = clients.filter(source=source).all()
            if level >=0:
                clients = clients.filter(level = level).all()
            if form.cleaned_data['name']:
                clients = clients.filter(company__contains=name).all()
            if form.cleaned_data['user']:
                clients=clients.filter(user__username=user).all()

    return render(request, 'clients/list_clients.html', {'clients': clients, 'form': form, 'level':0})

from django.contrib.auth.models import User, Permission

class ChangeClientRepForm(forms.Form):
    p = Permission.objects.filter(codename='add_order')
    user = forms.ModelChoiceField(label=u'更改销售代表', queryset=User.objects.filter(user_permissions=p).all())

@permission_required('crm.add_order')
def change_client_rep(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == 'POST':
        form = ChangeClientRepForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            preuser = client.user
            client.user = user
            client.save()
            client.addLog(request, u'销售代表 %s -> %s'%(preuser, user) )
            return redirect(reverse('list_all_clients'))
    else:
        return HttpResponse("Something is wrong. ")



class ContactorForm(forms.ModelForm):
    class Meta:
        model = Contactor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ContactorForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget = forms.HiddenInput()

@permission_required('crm.add_order')
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.cid = "C-%s"%Client.objects.count()
            client.save()
            client.addLog(request, u'添加客户- %s '%client)
            return redirect(reverse('add_contactor', kwargs={'id': client.id}))
    else:
        form = ClientForm()
        form.fields['user'].initial = request.user
    return render(request, 'clients/add_client.html', {'form': form})

@permission_required('crm.add_order')
def edit_client(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            client.addLog(request, u'修改客户 - %s'%client)
            return redirect(reverse('view_client', kwargs={'id': client.id}))
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/edit_client.html', {'form': form, 'client': client})

@permission_required('crm.add_order')
def view_client(request, id):
    client = get_object_or_404(Client, pk=id)
    changeuserform = ChangeClientRepForm()
    if client.user == request.user or request.user.canViewOrder:
        return render(request, 'clients/view_client.html', {'client': client, 'changeuserform': changeuserform})
    else:
        return HttpResponse(u'没有权限， 联系管理员')


@permission_required('crm.add_order')
def add_contactor(request, id):
    client = get_object_or_404(Client, pk=id)
    if client.user != request.user and request.user.canViewOrder() == False:
        return HttpResponse("No Permission")

    if request.method == 'POST':
        form = ContactorForm(request.POST, request.FILES)
        if form.is_valid():
            contactor = form.save()
            client.addLog(request, u'添加联系人： %s'%contactor)
            return redirect(reverse('view_client', kwargs={'id': client.id}))
    else:
        form = ContactorForm()
        form.fields['client'].initial = client
    return render(request, 'clients/add_contactor.html', {'form': form, 'client': client})

@permission_required('crm.add_order')
def edit_contactor(request, id):
    contactor = get_object_or_404(Contactor, pk=id)

    if request.method == 'POST':
        form = ContactorForm(request.POST, request.FILES, instance=contactor)
        if form.is_valid():
            contactor = form.save()
            contactor.client.addLog(request, u'修改联系人： %s'%contactor)
            return redirect(reverse('view_client', kwargs={'id': contactor.client.id}))
    else:
        form = ContactorForm(instance=contactor)

    return render(request, 'clients/edit_contactor.html', {'form': form, 'contactor': contactor})





# Orders

from .models import ORDER_STATUS_CHOICES
class ListOrderForm(forms.Form):
    status = forms.ChoiceField(label=u'状态')
    user = forms.CharField(label=u'销售代表', required=False)
    client = forms.CharField(label=u'客户', max_length=50, required=False)
    internalid = forms.CharField(label=u'内部跟踪号', max_length=10, required=False)
    externalid = forms.CharField(label = u'外部跟踪号', max_length=10, required=False)

    def __init__(self, *args, **kwargs):
        super(ListOrderForm, self).__init__(*args, **kwargs)
        statuschoice = [('ALL', 'ALL')]
        statuschoice.extend(ORDER_STATUS_CHOICES)
        self.fields['status'].choices = statuschoice
        self.fields['status'].initial =statuschoice[0]

@permission_required('crm.add_order')
def list_orders(request):
    order_list = request.user.order_set
    form = ListOrderForm()
    if request.user.isManager():
        order_list = Order.objects

    if request.method == "POST":
        form = ListOrderForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            if status != 'ALL':
                order_list = order_list.filter(status = status)
            if form.cleaned_data['user']:
                order_list = order_list.filter(user__username=form.cleaned_data['user'])
            if form.cleaned_data['client']:
                order_list = order_list.filter(client__company__contains = form.cleaned_data['client'])
            if form.cleaned_data['internalid']:
                order_list = order_list.filter(internalID__contains =form.cleaned_data['internalid'])
            if form.cleaned_data['externalid']:
                order_list = order_list.filter(externalID__contains =form.cleaned_data['externalid'])

    order_list = order_list.all()
    return render(request, 'orders/list_orders.html', {'order_list': order_list, 'searchform': form})


@permission_required('crm.add_order')
def add_order(request, id):
    client = get_object_or_404(Client, pk=id)
    if client.user != request.user and request.user.canViewOrder() == False:
        return HttpResponse("No Permission")

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            order.addLog(request,  '订单(%s) 创立成功'%(order.internalID))
            return redirect(reverse('view_order', kwargs={'id': order.id}))
    else:
        form = OrderForm()
        form.fields['user'].initial = request.user
        form.fields['client'].initial = client
        form.fields['contactor'].queryset = client.contactor_set.all()
        form.fields['contactor'].initial = client.contactor_set.first()

    return render(request, 'orders/add_order.html', {'client': client, 'form': form})

@permission_required('crm.add_order')
def edit_order(request, id):
    order = get_object_or_404(Order, pk=id)
    if order.user != request.user and request.user.canViewOrder() == False:
        return HttpResponse("No Permission")

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save()
            msg = ""
            for fld in form.changed_data:
                msg = "%s, %s" %(msg, "%s: %s -> %s"%(fld, form.initial[fld], form.cleaned_data[fld]))
                print(msg)
            if len(msg)>0:
                order.addLog(request, u'修改订单 %s'%msg)
            return redirect(reverse('view_order', kwargs={'id': order.id}))
    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/edit_order.html', {'order': order, 'form': form})


def view_order(request, id):

    order = get_object_or_404(Order, pk=id)
    if order.user != request.user and request.user.canViewOrder() == False:
        return HttpResponse("No Permission")

    return render(request, 'orders/view_order.html', {'order': order})




class SearchForm(forms.Form):
    type = forms.ChoiceField(choices=[('externalID', '合同外部跟踪号号'), ('internalID', '合同内部跟踪号号')])
    search_key = forms.CharField(max_length=50)

    # def clean_search_key(self):
    #     if self.cleaned_data['type'] == 'client_po':
    #         if Order.objects.filter(externalID__contains = self.cleaned_data['search_key']).exist():
    #             return self.cleaned_data['search_key']
    #         raise forms.ValidationError("合同不存在")


def crm_search(request):
    if request.user.isSales is False and request.user.isSalesManager is False:
        return HttpResponse("No Permission")

    orders = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['type']=='externalID':
                orders = Order.objects.filter(externalID__contains = form.cleaned_data['search_key']).all()
            elif form.cleaned_data['type']=='internalID':
                orders = Order.objects.filter(internalID__contains = form.cleaned_data['search_key']).all()
    else:
        form = SearchForm()

    return render(request, 'orders/crm_search.html', {'form': form, 'orders': orders})



from .models import ClientLog

class ClientLogForm(forms.ModelForm):
    class Meta:
        model = ClientLog
        fields = ('user', 'client', 'note', 'file', 'next_date')
        labels = {
            'note': '记录',
            'file': '文件',
            'next_date': u'下一次的时间(年/月/日)'
        }
    def __init__(self, *args, **kwargs):
        super(ClientLogForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['client'].widget = forms.HiddenInput()


@permission_required('crm.add_order')
def add_client_log(request, id):
    if request.method == 'POST':
        form = ClientLogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'LOG added!')
        else:
            for i in form.errors:
                messages.error(request, form.errors[i])

    return redirect(reverse('view_client_log', kwargs={'id': id}))


@permission_required('crm.add_order')
def view_client_log(request,id):
    client = get_object_or_404(Client, pk=id)

    addLogForm = ClientLogForm()
    addLogForm.fields['user'].initial = request.user
    addLogForm.fields['client'].initial = client

    return render(request, 'clients/view_log.html', {'client': client, 'addLogForm': addLogForm})

from .models import ClientFile

class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(ClientFileForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['client'].widget = forms.HiddenInput()

@permission_required('crm.add_order')
def add_client_file(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == 'POST':
        form = ClientFileForm(request.POST, request.FILES)
        if form.is_valid():
            cf = form.save()
            client.addLog(request, u'%s , 添加文件 - %s'%(request.user, cf))
            return redirect(reverse("view_client", kwargs={'id': cf.client.id}))
    else:
        form = ClientFileForm()
        form.fields['user'].initial = request.user
        form.fields['client'].initial = client

    return render(request, 'clients/add_file.html', {'client': client, 'form': form})

def del_client_file(request, id):
    cf = get_object_or_404(ClientFile, pk=id)
    cf.delete()
    cf.client.addLog(request, u'%s, 删除文件-%s'%(request.user, cf))
    return redirect(reverse("view_client", kwargs={'id':cf.client.id}))


from .models import OrderExpense
class OrderExpenseForm(forms.ModelForm):
    class Meta:
        model = OrderExpense
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(OrderExpenseForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['order'].widget = forms.HiddenInput()

@permission_required('crm.add_orderexpense')
def add_order_expense(request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == "POST":
        form = OrderExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            messages.success(request, 'Add Expense success. ')
            return redirect(reverse('view_order', kwargs={'id': id}))
    else:
        form = OrderExpenseForm()
        form.fields['user'].initial = request.user
        form.fields['order'].initial = order
    return render(request, 'orders/add_expense.html', {'order': order, 'form': form})

@permission_required('crm.add_orderexpense')
def expense_list(request):
    expenses = OrderExpense.objects.all()
    return render(request, 'orders/expense_list.html', {'expenses': expenses})

@permission_required('crm.add_orderexpense')
def del_expense(request, id):
    exp = get_object_or_404(OrderExpense, pk=id)
    exp.delete()
    messages.success(request, 'Expense deleted. ')
    return redirect(reverse('expense_list'))
#
# from .models import Color, ColorForm
#
# class ColorSearchForm(forms.Form):
#     type = forms.ChoiceField(choices=[('user', u'用户'), ('client', u'客户'),('phantom', u'潘通')],label=u'Type')
#     search_key = forms.CharField(max_length=50)
#     from .models import COLOR_PRODUCT_TYPE_CHOICE
#     producttype = forms.ChoiceField(choices = COLOR_PRODUCT_TYPE_CHOICE, required=False, label='产品类别')
#
# def list_colors(request):
#     if request.method == 'POST':
#         print("Hello")
#     else:
#         form = ColorSearchForm()
#         colors = Color.objects.all()
#
#     return render(request, 'colors/list_colors.html', {'colors': colors, 'form': form})
#
# def add_color(request, id):
#     client = get_object_or_404(Client, pk= id)
#     if request.method == "POST":
#         form = ColorForm(request.POST)
#         if form.is_valid():
#             c = form.save()
#             c.client.addLog(request, u'添加新颜色：%s'% c )
#             return redirect(reverse('list_colors'))
#     else:
#         form = ColorForm()
#         form.fields['user'].initial =request.user
#         form.fields['client'].initial = client
#
#     return render(request, 'colors/add_color.html', {'client': client, 'form': form})
#
# def edit_color(request, id):
#     color = get_object_or_404(Color, pk=id)
#     return render(request, 'colors/.html', {})
#
# def delete_color(request, id):
#     color = get_object_or_404(Color, pk=id)
#     return render(request, 'colors/.html', {})

