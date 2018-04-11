from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def canViewOrder(self):
    return self.has_perm('crm.delete_order') or self.isManager()

def canViewCatelog(self):
    return self.has_perm('catalog.add_product')

def isManager(self):
    return self.has_perm('auth.change_user')


def isSales(self):
    return self.has_perm('crm.add_order') or self.isManager()

def isSalesManager(self):
    return self.has_perm('crm.delete_order') or self.isManager()

User.add_to_class("canViewOrder",canViewOrder)

User.add_to_class('isManager', isManager)

User.add_to_class('isSales', isSales)
User.add_to_class("isSalesManager", isSalesManager)
User.add_to_class('canViewCatelog', canViewCatelog)


