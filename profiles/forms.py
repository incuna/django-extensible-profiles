from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from models import Profile
from incuna.forms.users import UserChangeForm

class ProfileForm(UserChangeForm):
    class Meta:
        model = Profile
        exclude = ('username', 'password', 
                   'is_staff', 'is_active', 'is_superuser', 
                   'last_login', 'date_joined', 
                   'user_permissions', 'groups',
                  )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = self.fields['first_name'].required = self.fields['last_name'].required = True

    def clean_email(self):
        """Prevent account hijacking by disallowing duplicate emails."""
        email = self.cleaned_data.get('email', None)
        
        if email:
            users = Profile.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                users = users.exclude(pk=self.instance.pk) 
            if users.count() > 0:
                raise forms.ValidationError(
                    ugettext("That email address is already in use."))

        return email

