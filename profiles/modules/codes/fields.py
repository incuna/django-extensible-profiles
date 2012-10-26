import re

from django.core import exceptions
from django.forms import fields

from .models import Code


class CodeField(fields.CharField):
    def to_python(self, value):
        if not value:
            return value

        try:
            value = value.strip()
            value = Code.objects.get(code__iexact=value, is_active=True)
        except Code.DoesNotExist:
            raise exceptions.ValidationError('Enter a valid registration code.')
        return value