import re, random
import unicodedata

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

_is_alnum_re = re.compile(r'\w+')
_ID_MIN_LENGTH = 5  # minimum reasonable length for username
_ID_MAX_LENGTH = 30 # as defined in django.auth.contrib.models.User.username field


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Follows the general idea from https://docs.djangoproject.com/en/dev/topics/class-based-views/#decorating-the-class.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


def _id_generator(first_name, last_name, email):
    def _alnum(s, glue=''):
        return glue.join(filter(len, _is_alnum_re.findall(s))).lower()
    # The way to generate id is by trying:
    #  1. username part of email
    #  2. ascii-transliterated first+last name
    #  3. whole email with non-alphanumerics replaced by underscore
    #  4. random string
    # Every try must return at least _ID_MIN_LENGTH chars to succeed and is truncated
    # to _ID_MAX_LENGTH. All IDs are lowercased.
    id = _alnum(email.split('@')[0])
    if len(id) >= _ID_MIN_LENGTH:
        yield id[:_ID_MAX_LENGTH]
    id = _alnum(unicodedata.normalize('NFKD', unicode(first_name + last_name)).encode('ascii', 'ignore'))
    if len(id) >= _ID_MIN_LENGTH:
        yield id[:_ID_MAX_LENGTH]
    id = _alnum(email, glue='_')
    if len(id) >= _ID_MIN_LENGTH:
        yield id[:_ID_MAX_LENGTH]
    while True:
        yield _alnum('%s_%s' % (id[:_ID_MIN_LENGTH], random_string(_ID_MIN_LENGTH, True)))[:_ID_MAX_LENGTH]


def generate_id(first_name='', last_name='', email=''):
    valid_id = False
    gen = _id_generator(first_name, last_name, email)
    test_name = gen.next()
    while valid_id is False:
        try:
            User.objects.get(username=test_name)
        except User.DoesNotExist:
            valid_id = True
        else:
            test_name = gen.next()
    return test_name


_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def random_string(length, variable=False, charset=_LETTERS):
    if variable:
        length = random.randrange(1, length+1)
    return ''.join([random.choice(charset) for x in xrange(length)])
