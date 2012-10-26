import re

from django.core import exceptions
from django.forms import fields

from .models import Code


class CodeField(fields.CharField):
    re_clean_code = re.compile('[^a-zA-Z0-9]+')

    def to_python(self, value):
        if not value:
            return value

        try:
            value = self.re_clean_code.sub('', value)
            value = Code.objects.get(code__iexact=value, is_active=True)
        except Code.DoesNotExist:
            raise exceptions.ValidationError('Enter a valid registration code.')
        return value