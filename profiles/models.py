import hashlib,random 

from django.db import transaction
from django.conf import settings

from django.utils.translation import ugettext, ugettext_lazy as _

import traceback
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.admin import UserAdmin, csrf_protect_m
from django.core.urlresolvers import get_callable
from django.core.exceptions import ImproperlyConfigured

from django import forms

from django.contrib import admin
from django.contrib.admin.options import *

from incuna.utils.unique_id import generate_id

if getattr(settings, 'AUTH_PROFILE_MODULE', False) and settings.AUTH_PROFILE_MODULE == "profiles.Profile":

    def get_profile(self):
        """
        Returns profile for this user. .
        """
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
            except Exception, e:
                raise 
                #raise ImproperlyConfigured("%s.register_extensions('%s') raised an '%s' exception %s" %
                #                            (cls.__name__, ext, e.message, traceback.format_exc()))

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_id(first_name=self.first_name, last_name=self.last_name, email=self.email)

        super(Profile, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = super(Profile, self).get_full_name()
        if not full_name:
            return self.username

        #if self.title:
        #    full_name = u'%s %s' % (self.title, full_name)

        return full_name


    def get_profile(self):
        return self

class ProfileForm(forms.ModelForm):
    def clean_email(self):
        """Prevent account hijacking by disallowing duplicate emails."""
        email = self.cleaned_data.get('email', None)
        
        if email:
            users = Profile.objects.filter(email__iexact=email)
            if self.instance:
                users = users.exclude(pk=self.instance.pk) 
            if users.count() > 0:
                raise forms.ValidationError(
                    ugettext("That email address is already in use."))

        return email



class ProfileAdmin(UserAdmin):
    form = ProfileForm
    add_form_template = None
    fieldsets = [
        (None, {
            'fields': ['email', 
                       'password', 'first_name','last_name',  ]
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
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        # Override the UserAdmin add view and return it's parent.
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        If this is an add then remove the password help_text.
        """
        # Override the UserAdmin add view and return it's parent.
        form = super(UserAdmin, self).get_form(request, obj=obj, **kwargs)
        if obj is None:
            form.base_fields['password'].help_text = ""

        form.base_fields['email'].required = True
        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True

        return form

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # Override the UserAdmin add view and return it's parent.
        return super(UserAdmin, self).add_view(request, form_url, extra_context)

    def save_form(self, request, form, change):
        """
        If this is an add then set the password .
        """
        user = super(ProfileAdmin, self).save_form(request, form, change)
        if not change and user.password:
            user.set_password(user.password)
        return user


# Register extensions listed in the settings
PROFILE_EXTENSIONS = getattr(settings, 'PROFILE_EXTENSIONS', None)
if PROFILE_EXTENSIONS and not Profile._extensions_imported:
    Profile.register_extensions(*PROFILE_EXTENSIONS)
    Profile._extensions_imported = True
