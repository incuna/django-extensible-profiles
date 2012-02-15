from django.contrib import admin
from django.db import models

from profiles.modules.addresses.models import Address


def register(cls, admin_cls):
    cls.add_to_class('addresses', models.ManyToManyField('profiles.Address', related_name='addresses', blank=True))

    if admin_cls:
        class AddressInline(admin.StackedInline):
            model = Address
            extra = 1

        admin_cls.inlines = admin_cls.inlines + [AddressInline]
