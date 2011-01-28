from django.db import models
from django.utils.translation import ugettext_lazy as _
from incuna.utils import find


def register(cls, admin_cls):
    cls.add_to_class('modified', models.DateTimeField(auto_now=True))

    if admin_cls:

        admin_cls.readonly_fields += ['modified', ]
        admin_cls.list_display += ['modified', ]
        if admin_cls.fieldsets:
           other_title = _('Other options')
           other_set =  find(lambda sets: sets[0] == other_title, admin_cls.fieldsets)
           if other_set:
               fields = other_set[1]['fields'] 
           else:
               fields = admin_cls.fieldsets[0][1]['fields']

           fields.insert(len(fields), 'modified')


