from django import template

from models import Profile

register = template.Library()

@register.inclusion_tag('profiles/_users_count.html')
def users_count():
    return {'users_count': Profile.objects.count()}

