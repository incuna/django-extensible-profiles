import re

from django.core import exceptions
from django.forms import fields

from .models import Code


class CodeField(fields.CharField):
    re_clean_code = re.compile('[^a-zA-Z0-9]+')

    def validate(self, value):
        super(CodeField, self).validate(value)

        value = self.re_clean_code.sub('', value)
        try:
            Code.objects.get(code=value)
        except Code.DoesNotExist:
            raise exceptions.ValidationError('Enter a valid registration code.')