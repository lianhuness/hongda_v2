from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def canViewOrder(self):
    return self.has_perm('crm.delete_order')

def isManager(self):
    return self.has_perm('auth.change_user')


def isSales(self):
    return self.isManager() or self.has_perm('crm.add_order')



User.add_to_class("canViewOrder",canViewOrder)

User.add_to_class('isManager', isManager)

User.add_to_class('isSales', isSales)


