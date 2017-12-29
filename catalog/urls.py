# coding=utf-8
# author= YQZHU

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='items_list'),
    url(r'^item/', include([
        url(r'^view_edit/(?P<id>[0-9]+)$', views.view_item_edit, name='view_item_edit'),
        url(r'^view/(?P<id>[0-9]+)$', views.view_item, name='view_item'),
        url(r'^edit/(?P<id>[0-9]+)$', views.edit_item, name='edit_item'),
        url(r'^add$', views.add_item, name='add_item'),
    ]), name='items'),

    url(r'^itemphoto/', include([
        url(r'^delete/(?P<id>[0-9]+)$', views.delete_itemphoto, name='delete_itemphoto'),
        url(r'^add/(?P<id>[0-9]+)$', views.add_itemphoto, name='add_itemphoto'),
    ]), name='itemphoto'),

    url(r'^subitem/', include([
        url(r'^add/(?P<id>[0-9]+)$', views.add_subitem, name='add_subitem'),
        url(r'^edit/(?P<id>[0-9]+)$', views.edit_subitem, name='edit_subitem'),
        url(r'^addphoto/(?P<id>[0-9]+)$', views.add_subitem_photo, name='add_subitem_photo'),
        url(r'^deletephoto/(?P<id>[0-9]+)$', views.delete_subitemphoto, name='delete_subitemphoto'),
        url(r'^view_edit/(?P<id>[0-9]+)$', views.view_subitem_edit, name='view_subitem_edit'),
        url(r'^view/(?P<id>[0-9]+)$', views.view_subitem, name='view_subitem'),

        url(r'^subitemsupplier/', include([
            url(r'^edit/(?P<id>[0-9]+)$', views.edit_subitemsupplier, name='edit_subitemsupplier'),
            url(r'^add/(?P<id>[0-9]+)$', views.add_subitemsupplier, name='add_subitemsupplier'),
            url(r'^delete/(?P<id>[0-9]+)$', views.delete_subitemsupplier, name='delete_subitemsupplier'),
        ]), name='subitemsupplier'),
    ]), name='subitem'),
]