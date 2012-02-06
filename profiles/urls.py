from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('profiles.views',
    url(r'^$', 'profile', name='profile'),
    url(r'^edit/$', 'profile_edit', name='profile-edit'),
)
