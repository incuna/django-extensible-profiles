from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from incuna.utils import get_class_from_path

try:
    ProfileForm = get_class_from_path(settings.PROFILE_FORM_CLASS)
except AttributeError:
    from forms import ProfileForm

@login_required
def profile(request, extra_context = None):

    context = RequestContext(request)

    if extra_context != None:
        context.update(extra_context)

    return render_to_response('profiles/profile.html', context)

@login_required
def profile_edit(request, extra_context = None, next=None):
        
    context = RequestContext(request)
    
    if extra_context != None:
        context.update(extra_context)

    if request.POST or request.FILES:
        form = ProfileForm(request.POST, request.FILES, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            form.save_m2m()
            
            request.user.message_set.create(message='Your profile has been updated.')
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('profile'))

    else:
        form = ProfileForm(instance=request.user.get_profile())

    context['form'] = form
    context['site'] = Site.objects.get_current()

    return render_to_response('hcpprofile/profile_form.html', context)

