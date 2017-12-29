
from django.shortcuts import HttpResponse, render, redirect, reverse, get_object_or_404
from .forms import ItemForm, ItemPhotoForm, SubItemForm, SubItemPhotoForm, SubItemSupplierForm
from django.contrib import messages
# Create your views here.
from .models import Item, ItemPhoto, SubItem, SubItemSupplier, SubItemPhoto
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    items = Item.objects.all()

    paginator = Paginator(items, 25)

    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'items/list.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect(reverse('view_item', kwargs={'id':item.pk}))
    else:
        form = ItemForm()
        form.fields['user'].initial = request.user
    return render(request, 'items/add.html', {'form': form})

def view_item_edit(request, id):
    return view_item(request, id, True)
def view_item(request, id, editable = False):
    item = get_object_or_404(Item, pk=id)
    if editable is True:
        return render(request, 'items/view_edit.html', {'item': item, 'editable': editable})
    else:
        return render(request, 'items/view.html', {'item': item, 'editable': editable})

def edit_item(request, id):
    item = get_object_or_404(Item, pk=id)
    if request.method == 'POST':
        form = ItemForm(request.POST,instance=item)
        if form.is_valid():
            item = form.save()
            messages.success(request, '产品跟新成功！')

            return redirect(reverse('view_item', kwargs={'id':item.pk}))
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/edit.html', {'item': item, 'form': form})

def add_itemphoto(request, id):
    item = get_object_or_404(Item, pk=id)

    if request.method == 'POST':
        form = ItemPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            itemPhoto = form.save()
            return redirect(reverse('view_item', kwargs={'id': item.id}))
    else:
        form = ItemPhotoForm()
        form.fields['item'].initial = item

    return render(request, 'items/add_photo.html', {'item': item, 'form': form})

def delete_itemphoto(request, id):
    itemphoto = get_object_or_404(ItemPhoto, pk=id)
    itemphoto.delete()
    messages.success(request, '图片成功删除!')
    return redirect(reverse('view_item', kwargs={'id':itemphoto.item.pk}))

def add_subitem(request, id):
    item = get_object_or_404(Item, pk=id)

    if request.method == 'POST':
        form = SubItemForm(request.POST)
        if form.is_valid():
            subitem = form.save()
            messages.success(request, '成功添加新产品信息!')
            return redirect(reverse('view_item', kwargs={'id': item.pk}))
    else:
        form = SubItemForm()
        form.fields['user'].initial = request.user
        form.fields['item'].initial = item
    return render(request, 'subitems/add.html', {'item': item, 'form': form})

def edit_subitem(request, id):
    subitem = get_object_or_404(SubItem, pk=id)
    if request.method == 'POST':
        form = SubItemForm(request.POST, instance=subitem)
        if form.is_valid():
            item = form.save()
            messages.success(request, '产品跟新成功！')

            return redirect(reverse('view_item', kwargs={'id': subitem.item.pk}))
    else:
        form = SubItemForm(instance=subitem)
    return render(request, 'subitems/edit.html', {'subitem': subitem, 'form': form})

def add_subitem_photo(request, id):
    subitem = get_object_or_404(SubItem, pk=id)

    if request.method == 'POST':
        form = SubItemPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            subItemPhoto = form.save()
            return redirect(reverse('view_item', kwargs={'id': subitem.item.id}))
    else:
        form = SubItemPhotoForm()
        form.fields['subitem'].initial = subitem

    return render(request, 'subitems/add_photo.html', {'subitem': subitem, 'form': form})


def delete_subitemphoto(request, id):
    obj  = get_object_or_404(SubItemPhoto, pk=id)
    obj.delete()
    messages.success(request, '图片成功删除!')
    return redirect(reverse('view_item', kwargs={'id': obj.subitem.item.pk}))


def add_subitemsupplier(request, id):
    subitem  = get_object_or_404(SubItem, pk=id)

    if request.method == 'POST':
        form = SubItemSupplierForm(request.POST)
        if form.is_valid():
            subitemsupplier = form.save()
            messages.success(request, '成功添加供应商信息!')
            return redirect(reverse('view_item', kwargs={'id': subitemsupplier.subitem.item.pk}))
    else:
        form = SubItemSupplierForm()
        form.fields['subitem'].initial = subitem

    return render(request, 'subitemsuppliers/add.html', {'subitem': subitem, 'form': form})

def edit_subitemsupplier(request, id):
    subitemsupplier = get_object_or_404(SubItemSupplier, pk=id)
    if request.method == 'POST':
        form = SubItemSupplierForm(request.POST, instance=subitemsupplier)
        if form.is_valid():
            obj = form.save()
            messages.success(request, '供应商跟新成功！')
            return redirect(reverse('view_item', kwargs={'id': subitemsupplier.subitem.item.pk}))
    else:
        form = SubItemSupplierForm(instance=subitemsupplier)
    return render(request, 'subitemsuppliers/edit.html', {'subitemsupplier': subitemsupplier, 'form': form})

def delete_subitemsupplier(request, id):
    subitemsupplier = get_object_or_404(SubItemSupplier, pk=id)
    subitemsupplier.delete()
    messages.success(request, '供应商信息成功删除!')
    return redirect(reverse('view_item', kwargs={'id': subitemsupplier.subitem.item.pk}))


def view_subitem_edit(request, id):
    return view_subitem(request, id, True)
def view_subitem(request, id, editable=False):

    subitem = get_object_or_404(SubItem, pk=id)
    if editable is True:
        return render(request, 'subitems/view_edit.html', {'subitem': subitem, 'editable': editable })
    else:
        return render(request, 'subitems/view.html', {'subitem': subitem, 'editable': editable})
