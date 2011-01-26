from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('options', models.ManyToManyField('profiles.Option', verbose_name=_('Opt-ins'), null=True, blank=True))

    if admin_cls:
        admin_cls.list_display_filter += ['options', ]

        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Opt-ins'), {
                    'fields': ['options',],
                    'classes': ('collapse',),
                }))

