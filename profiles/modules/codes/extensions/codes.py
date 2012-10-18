from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('code', models.ForeignKey('profiles.Code',
        verbose_name=_('Registration code'), null=True, blank=True))

    if admin_cls:
        admin_cls.list_display_filter += ['code', ]

        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Registration code'), {
                    'fields': ['code',],
                    'classes': ('collapse',),
                }))
            admin_cls.filter_horizontal = admin_cls.filter_horizontal + ('code',)
