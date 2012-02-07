from django import forms
from django.conf import settings
from django.db.models import get_model
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _

from profiles.models import Profile


try:
    user_model = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
except AttributeError:
    from django.contrib.auth.models import User as user_model

class UserChangeForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), required=False,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'),
                                required=False, widget=forms.PasswordInput)

    class Meta:
        model = user_model

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1', '')
        password2 = cleaned_data.get('password2', '')
        if password1 != password2:
            msg = u'The password fields did not match.'
            self._errors['password2'] = ErrorList([msg])
            del cleaned_data['password1']
            del cleaned_data['password2']

        return cleaned_data

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if self.cleaned_data['password1'] and self.cleaned_data['password2']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


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

