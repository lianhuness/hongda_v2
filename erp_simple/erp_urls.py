# coding=utf-8
# author= YQZHU

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^jihuadan/', include([
        url(r'^$', views.list_jihuadan, name='erp_list_jihuadan'),
        # url(r'^my_jhd$', views.my_jhd, name='erp_my_jihuadan'),
        url(r'^my_jhd/(?P<show>[A-Z]+$)', views.my_jhd, name='erp_my_jihuadan'),
        url(r'^add/(?P<id>[0-9]+$)', views.add_jihuadan, name='erp_add_jihuadan'),
        url(r'^view/(?P<id>[0-9]+$)', views.view_jihuadan, name='erp_view_jihuadan'),

        url(r'^add_log/(?P<id>[0-9]+$)', views.add_jhd_log, name='erp_add_jhd_log'),
        url(r'^add_file/(?P<id>[0-9]+$)', views.add_jhd_file, name='erp_add_jhd_file'),

        url(r'^delete/(?P<id>[0-9]+$)', views.delete_jihuadan, name='erp_delete_jhd'),
        url(r'^complete/(?P<id>[0-9]+$)', views.complete_jihuadan, name='erp_complete_jhd'),
    ]), name='jihuadan'),

    url(r'^houquan/', include([
        url(r'^$', views.houquan_list_liuchandan, name='erp_houquan_list_liuchandan'),
        url(r'^addliuchendan$', views.houquan_add_liuchendan, name='erp_houquan_add_liuchendan'),
        url(r'^view/(?P<id>[0-9]+$)', views.houquan_view_liuchendan, name='erp_houquan_view_liuchendan'),
        url(r'^edit/(?P<id>[0-9]+$)', views.houquan_edit_liuchendan, name='erp_houquan_edit_liuchendan'),


    ])),

    url(r'^erp/', include([
        url(r'^list_all_jhd', views.list_all_jhd, name='list_all_jhd'),
        url(r'^search_jhd$', views.search_jhd, name='erp_search_jhd'),

    ])),



#     url(r'^jihuadan/', include([
#         url(r'^$', views.list_jihuadan, name='list_jihuadan'),
#         url(r'^view/(?P<id>[0-9]+)$', views.view_jihuadan, name='view_jihuadan'),
#         url(r'^view_jhd_log/(?P<id>[0-9]+)$', views.view_jhd_log, name='view_jhd_log'),
#         url(r'^add/(?P<id>[0-9]+)$', views.add_jihuadan, name='add_jihuadan'),
#         url(r'^add_jhd_item/(?P<id>[0-9]+)$', views.add_jhd_item, name='add_jhd_item'),
#         url(r'^del_jhd_item/(?P<id>[0-9]+)$', views.del_jhd_item, name='del_jhd_item'),
#
#         url(r'^change_jhd_status/(?P<id>[0-9]+)/(?P<status>[A-Z]+)$', views.change_jhd_status, name='change_jhd_status'),
#         url(r'^jhd_search', views.jhd_search, name='jhd_search'),
#     ]), name='jihuadan'),
#
#
#     url(r'^chejian/', include([
#         url(r'^subproducts$', views.subproducts, name='subproducts'),
#         url(r'^del_subproducts/(?P<id>[0-9]+)$', views.del_subproducts, name='del_subproducts'),
#         url(r'^myitems', views.cj_myitems, name='myitems'),
#
# ]), name='chejian'),

    ]
