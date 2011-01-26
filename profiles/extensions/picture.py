from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('picture', models.ImageField(verbose_name=_('your picture'), upload_to='images/profiles',blank=True,null=True,))

    if admin_cls:
        if admin_cls.fieldsets:
            fields = admin_cls.fieldsets[0][1]['fields']
            fields.insert(len(fields), 'picture')



