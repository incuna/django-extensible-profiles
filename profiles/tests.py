from django.contrib.auth.models import User
from django.test import TestCase
import factory

from .models import Profile


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    first_name = factory.Sequence(lambda n: 'Firstname {0}'.format(n))
    last_name = factory.Sequence(lambda n: 'Lastname {0}'.format(n))
    username = factory.Sequence(lambda n: 'user-{0}'.format(n).lower())
    email = factory.LazyAttribute(lambda a: '{0}@example.com'.format(a.username).lower())


class ProfileFactory(UserFactory):
    FACTORY_FOR = Profile
    user_ptr = factory.SubFactory(UserFactory)


class ProfileUtils(object):
    def generate_profile(self, **kwargs):
        password = kwargs.pop('password', 'test')
        profile = ProfileFactory.build(**kwargs)
        profile.set_password(password)
        profile.save()
        return profile

    def login(self, user=None, password='test'):
        user = user or self.user
        self.client.login(username=user.username, password=password)

