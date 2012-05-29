from django.db import models
from django.utils.translation import ugettext_lazy as _


def register(cls, admin_cls):
    cls.add_to_class('modified', models.DateTimeField(auto_now=True))

    if admin_cls:

        admin_cls.readonly_fields += ['modified']
        admin_cls.list_display += ['modified']
        if admin_cls.fieldsets:
            other_title = _('Other options')
            try:
                other_set = (s for s in admin_cls.fieldsets if lambda s: s[0] == other_title).next()
            except StopIteration:
                fields = admin_cls.fieldsets[0][1]['fields']
            else:
                fields = other_set[1]['fields']
            fields.append('modified')
