from django.conf import settings
from django.db.models import get_model

from profiles.models import Profile, BasePasswordChangeForm, EmailFormMixin

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

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
