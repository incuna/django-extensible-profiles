from django.dispatch import Signal

# A new user has registered
user_registered = Signal(providing_args=['user', 'request'])

# A user has updated the account
user_updated = Signal(providing_args=['user', 'request'])
