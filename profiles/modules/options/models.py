from django.db import models
from django.utils.safestring import mark_safe

from incuna.db.models import Orderable

class Option(Orderable):
    """
    User options (op-ins)
    """
    name = models.CharField(max_length=150)
   
    class Meta:
        app_label = 'profiles'
        ordering = ('sort_order',)
   
    def __unicode__(self):
        return mark_safe(self.name)

