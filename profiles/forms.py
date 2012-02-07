from django import forms
from django.utils.translation import ugettext as _
from incuna.forms.users import UserChangeForm

from profiles.models import Profile


class ProfileForm(UserChangeForm):
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

    def clean_email(self):
        """Prevent account hijacking by disallowing duplicate emails."""
        email = self.cleaned_data.get('email', None)

        if email:
            users = Profile.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                users = users.exclude(pk=self.instance.pk)
            if users.count() > 0:
                raise forms.ValidationError(_('That email address is already in use.'))

        return email

