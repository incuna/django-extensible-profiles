from django.contrib.auth.models import User

import factory

from .models import Profile


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    first_name = factory.Sequence(lambda n: 'Firstname {0}'.format(n))
    last_name = factory.Sequence(lambda n: 'Lastname {0}'.format(n))
    username = factory.Sequence(lambda n: 'user-{0}'.format(n).lower())
    email = factory.LazyAttribute(lambda a: '{0}@example.com'.format(a.username).lower())

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', 'password')
        user = super(UserFactory, cls)._prepare(create=False, **kwargs)
        user.set_password(password)
        user.raw_password = password
        if create:
            user.save()
        return user


class ProfileFactory(UserFactory):
    FACTORY_FOR = Profile
    user_ptr = factory.SubFactory(UserFactory)


class UserWithProfileFactory(ProfileFactory):
    """
    Return a user object that has a profile.
    """
    @classmethod
    def _prepare(cls, create, **kwargs):
        profile = super(UserWithProfileFactory, cls)._prepare(create, **kwargs)
        return profile.user_ptr


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

