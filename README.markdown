## Extensible user profiles for Django

This project provides a base `Profile` model that relates to the built-in `auth.User` model and provides hooks for adding any number of feature extensions. A number of example extensions (address details, avatar, etc) are included.

The basic concept (and some code) is borrowed from the [FeinCMS](https://github.com/feincms/feincms) Page model.

### Usage

To use the profiles module add `profiles` to `INSTALLED_APPS` in your django settings file.

Before proceeding with `manage.py syncdb`, you must add some profile extensions.
The profiles module does not add anything to the User model by default.

### Profile extension modules

Extensions are a way to add often-used functionality the `Profile` model. The
extensions are standard python modules with a `register()` method which will be
called upon registering the extension. The `register()` method receives the
`Profile` class itself and the model admin class `ProfileAdmin` as arguments.

There are two ways to set up the extensions. Either you can use the FeinCMS
approach of registering extensions directly (this should go in your models.py):

    from profiles.models import Profile
    Profile.register_extensions('title', 'picture', 'address', 'profiles.modules.options.extensions.options')

or you can simply use a setting:

    PROFILE_EXTENSIONS = ('title', 'picture', 'address', 'profiles.modules.options.extensions.options')

If the extension requires its own models (like the options extension) then the
app containing the models will also need to be added to your `INSTALLED_APPS`.

### Adding extensions

To add an extension create a python module that defines a register function
which accepts the `Profile` class and the `ProfileAdmin` class as arguments and
modifies them as required.

Here is the address extension (`profiles/extensions/address.py`):


    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    def register(cls, admin_cls):
        cls.add_to_class('address1', models.CharField(max_length=255, verbose_name=_('address'), null=True, blank=True))
        cls.add_to_class('address2', models.CharField(max_length=255, verbose_name=_('address 2'), null=True, blank=True))
        cls.add_to_class('city', models.CharField(max_length=255, verbose_name=_('town/city'), null=True, blank=True))
        cls.add_to_class('region', models.CharField(max_length=255, verbose_name=_('county/state/province'), null=True, blank=True))
        cls.add_to_class('postcode', models.CharField(max_length=15, verbose_name=_('postcode'), null=True))
        cls.add_to_class('country', models.ForeignKey('countries.Country', null=True, blank=True))
        cls.add_to_class('telephone', models.CharField(max_length=32, verbose_name=_('mobile number'), null=True, blank=True))

        if admin_cls:
            admin_cls.search_fields += ['address1', 'address2', 'city', 'region', 'postcode']
            admin_cls.list_display_filter += ['country', ]

            if admin_cls.fieldsets:
                admin_cls.fieldsets.append((_('Address'), {
                        'fields': ['address1', 'address2','city', 'region', 'postcode', 'country', 'telephone'],
                        'classes': ('collapse',),
                    }))


### Dependencies

The address extension requires
[`incuna-countries`](http://github.com/incuna/incuna-countries). Add
`countries` to your `INSTALLED_APPS`.

The options and notification extensions require
[`django-orderable`](http://github.com/incuna/django-orderable). Add
`orderable` to your `INSTALLED_APPS`.
