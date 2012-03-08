from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from profiles.modules.addresses.models import Address


def register(cls, admin_cls):
    cls.add_to_class('addresses', models.ManyToManyField('profiles.Address', related_name='addresses', blank=True))

    if admin_cls:
        admin_cls.fieldsets += [(_('Other addresses'), {
            'classes': ['collapse',],
            'fields': ['addresses'],
        })]
        admin_cls.filter_horizontal += ('addresses',)
