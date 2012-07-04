from django.conf import settings
from django.conf.urls.defaults import *

from profiles.views import ProfileEdit, ProfileView, RegisterView


urlpatterns = patterns('profiles.views',
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/$', ProfileEdit.as_view(), name='profile-edit'),
)

if getattr(settings, 'REGISTRATION_ON_VIEW', False):
    urlpatterns += patterns('profiles.views',
        url(r'^profile/register/$', RegisterView.as_view(), name='profile-register'),
    )
