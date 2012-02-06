from django.conf.urls.defaults import *

from profiles.views import ProfileView


urlpatterns = patterns('profiles.views',
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'^edit/$', 'profile_edit', name='profile-edit'),
)

