from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('codes', models.ManyToManyField('profiles.Code',
        verbose_name=_('Registration codes'), null=True, blank=True))

    if admin_cls:
        admin_cls.list_display_filter += ['codes', ]

        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Registration codes'), {
                    'fields': ['codes',],
                    'classes': ('collapse',),
                }))
            admin_cls.filter_horizontal = admin_cls.filter_horizontal + ('codes',)
