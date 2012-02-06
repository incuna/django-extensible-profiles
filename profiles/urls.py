from django.conf.urls.defaults import *

from profiles.views import ProfileEdit, ProfileView


urlpatterns = patterns('profiles.views',
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'^edit/$', ProfileEdit.as_view(), name='profile-edit'),
)

