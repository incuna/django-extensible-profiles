from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, get_callable
from django.views.generic import TemplateView, CreateView, UpdateView

from profiles.models import Profile
from profiles.utils import class_view_decorator, generate_id

try:
    ProfileForm = get_callable(settings.PROFILE_FORM_CLASS)
except AttributeError:
    from forms import ProfileForm

try:
    RegistrationForm = get_callable(settings.REGISTRATION_FORM_CLASS)
except AttributeError:
    RegistrationForm = ProfileForm


@class_view_decorator(login_required)
class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'profiles/profile_form.html'
    success_url = getattr(settings, 'REGISTRATION_COMPLETE_URL',
        settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        if not 'username' in form.cleaned_data:
            # auto generate a username
            generate_kwargs = {}
            for fname in ['first_name', 'last_name', 'email']:
                if fname in form.cleaned_data:
                    generate_kwargs[fname] = form.cleaned_data[fname]
            form.cleaned_data['username'] = generate_id(**generate_kwargs)

        # try to get the password
        password = None
        for fname in ['password', 'password1', 'password2', 'plain_password']:
            if fname in form.cleaned_data:
                password = form.cleaned_data[fname]
                break

        obj = form.save(commit=False)

        if password:
            obj.set_password(password)

        obj.save()

        if password:
            user = authenticate(username=form.cleaned_data['username'], password=password)
            messages.info(self.request, 'Your profile has been created.')
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)


@class_view_decorator(login_required)
class ProfileEdit(UpdateView):
    form_class = ProfileForm

    def form_valid(self, form):
        response = super(ProfileEdit, self).form_valid(form)
        messages.info(self.request, 'Your profile has been updated.')
        return response

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        return context

    def get_object(self):
        if isinstance(self.request.user, Profile):
            return self.request.user
        return self.request.user.profile

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url or reverse('profile'))

