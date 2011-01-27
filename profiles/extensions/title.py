from django.db import models
from django.utils.translation import ugettext_lazy as _


def register(cls, admin_cls):
    cls.add_to_class('TITLE_CHOICES', [('Dr','Dr'),
                                       ('Professor','Professor'),
                                       ('Mr','Mr'),
                                       ('Miss','Miss'),
                                       ('Mrs','Mrs'),
                                       ('Ms','Ms'),
                                      ])
    cls.add_to_class('title', models.CharField(max_length=255, verbose_name=_('title'), null=True, blank=True, choices=cls.TITLE_CHOICES))

    from profiles.models import Profile
    get_full_name = Profile.get_full_name
    def get_full_name_title(self):
        full_name = get_full_name(self)
        if self.title:
            full_name = u'%s %s' % (self.title, full_name)

        return full_name
    cls.add_to_class('get_full_name', get_full_name_title)
    

    if admin_cls:
        admin_cls.list_display_filter += ['title', ]

        if admin_cls.fieldsets:
            fields = admin_cls.fieldsets[0][1]['fields']
            try:
                at = fields.index('first_name')
            except ValueError:
                at = len(fields)
            fields.insert(at, 'title')


