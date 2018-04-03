# coding=utf-8
# author= YQZHU

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^home$', views.crm_home, name='crm_home'),
    url(r'^daily_report', views.daily_report, name='daily_report'),

    url(r'^clients/', include([
        url(r'^$', views.list_all_clients, name='list_all_clients'),
        # url(r'^list_client/(?P<level>[0-9]+)$', views.list_clients, name='list_clients'),
        url(r'^view/(?P<id>[0-9]+)$', views.view_client, name='view_client'),
        url(r'^viewlog/(?P<id>[0-9]+)$', views.view_client_log, name='view_client_log'),
        url(r'^edit/(?P<id>[0-9]+)$', views.edit_client, name='edit_client'),
        url(r'^add$', views.add_client, name='add_client'),
        url(r'^addfile/(?P<id>[0-9]+)$', views.add_client_file, name='add_client_file'),
        url(r'^deleteclientfile/(?P<id>[0-9]+)$', views.del_client_file, name='del_client_file'),

        url(r'^addcontactor/(?P<id>[0-9]+)$', views.add_contactor, name='add_contactor'),
        url(r'^editcontactor/(?P<id>[0-9]+)$', views.edit_contactor, name='edit_contactor'),

        url(r'addnote/(?P<id>[0-9]+)$', views.add_client_log, name='add_client_log'),
        url(r'changeuser/(?P<id>[0-9]+)$', views.change_client_rep, name='change_client_rep'),
    ]), name='clients'),

    # url(r'^color/', include([
    #     url(r'^$', views.list_colors, name='list_colors'),
    #     url(r'^delete/(?P<id>[0-9]+)$', views.delete_color, name='delete_color'),
    #     url(r'^add/(?P<id>[0-9]+)$', views.add_color, name='add_color'),
    #     url(r'^edit/(?P<id>[0-9]+)$', views.edit_color, name='edit_color'),
    # ]), name='colors'),


    url(r'^orders/', include([
        url(r'^$', views.list_orders, name='list_orders'),
        url(r'^view/(?P<id>[0-9]+)$', views.view_order, name='view_order'),
        url(r'^edit/(?P<id>[0-9]+)$', views.edit_order, name='edit_order'),
        url(r'^add/(?P<id>[0-9]+)$', views.add_order, name='add_order'),
        url(r'^crm_search', views.crm_search, name='crm_search'),

        url(r'^add_expense/(?P<id>[0-9]+)$', views.add_order_expense, name='add_order_expense'),
        url(r'^expense_list$', views.expense_list, name='expense_list'),
        url(r'^del_expense/(?P<id>[0-9]+)$', views.del_expense, name='del_expense'),
    ]), name='orders'),
]