from django import forms
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import get_callable
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from unique_id import generate_id

ModelAdmin = get_callable(getattr(settings, 'PROFILE_MODELADMIN_CLASS', 'django.contrib.admin.ModelAdmin'))
if getattr(settings, 'AUTH_PROFILE_MODULE', False) and settings.AUTH_PROFILE_MODULE == "profiles.Profile":
    def get_profile(self):
        """Returns profile for this user."""
        return self.profile
    User.get_profile = get_profile


class Profile(User):
    objects = UserManager()
    _extensions_imported = False

    @classmethod
    def remove_field(cls, f_name):
        # Removes the field form local fields list
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name):
            delattr(cls, f_name)

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, ProfileAdmin)

    @classmethod
    def register_extensions(cls, *extensions):
        if not hasattr(cls, '_profile_extensions'):
            cls._profile_extensions = set()

        here = cls.__module__.split('.')[:-1]
        here_path = '.'.join(here + ['extensions'])

        for ext in extensions:
            if ext in cls._profile_extensions:
                continue

            try:
                if isinstance(ext, basestring):
                    try:
                        fn = get_callable(ext + '.register', False)
                    except ImportError:
                        fn = get_callable('%s.%s.register' % ( here_path, ext ), False)
                # Not a string, so take our chances and just try to access "register"
                else:
                    fn = ext.register

                cls.register_extension(fn)
                cls._profile_extensions.add(ext)
            except Exception:
                raise

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_id(first_name=self.first_name,
                                        last_name=self.last_name, email=self.email)
        super(Profile, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = super(Profile, self).get_full_name()
        if not full_name:
            return self.username
        return full_name

    def get_profile(self):
        return self

# This form is here to avoid a cyclic import between models and forms
class BasePasswordChangeForm(forms.ModelForm):
    """
    Model form that includes password fields and sets password on save.
    """
    password1 = forms.CharField(label=_('Password'), required=False,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'),
                                required=False, widget=forms.PasswordInput)

    def clean(self):
       cleaned_data = self.cleaned_data
       password1 = cleaned_data.get('password1', '')
       password2 = cleaned_data.get('password2', '')
       if password1 != password2:
           msg = u'The password fields did not match.'
           self._errors['password2'] = ErrorList([msg])
           if 'password1' in cleaned_data.keys():
               del cleaned_data['password1']
           if 'password2' in cleaned_data.keys():
               del cleaned_data['password2']

       return cleaned_data

    def save(self, commit=True):
       user = super(BasePasswordChangeForm, self).save(commit=False)
       password = self.cleaned_data.get('password1', None)
       if password:
           user.set_password(password)
       if commit:
           user.save()
           self.save_m2m()
       return user


class EmailFormMixin(object):
    """
    Form mixin to ensure that the email is unique.
    """
    def clean_email(self):
        """Prevent account hijacking by disallowing duplicate emails."""
        email = self.cleaned_data.get('email', None)

        if email:
            users = User.objects.filter(email__iexact=email)
            if self.instance:
                users = users.exclude(pk=self.instance.pk)
            if users.count() > 0:
                raise forms.ValidationError(_('That email address is already in use.'))
        return email


class ProfileAdminForm(EmailFormMixin, BasePasswordChangeForm):
    pass


class ProfileAdmin(ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['email', 'first_name','last_name',  ]
        }),
        (_('Other options'), {
            'classes': ['collapse',],
            'fields': ['is_active', 'last_login', 'date_joined',],
        }),
    ]
    list_display = ['email', 'first_name', 'last_name', ]
    list_display_links = ['email',]
    search_fields = ['email',  'first_name', 'last_name',]
    readonly_fields = ['last_login', 'date_joined', ]
    list_filter = ['is_active', ]
    list_display_filter = []
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['email',]

    required_fields = ['email', 'first_name', 'last_name']

    def get_form(self, request, obj=None, **kwargs):

        if not issubclass(self.form, ProfileAdminForm):
            # Delay setting the ProfileAdminForm.
            # If form is added to the ProfileAdmin class then it cause 
            # validation error due to the form fields and admin fieldsets 
            # not being consistent.

            self.form = ProfileAdminForm

            # Delay adding the password fields until the form is set.
            fields = self.fieldsets[0][1]['fields']
            try:
                index = fields.index('email') + 1
            except ValueError:
                index = len(fields)
            if not 'password1' in fields:
                fields[index:index] = ['password1', 'password2']

        # Create the form 
        form = super(ProfileAdmin, self).get_form(request, obj=obj, **kwargs)

        # Set required fields
        for fname in self.required_fields:
            form.base_fields[fname].required = True

        return form


# Register extensions listed in the settings
PROFILE_EXTENSIONS = getattr(settings, 'PROFILE_EXTENSIONS', None)
if PROFILE_EXTENSIONS and not Profile._extensions_imported:
    Profile.register_extensions(*PROFILE_EXTENSIONS)
    Profile._extensions_imported = True
