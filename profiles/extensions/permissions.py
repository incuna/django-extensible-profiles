from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    if admin_cls:
        admin_cls.list_display_filter += ['is_staff', 'groups', ]
        if admin_cls.fieldsets:
            admin_cls.fieldsets.append(
                (_('Permissions'), { 'fields': ('is_staff', 'groups'), 'classes': ('collapse',), })
            )

