from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('notifications', models.ManyToManyField('profiles.Notification', verbose_name=_('Keep me up-to-date'), 
                                                             null=True, blank=True))

    if admin_cls:
        admin_cls.list_display_filter += ['notifications', ]
        admin_cls.filter_horizontal += ('notifications',)

        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Notifications'), {
                    'fields': ['notifications',],
                    'classes': ('collapse',),
                }))


