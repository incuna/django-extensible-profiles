import re

from django.conf import settings
from django.core import exceptions
from django.db.models import get_model
from django.forms import fields

from profiles.models import Profile, BasePasswordChangeForm, EmailFormMixin
from profiles.modules.codes.models import Code

try:
    User = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
except AttributeError:
    from django.contrib.auth.models import User


class UserChangeForm(BasePasswordChangeForm):
    class Meta:
        model = User


class ProfileForm(EmailFormMixin, BasePasswordChangeForm):
    class Meta:
        model = Profile
        exclude = (
            'date_joined',
            'groups',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'password',
            'user_permissions',
            'username',
        )
    make_required = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for fname in self.make_required:
            try:
                self.fields[fname].required = True
            except KeyError:
                pass


class CodeField(fields.CharField):
    re_clean_code = re.compile('[^a-zA-Z0-9]+')

    def validate(self, value):
        super(CodeField, self).validate(value)

        value = self.re_clean_code.sub('', value)
        try:
            Code.objects.get(code=value)
        except Code.DoesNotExist:
            raise exceptions.ValidationError('Enter a valid registration code.')