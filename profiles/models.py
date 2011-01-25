import hashlib,random 

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import get_callable
from django.core.exceptions import ImproperlyConfigured

from django import forms

from django.contrib import admin
from django.contrib.admin.options import *

from incuna.utils.unique_id import generate_id
from incuna.forms import PlainPasswordUserForm

class Profile(User):
    objects = UserManager()

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, ProfileAdmin)

    @classmethod
    def register_extensions(cls, *extensions):
        if not hasattr(cls, '_profile_extensions'):
            cls._profile_extensions = set()

        here = cls.__module__.split('.')[:-1]
        here_path = '.'.join(here + ['extensions'])
        #common_path = '.'.join(here[:-1] + ['extensions'])

        for ext in extensions:
            if ext in cls._profile_extensions:
                continue

            try:
                if isinstance(ext, basestring):
                    try:
                        fn = get_callable(ext + '.register', False)
                    except ImportError:
                        fn = get_callable('%s.%s.register' % ( here_path, ext ), False)
                        #try:
                        #    fn = get_callable('%s.%s.register' % ( here_path, ext ), False)
                        #except ImportError:
                        #    fn = get_callable('%s.%s.register' % ( common_path, ext ), False)
                # Not a string, so take our chances and just try to access "register"
                else:
                    fn = ext.register

                cls.register_extension(fn)
                cls._profile_extensions.add(ext)
            except Exception, e:
                raise ImproperlyConfigured("%s.register_extensions('%s') raised an '%s' exception" %
                                            (cls.__name__, ext, e.message))

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_id(first_name=self.first_name, last_name=self.last_name, email=self.email)

        super(Profile, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = super(User, self).get_full_name()
        if not full_name:
            return self.username

        #if self.title:
        #    full_name = u'%s %s' % (self.title, full_name)

        return full_name


    def get_profile(self):
        return self




#class ProfileForm(forms.ModelForm):
#   def clean_username(self):
#       return self.cleaned_data["username"].lower()


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
                                help_text = _("Enter the same password as above, for verification."))

    class Meta:
        model = Profile
        fields = ("email",)

    #def clean_username(self):
    #    username = self.cleaned_data["username"]
    #    try:
    #        User.objects.get(username=username)
    #    except User.DoesNotExist:
    #        return username
    #    raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


def encrypt_password(raw_password): 
    algo = 'sha1' 
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5] 
    hsh = hashlib.sha1(salt+raw_password).hexdigest() 
    return '%s$%s$%s' % (algo, salt, hsh) 

class ProfileAdmin(admin.ModelAdmin):
    form = forms.ModelForm
    unknown_fields = ['last_login', 'date_joined',]
    fieldsets = [
        (None, {
            'fields': ['email', 
                       'password', 'first_name','last_name', 'is_active',  ]
        }),
        (_('Other options'), {
            'classes': ['collapse',],
            'fields': unknown_fields,
        }),
    ]
    list_display = ['email', 'first_name', 'last_name', ]
    list_display_links = ['email',]
    search_fields = ['email',  'first_name', 'last_name',]
    readonly_fields = ['last_login', 'date_joined', ]
    list_filter = ['is_active', ]

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        form = super(ProfileAdmin, self).get_form(request, obj=obj, **kwargs)
        if obj is None:
            form.base_fields['password'].help_text = ""

        return form

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        obj = super(ProfileAdmin, self).save_form(request, form, change)
        if not change and obj.password:
            obj.password = encrypt_password(obj.password)
        return obj

