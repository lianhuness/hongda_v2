# -*- coding: UTF-8 -*-
from django.shortcuts import HttpResponse, render, redirect, reverse, get_object_or_404
from django.contrib import messages
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import  Product
from django import forms
from django.contrib.auth.decorators import permission_required



class ProductSearchForm(forms.Form):
    user = forms.CharField(label=u'创建人', required=False)
    catelog = forms.CharField(label=u'产品分类', required=False)
    name = forms.CharField(label=u'名称', required=False)
    material = forms.CharField(label=u'材料', required=False)


@permission_required('catalog.add_product')
def catelog_home(request):
    products = []
    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            products = Product.objects
            if form.cleaned_data['catelog']:
                products = products.filter(catelog__contains=form.cleaned_data['catelog'])
            if form.cleaned_data['name']:
                products = products.filter(name__contains=form.cleaned_data['name'])
            if form.cleaned_data['material']:
                products = products.filter(material__contains=form.cleaned_data['material'])
            if form.cleaned_data['user']:
                products = products.filter(user__username=form.cleaned_data['user'])
            products = products.all()
    else:
        form = ProductSearchForm()
        products = Product.objects.all()

    return render(request, 'catelogs/catelog_home.html', {'products': products, 'form': form})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

@permission_required('catalog.add_product')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            product.addLog(request, 'Product Created!')
            return redirect(reverse('view_product', kwargs={'id': product.id}))
    else:
        form = ProductForm()
        form.fields['user'].initial = request.user

    return render(request, 'catelogs/add_product.html',{ 'form': form})

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # import pdb
            # pdb.set_trace()
            product = form.save()
            msg = ""
            for fld in form.changed_data:
                msg = "%s, %s"%(msg, "%s from %s to %s"%(fld, form.initial[fld], form.cleaned_data[fld]))
            if len(msg) > 0:
                product.addLog(request, 'Product Information Updated! %s '%msg )
            return redirect(reverse('view_product', kwargs={'id': product.id}))
    else:
        form = ProductForm(instance=product)

    return render(request, 'catelogs/edit_product.html',{ 'form': form, 'product': product})


from .models import ProductLog
class ProductLogForm(forms.ModelForm):
    class Meta:
        model = ProductLog
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super(ProductLogForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['product'].widget = forms.HiddenInput()

def view_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        addlogform = ProductLogForm(request.POST, request.FILES)
        if addlogform.is_valid():
            messages.success(request, 'Add log success.')
            addlogform.save()
            return redirect(reverse('view_product', kwargs={'id': product.id}))
    else:
        addlogform = ProductLogForm()
        addlogform.fields['user'].initial = request.user
        addlogform.fields['product'].initial = product

    return render(request, 'catelogs/view_product.html', {'p': product, 'form': addlogform})



def add_product_log(request,id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductLogForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, 'Add log success.')
            form.save()

    return redirect(reverse('view_product', kwargs={'id': product.id}))

# class CatelogForm(forms.ModelForm):
#     class Meta:
#         model = CatelogGroup
#         fields = "__all__"
#     def __init__(self, *args, **kwargs):
#         super(CatelogForm, self).__init__(*args, **kwargs)
#         self.fields['user'].widget = forms.HiddenInput()
#
#
# def add_catelog(request):
#     if request.method == 'POST':
#         form = CatelogForm(request.POST, request.FILES)
#         if form.is_valid():
#             catelog = form.save()
#             return redirect(reverse('view_catelog', kwargs={'id': catelog.id}))
#     else:
#         form = CatelogForm()
#         form.fields['user'].initial = request.user
#     return render(request, 'catelogs/add_catelog.html', {'form': form})
#
# def edit_catelog(request, id):
#     catelog = get_object_or_404(CatelogGroup, pk=id)
#     if request.method == 'POST':
#         form = CatelogForm(request.POST, request.FILES, instance=catelog)
#         if form.is_valid():
#             catelog = form.save()
#             return redirect(reverse('view_catelog', kwargs={'id': catelog.id}))
#     else:
#         form = CatelogForm(instance=catelog)
#     return render(request, 'catelogs/edit_catelog.html', {'form': form, 'catelog': catelog})
#
# def view_catelog(request, id):
#     catelog = get_object_or_404(CatelogGroup, pk=id)
#     return render(request, 'catelogs/view_catelog.html', {'catelog': catelog})
#
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model= Product
#         fields = "__all__"
#     def __init__(self, *args, **kwargs):
#         super(ProductForm, self).__init__(*args, **kwargs)
#         self.fields['user'].widget = forms.HiddenInput()
#
# def add_product(request, id):
#     catelog = get_object_or_404(CatelogGroup, pk=id)
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save()
#             return redirect(reverse('view_product', kwargs={'id': product.id}))
#     else:
#         form = ProductForm()
#         form.fields['user'].initial = request.user
#         form.fields['catelog'].initial = catelog
#
#     return render(request, 'catelogs/add_product.html', {'catelog': catelog, 'form': form})
#
# def edit_product(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             product = form.save()
#             return redirect(reverse('view_product', kwargs={'id': product.id}))
#     else:
#         form = ProductForm(instance=product)
#     return render(request, 'catelogs/edit_product.html', {'product': product, 'form': form})
#
# def view_product(request, id):
#     product = get_object_or_404(Product, pk=id)
#     return render(request, 'catelogs/view_product.html', {'product': product,})
#
#
# class ProductSourceForm(forms.ModelForm):
#     class Meta:
#         model= ProductSource
#         fields = "__all__"
#     def __init__(self, *args, **kwargs):
#         super(ProductSourceForm, self).__init__(*args, **kwargs)
#
# def add_supply(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "POST":
#         form = ProductSourceForm(request.POST, request.FILES)
#         if form.is_valid():
#             sp = form.save()
#             return redirect(reverse('view_product', kwargs={'id': sp.product.id}))
#     else:
#         form = ProductSourceForm()
#         form.fields['product'].initial = product
#     return render(request, 'catelogs/add_supply.html', {'product': product, 'form': form})
#
# def edit_supply(request, id):
#     productsource = get_object_or_404(ProductSource, pk=id)
#     if request.method == "POST":
#         form = ProductSourceForm(request.POST, request.FILES, instance=productsource)
#         if form.is_valid():
#             sp = form.save()
#             return redirect(reverse('view_product', kwargs={'id': sp.product.id}))
#     else:
#         form = ProductSourceForm(instance=productsource)
#     return render(request, 'catelogs/edit_supply.html.', {'sp': productsource, 'form': form})
#


# def index(request):
#     items = Item.objects.all()
#
#     paginator = Paginator(items, 25)
#
#     page = request.GET.get('page')
#
#     try:
#         items = paginator.page(page)
#     except PageNotAnInteger:
#         items = paginator.page(1)
#     except EmptyPage:
#         items = paginator.page(paginator.num_pages)
#
#     return render(request, 'items/list.html', {'items': items})
#
# def add_item(request):
#     if request.method == 'POST':
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             item = form.save()
#             return redirect(reverse('view_item', kwargs={'id':item.pk}))
#     else:
#         form = ItemForm()
#         form.fields['user'].initial = request.user
#     return render(request, 'items/add.html', {'form': form})
#
# def view_item_edit(request, id):
#     return view_item(request, id, True)
# def view_item(request, id, editable = False):
#     item = get_object_or_404(Item, pk=id)
#     if editable is True:
#         return render(request, 'items/view_edit.html', {'item': item, 'editable': editable})
#     else:
#         return render(request, 'items/view.html', {'item': item, 'editable': editable})
#
# def edit_item(request, id):
#     item = get_object_or_404(Item, pk=id)
#     if request.method == 'POST':
#         form = ItemForm(request.POST,instance=item)
#         if form.is_valid():
#             item = form.save()
#             messages.success(request, '产品跟新成功！')
#
#             return redirect(reverse('view_item', kwargs={'id':item.pk}))
#     else:
#         form = ItemForm(instance=item)
#     return render(request, 'items/edit.html', {'item': item, 'form': form})
#
# def add_itemphoto(request, id):
#     item = get_object_or_404(Item, pk=id)
#
#     if request.method == 'POST':
#         form = ItemPhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             itemPhoto = form.save()
#             return redirect(reverse('view_item', kwargs={'id': item.id}))
#     else:
#         form = ItemPhotoForm()
#         form.fields['item'].initial = item
#
#     return render(request, 'items/add_photo.html', {'item': item, 'form': form})
#
# def delete_itemphoto(request, id):
#     itemphoto = get_object_or_404(ItemPhoto, pk=id)
#     itemphoto.delete()
#     messages.success(request, '图片成功删除!')
#     return redirect(reverse('view_item', kwargs={'id':itemphoto.item.pk}))
#
# def add_subitem(request, id):
#     item = get_object_or_404(Item, pk=id)
#
#     if request.method == 'POST':
#         form = SubItemForm(request.POST)
#         if form.is_valid():
#             subitem = form.save()
#             messages.success(request, '成功添加新产品信息!')
#             return redirect(reverse('view_item', kwargs={'id': item.pk}))
#     else:
#         form = SubItemForm()
#         form.fields['user'].initial = request.user
#         form.fields['item'].initial = item
#     return render(request, 'subitems/add.html', {'item': item, 'form': form})
#
# def edit_subitem(request, id):
#     subitem = get_object_or_404(SubItem, pk=id)
#     if request.method == 'POST':
#         form = SubItemForm(request.POST, instance=subitem)
#         if form.is_valid():
#             item = form.save()
#             messages.success(request, '产品跟新成功！')
#
#             return redirect(reverse('view_item', kwargs={'id': subitem.item.pk}))
#     else:
#         form = SubItemForm(instance=subitem)
#     return render(request, 'subitems/edit.html', {'subitem': subitem, 'form': form})
#
# def add_subitem_photo(request, id):
#     subitem = get_object_or_404(SubItem, pk=id)
#
#     if request.method == 'POST':
#         form = SubItemPhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             subItemPhoto = form.save()
#             return redirect(reverse('view_item', kwargs={'id': subitem.item.id}))
#     else:
#         form = SubItemPhotoForm()
#         form.fields['subitem'].initial = subitem
#
#     return render(request, 'subitems/add_photo.html', {'subitem': subitem, 'form': form})
#
#
# def delete_subitemphoto(request, id):
#     obj  = get_object_or_404(SubItemPhoto, pk=id)
#     obj.delete()
#     messages.success(request, '图片成功删除!')
#     return redirect(reverse('view_item', kwargs={'id': obj.subitem.item.pk}))
#
#
# def add_subitemsupplier(request, id):
#     subitem  = get_object_or_404(SubItem, pk=id)
#
#     if request.method == 'POST':
#         form = SubItemSupplierForm(request.POST)
#         if form.is_valid():
#             subitemsupplier = form.save()
#             messages.success(request, '成功添加供应商信息!')
#             return redirect(reverse('view_item', kwargs={'id': subitemsupplier.subitem.item.pk}))
#     else:
#         form = SubItemSupplierForm()
#         form.fields['subitem'].initial = subitem
#
#     return render(request, 'subitemsuppliers/add.html', {'subitem': subitem, 'form': form})
#
# def edit_subitemsupplier(request, id):
#     subitemsupplier = get_object_or_404(SubItemSupplier, pk=id)
#     if request.method == 'POST':
#         form = SubItemSupplierForm(request.POST, instance=subitemsupplier)
#         if form.is_valid():
#             obj = form.save()
#             messages.success(request, '供应商跟新成功！')
#             return redirect(reverse('view_item', kwargs={'id': subitemsupplier.subitem.item.pk}))
#     else:
#         form = SubItemSupplierForm(instance=subitemsupplier)
#     return render(request, 'subitemsuppliers/edit.html', {'subitemsupplier': subitemsupplier, 'form': form})
#
# def delete_subitemsupplier(request, id):
#     subitemsupplier = get_object_or_404(SubItemSupplier, pk=id)
#     subitemsupplier.delete()
#     messages.success(request, '供应商信息成功删除!')
#     return redirect(reverse('view_item', kwargs={'id': subitemsupplier.subitem.item.pk}))
#
#
# def view_subitem_edit(request, id):
#     return view_subitem(request, id, True)
# def view_subitem(request, id, editable=False):
#
#     subitem = get_object_or_404(SubItem, pk=id)
#     if editable is True:
#         return render(request, 'subitems/view_edit.html', {'subitem': subitem, 'editable': editable })
#     else:
#         return render(request, 'subitems/view.html', {'subitem': subitem, 'editable': editable})
