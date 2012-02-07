from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, UpdateView
from incuna.utils import get_class_from_path

from profiles.models import Profile
from profiles.utils import class_view_decorator

try:
    ProfileForm = get_class_from_path(settings.PROFILE_FORM_CLASS)
except AttributeError:
    from forms import ProfileForm


@class_view_decorator(login_required)
class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'


@class_view_decorator(login_required)
class ProfileEdit(UpdateView):
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def form_valid(self, form):
        instance = super(ProfileEdit, self).form_valid(form)
        self.request.user.message_set.create(message='Your profile has been updated.')
        return instance

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        return context

    def get_object(self):
        if isinstance(self.request.user, Profile):
            return self.request.user
        return self.request.user.profile

    def get_success_url(self):
        return self.request.GET.get('next', reverse('profile'))

