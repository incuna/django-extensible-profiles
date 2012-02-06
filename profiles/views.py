from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
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


@login_required
def profile_edit(request, extra_context = None, next=None):

    context = RequestContext(request)

    if extra_context != None:
        context.update(extra_context)

    if isinstance(request.user, Profile):
        profile = request.user
    else:
        profile = request.user.profile

    if request.POST or request.FILES:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            request.user.message_set.create(message='Your profile has been updated.')
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('profile'))

    else:
        form = ProfileForm(instance=profile)

    context['form'] = form
    context['site'] = Site.objects.get_current()

    return render_to_response('profiles/profile_form.html', context)

