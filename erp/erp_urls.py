# coding=utf-8
# author= YQZHU

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^jihuadan/', include([
        url(r'^$', views.list_jihuadan, name='list_jihuadan'),
        url(r'^view/(?P<id>[0-9]+)$', views.view_jihuadan, name='view_jihuadan'),
        url(r'^view_jhd_log/(?P<id>[0-9]+)$', views.view_jhd_log, name='view_jhd_log'),
        url(r'^add/(?P<id>[0-9]+)$', views.add_jihuadan, name='add_jihuadan'),
        url(r'^add_jhd_item/(?P<id>[0-9]+)$', views.add_jhd_item, name='add_jhd_item'),
        url(r'^del_jhd_item/(?P<id>[0-9]+)$', views.del_jhd_item, name='del_jhd_item'),

        url(r'^change_jhd_status/(?P<id>[0-9]+)/(?P<status>[A-Z]+)$', views.change_jhd_status, name='change_jhd_status'),
        url(r'^jhd_search', views.jhd_search, name='jhd_search'),
    ]), name='jihuadan'),


    url(r'^chejian/', include([
        url(r'^subproducts$', views.subproducts, name='subproducts'),
        url(r'^del_subproducts/(?P<id>[0-9]+)$', views.del_subproducts, name='del_subproducts'),
        url(r'^myitems', views.cj_myitems, name='myitems'),

]), name='chejian'),


]