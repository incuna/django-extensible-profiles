from django.core.management.base import LabelCommand, CommandError

class Command(LabelCommand):
    help = 'Add a profile for the specified user(s).'
    args = '[username1, username2, email1, ...]'

    def handle_label(self, username, **options):
        from django.contrib.auth.models import User
        from profiles.models import Profile

        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            profile = Profile.objects.get(**kwargs)
        except Profile.DoesNotExist:
            try:
                user = User.objects.get(**kwargs)
            except User.DoesNotExist:
                raise CommandError("User '%s' does not exist" % username)

            print "Adding profile for %s" % username
            initial = dict([(f.name, getattr(user, f.name)) for f in user._meta.fields])
            profile = Profile(user_ptr=user, **initial)
            profile.save()
            for f in user._meta.many_to_many:
                getattr(profile, f.name).add(*getattr(user, f.name).all())

        else:
            raise CommandError("Profile '%s' already exists" % username)
