from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('address1', models.CharField(max_length=255, verbose_name=_('address'), null=True, blank=True))
    cls.add_to_class('address2', models.CharField(max_length=255, verbose_name=_('address 2'), null=True, blank=True))
    cls.add_to_class('city', models.CharField(max_length=255, verbose_name=_('town/city'), null=True, blank=True))
    cls.add_to_class('region', models.CharField(max_length=255, verbose_name=_('county/state/province'), null=True, blank=True))
    cls.add_to_class('postcode', models.CharField(max_length=15, verbose_name=_('postcode'), null=True, blank=True))
    cls.add_to_class('country', models.ForeignKey('countries.Country', null=True, blank=True))
    cls.add_to_class('telephone', models.CharField(max_length=32, verbose_name=_('telephone'), null=True, blank=True))

    if admin_cls:
        admin_cls.search_fields += ['address1', 'address2', 'city', 'region', 'postcode', 'telephone']
        admin_cls.list_display_filter += ['country', ]

        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Address'), {
                    'fields': ['address1', 'address2','city', 'region', 'postcode', 'country', 'telephone'],
                    'classes': ('collapse',),
                }))

