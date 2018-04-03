# coding=utf-8
# author= YQZHU

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
url(r'^$', views.catelog_home, name='catelog_home'),
url(r'^add_product', views.add_product, name='add_product'),
url(r'^view_product/(?P<id>[0-9]+)$', views.view_product, name='view_product'),
url(r'^edit_product/(?P<id>[0-9]+)$', views.edit_product, name='edit_product'),
url(r'^add_product_log/(?P<id>[0-9]+)$', views.view_product, name='add_product_log'),

]