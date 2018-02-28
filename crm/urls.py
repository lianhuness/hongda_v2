# coding=utf-8
# author= YQZHU

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^home$', views.crm_home, name='crm_home'),

    url(r'^clients/', include([
        url(r'^$', views.list_all_clients, name='list_all_clients'),
        url(r'^list_client/(?P<level>[0-9]+)$', views.list_clients, name='list_clients'),
        url(r'^view/(?P<id>[0-9]+)$', views.view_client, name='view_client'),
        url(r'^viewlog/(?P<id>[0-9]+)$', views.view_client_log, name='view_client_log'),
        url(r'^edit/(?P<id>[0-9]+)$', views.edit_client, name='edit_client'),
        url(r'^add$', views.add_client, name='add_client'),

        url(r'^addcontactor/(?P<id>[0-9]+)$', views.add_contactor, name='add_contactor'),
        url(r'^editcontactor/(?P<id>[0-9]+)$', views.edit_contactor, name='edit_contactor'),

        url(r'addnote/(?P<id>[0-9]+)$', views.add_client_log, name='add_client_log'),

    ]), name='clients'),

    url(r'^orders/', include([
        url(r'^$', views.list_orders, name='list_orders'),
        url(r'^view/(?P<id>[0-9]+)$', views.view_order, name='view_order'),
        url(r'^edit/(?P<id>[0-9]+)$', views.edit_order, name='edit_order'),
        url(r'^add/(?P<id>[0-9]+)$', views.add_order, name='add_order'),
        url(r'^crm_search', views.crm_search, name='crm_search'),
    ]), name='orders'),
]