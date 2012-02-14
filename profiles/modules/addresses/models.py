from django.db import models
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):
    profile = models.ForeignKey('profiles.Profile')
    address1 = models.CharField(max_length=255, verbose_name=_('address'), null=True, blank=True)
    address2 = models.CharField(max_length=255, verbose_name=_('address 2'), null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name=_('town/city'), null=True, blank=True)
    region = models.CharField(max_length=255, verbose_name=_('county/state/province'), null=True, blank=True)
    postcode = models.CharField(max_length=15, verbose_name=_('postcode'), null=True, blank=True)
    country = models.ForeignKey('countries.Country', null=True, blank=True)
    telephone = models.CharField(max_length=32, verbose_name=_('telephone'), null=True, blank=True)

    class Meta:
        app_label = 'profiles'
        verbose_name_plural = 'addresses'

    def __unicode__(self):
        return self.address1
