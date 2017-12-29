# -*- coding: UTF-8 -*-
# coding=utf-8
# author= YQZHU

from django import forms
from .models import Item, ItemPhoto, SubItem, SubItemPhoto, SubItemSupplier

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('user', 'sku', 'name', 'description')
        labels={
            'sku': "SKU",
            'name': '名称',
            'description': '描述'
        }

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

    def clean_sku(self):
        data = self.cleaned_data['sku']
        return data.upper()

class ItemPhotoForm(forms.ModelForm):
    class Meta:
        model = ItemPhoto
        fields = ('item', 'image')
        labels = {'image': '图片'}
    def __init__(self, *args, **kwargs):
        super(ItemPhotoForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget = forms.HiddenInput()

class SubItemForm(forms.ModelForm):
    class Meta:
        model = SubItem
        fields = ('user', 'item', 'subsku', 'material', 'specs', 'color', 'weight', 'MOQ', 'unitprice', 'cartonsize', 'qtypercarton', 'cartongw')
        labels = {
            'subsku': "SKU",
            'material': '材料',
            'specs': '规格',
                     'color': "颜色" ,
                     'weight': "重量(g)",
                     'MOQ': "最小起订量",
                     'unitprice': "单价(RMB)",
                     'cartonsize': "外箱尺寸",
                     'qtypercarton': "每箱数量",
            'cartongw': "毛重(KG)"
        }

    def __init__(self, *args, **kwargs):
        super(SubItemForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget = forms.HiddenInput()
        self.fields['user'].widget = forms.HiddenInput()

    def clean_subsku(self):
        subsku = self.cleaned_data['subsku']
        return subsku.upper()

class SubItemPhotoForm(forms.ModelForm):
    class Meta:
        model = SubItemPhoto
        fields = ('subitem', 'image')
        labels = {'image': '图片'}
    def __init__(self, *args, **kwargs):
        super(SubItemPhotoForm, self).__init__(*args, **kwargs)
        self.fields['subitem'].widget = forms.HiddenInput()


class SubItemSupplierForm(forms.ModelForm):
    class Meta:
        model = SubItemSupplier
        fields = ('subitem', 'name', 'city', 'moq', 'unitprice', 'other')
        labels={
            'name': '供应商公司名称',
            'city': '地区',
            'moq': '最小起订量',
            'unitprice': '单价',
            'other': '其他'
        }

    def __init__(self, *args, **kwargs):
        super(SubItemSupplierForm, self).__init__(*args, **kwargs)
        self.fields['subitem'].widget = forms.HiddenInput()