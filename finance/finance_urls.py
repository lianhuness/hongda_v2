# coding=utf-8
# author= YQZHU

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [

    url(r'^ranking/', include([
        url(r'^list_rules', views.list_rules, name='list_rules'),
        url(r'^add_rule', views.add_rule, name='add_rule'),
        url(r'^edit_rule/(?P<id>[0-9]+)$', views.edit_rule, name='edit_rule'),

        url(r'^my_yuangong', views.my_yuangong, name='my_yuangong'),
        url(r'^del_yuangong/(?P<id>[0-9]+)$', views.del_yuangong, name='del_yuangong'),
        url(r'^add_yuangong', views.add_yuangong, name='add_yuangong'),

        url(r'^list_weeks', views.list_weeks, name='list_weeks'),
        url(r'^add_week', views.add_week, name='add_week'),
        url(r'^edit_week/(?P<id>[0-9]+)$', views.edit_week, name='edit_week'),
        url(r'^view_week/(?P<id>[0-9]+)$', views.view_week, name='view_week'),
        url(r'^add_kaohe_record/(?P<id>[0-9]+)$', views.add_kaohe_record, name='add_kaohe_record'),
url(r'^del_kaohe_record/(?P<id>[0-9]+)$', views.del_kaohe_record, name='del_kaohe_record'),
    ]), name='ranking'),

]
