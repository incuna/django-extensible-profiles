from django.conf import settings
from django.conf.urls.defaults import *

from profiles.views import ProfileEdit, ProfileView, RegisterView


urlpatterns = patterns('',
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'^edit/$', ProfileEdit.as_view(), name='profile-edit'),
)

if getattr(settings, 'REGISTRATION_ENABLED', False):
    urlpatterns += patterns('',
        url(r'^register/$', RegisterView.as_view(), name='profile-register'),
    )
