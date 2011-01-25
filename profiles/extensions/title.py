from django.db import models
from django.utils.translation import ugettext_lazy as _


TITLE_CHOICES = [('Dr','Dr'),
                 ('Professor','Professor'),
                 ('Mr','Mr'),
                 ('Miss','Miss'),
                 ('Mrs','Mrs'),
                 ('Ms','Ms'),
                ]

def register(cls, admin_cls):
    cls.add_to_class('title', models.CharField(max_length=255, verbose_name=_('title'), null=True, blank=True, choices=TITLE_CHOICES))
    if admin_cls:
        admin_cls.list_display_filter += ['title', ]

        if admin_cls.fieldsets:
            fields = admin_cls.fieldsets[0][1]['fields']
            try:
                at = fields.index('first_name')
            except ValueError:
                at = len(fields)
            fields.insert(at, 'title')


