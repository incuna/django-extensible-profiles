from django import forms
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import get_callable
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from incuna.utils.unique_id import generate_id

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
           del cleaned_data['password1']
           del cleaned_data['password2']

       return cleaned_data

    def save(self, commit=True):
       user = super(BasePasswordChangeForm, self).save(commit=False)
       if self.cleaned_data['password1'] and self.cleaned_data['password2']:
           user.set_password(self.cleaned_data['password1'])
       if commit:
           user.save()
           self.save_m2m()
       return user


class BaseProfileAdminForm(BasePasswordChangeForm):

    def clean_email(self):
        """Prevent account hijacking by disallowing duplicate emails."""
        email = self.cleaned_data.get('email', None)

        if email:
            users = Profile.objects.filter(email__iexact=email)
            if self.instance:
                users = users.exclude(pk=self.instance.pk)
            if users.count() > 0:
                raise forms.ValidationError(_('That email address is already in use.'))
        return email


class ProfileAdmin(ModelAdmin):
    add_form_template = None
    fieldsets = [
        (None, {
            'fields': ['email', #'password1', 'password2', 
                       'first_name','last_name',  ]
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

    #def get_fieldsets(self, request, obj=None):
    #    # Delay adding the password fields as they cause validation errors
    #    fieldsets =  super(ProfileAdmin, self).get_fieldsets(request, obj=obj)
    #    # Insert the password fields  
    #    fieldsets[0][1]['fields'][1:1] = ['password1', 'password2']

    #    return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        # Delay creation of the ProfileAdminForm until we have a 'final'
        # model to base it on

        class ProfileAdminForm(BaseProfileAdminForm):
            class Meta:
                model = Profile
        self.form = ProfileAdminForm

        # TODO: Delay adding the password fields as they cause validation errors
        if not 'password1' in self.fieldsets[0][1]['fields']:
            self.fieldsets[0][1]['fields'][1:1] = ['password1', 'password2']

        form = super(ProfileAdmin, self).get_form(request, obj=obj, **kwargs)

        form.base_fields['email'].required = True
        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True
        return form

    def save_form(self, request, form, change):
        """If this is an add then set the password."""
        user = super(ProfileAdmin, self).save_form(request, form, change)
        password = form.cleaned_data.get('password1', None);
        if password:
            user.set_password(password)
        return user


# Register extensions listed in the settings
PROFILE_EXTENSIONS = getattr(settings, 'PROFILE_EXTENSIONS', None)
if PROFILE_EXTENSIONS and not Profile._extensions_imported:
    Profile.register_extensions(*PROFILE_EXTENSIONS)
    Profile._extensions_imported = True

