## Extensible user profiles for Django

This is an extensible user profile system for Django, designed to provide a simple user Profile model that is extensible.

The concept (and some code) is borrowed from the FeinCMS (https://github.com/matthiask/feincms) page model.

To use the profiles module add profiles to your INSTALLED_APPS.

Before proceeding with manage.py syncdb, you must add some profile extensions. The profiles module does not add anything to the User model by default.


### Profile extension modules

Extensions are a way to add often-used functionality the Profile model. The extensions are standard python modules with a register() method which will be called upon registering the extension. The register() method receives the Profile class itself and the model admin class ProfileAdmin as arguments.

To register extensions, simply pop a list of them in your settings.py:

    PROFILE_EXTENSIONS = ('title', 'picture', 'address', 'profiles.modules.options.extensions.options')

For backwards compatibility, extensions can be activated by adding the following to a models.py file that will be processed anyway. eg:

    from profiles.models import Profile
    Profile.register_extensions('title', 'picture', 'address', 'profiles.modules.options.extensions.options')


If the extension requires it's own models (like the options extension) then the app containing the models will also need to be added to your INSTALLED_APPS.

### Adding extensions

To add an extension create a python module that defines a register function that accepts the Profile class and the ProfileAdmin class as arguments and modifies them as required.

Here is the address extension (profiles/extensions/address.py):


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

Add 'incuna.countries' to INSTALLED_APPS for using address extension.
