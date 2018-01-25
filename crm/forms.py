# coding=utf-8
# author= YQZHU

from django import forms
from .models import Client, Contactor, Order

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('user', 'company', 'district')
        labels = {
            'company': '公司名称',
            'district': '地区'
        }
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

class ContactorForm(forms.ModelForm):
    class Meta:
        model = Contactor
        fields = ('client', 'name', 'email', 'tel', 'address')
        labels = {
            'name': '姓名',
            'email': 'Email',
            'tel': '电话',
            'address': '地址'
        }

    def __init__(self, *args, **kwargs):
        super(ContactorForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget = forms.HiddenInput()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('user', 'client',  'status', 'contactor', 'externalID', 'internalID','amount', 'currency',  'contract')
        labels = {
            'client': '客户',
            'contactor':'联系人',
            'externalID': '客户订单号/跟踪号',
            'internalID': '内部跟踪号',
            'amount':'金额',
            'currency': '货币',
            'contract': '合同'
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()
        # self.fields['trueAmount'].widget = forms.HiddenInput()
        # user = models.ForeignKey(User)
        # client = models.ForeignKey(Client)
        # contactor = models.ForeignKey(Contactor)
        # amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='订单金额')
        # currency = models.CharField(choices=(('RMB', 'RMB'), ('USD', 'USD')), default='RMB')
        # trueAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        #
        # orderID = models.CharField(max_length=20, unique=True, help_text='订单号')
        # contract = models.FileField(upload_to=contact_upload_to)