from django.db import models
from django.utils.translation import ugettext_lazy as _

from incuna.db.models import Orderable
from profiles.models import Profile

class ProfileFieldsChoices(object):
    """
    Iterable that will yield Profile fields as choices. 
    This is necessary to delay accessing the Profile class until it has been defined.
    """

    def __init__(self ):
        self.count = 0

    def next(self):
        if self.count >= len(Profile._meta.fields):
            self.count = 0
            raise StopIteration
        else:
            c = self.count
            self.count += 1
            return self.__getitem__(c)

    def __getitem__(self, item):
        field = Profile._meta.fields[item]
        return (field.name, unicode(field.verbose_name))

    def __iter__(self):
        return self

class Notification(Orderable):
    """
    Patient notification methods (e.g. Email, Mobile,)
    """

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    field_name = models.CharField(max_length=31, null=True, blank=True, 
                                  choices=ProfileFieldsChoices(),
                                  help_text=_('Name of the Profile field required for this notification.'))
   
    class Meta:
        app_label = 'profiles'
        ordering = ('sort_order',)
   
    def __unicode__(self):
        return self.name

