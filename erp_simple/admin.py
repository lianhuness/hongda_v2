# -*- coding: UTF-8 -*-

from django.contrib import admin

# Register your models here.


from .models import HouquanLiuchen


# Blog模型的管理器
class HouquanLiuchenAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'caption', 'author', 'publish_time')


# 在admin中注册绑定
admin.site.register(HouquanLiuchen, HouquanLiuchenAdmin)
