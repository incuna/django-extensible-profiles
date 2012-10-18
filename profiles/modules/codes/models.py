from django.db import models
from django.utils.safestring import mark_safe

class Code(models.Model):
    """
    Registration codes
    """
    code = models.CharField(max_length=255)

    class Meta:
        app_label = 'profiles'
        ordering = ('code',)

    def __unicode__(self):
        return mark_safe(self.code)