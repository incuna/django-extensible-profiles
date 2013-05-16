from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, get_callable
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, CreateView, UpdateView

from profiles.models import Profile
from profiles.signals import user_registered, user_updated
from profiles.utils import class_view_decorator, generate_id


@class_view_decorator(login_required)
class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'


class ProfleFormMixin(object):
    def get_form_class(self):
        if self.form_class:
            return self.form_class

        # Delay defining the ProfileForm to ensure that the model has been
        # defined (with all extensions).
        try:
            ProfileForm = get_callable(settings.PROFILE_FORM_CLASS)
        except AttributeError:
            from .forms import ProfileForm
        return ProfileForm


class RegisterView(ProfleFormMixin, CreateView):
    template_name = 'profiles/profile_form.html'
    success_url = getattr(settings, 'REGISTRATION_COMPLETE_URL', settings.LOGIN_REDIRECT_URL)

    def authenticate_new_user(self, username, password):
        if password:
            user = authenticate(username=username, password=password)
            messages.info(self.request, _('Your profile has been created.'))
            login(self.request, user)
        return user

    def get_form_class(self):
        if self.form_class:
            return self.form_class

        # Delay defining the form to ensure that the model has been
        # defined (with all extensions).
        try:
            RegistrationForm = get_callable(settings.REGISTRATION_FORM_CLASS)
        except AttributeError:
            RegistrationForm = super(RegisterView, self).get_form_class()

        return RegistrationForm

    def form_valid(self, form):
        self.username = self.get_username(form.cleaned_data)

        self.password = self.get_password(form.cleaned_data)

        obj = form.save(commit=False)
        obj = self.update_user_object(obj)
        obj.save()

        self.send_signals(form, obj)

        self.authenticate_new_user(self.username, self.password)

        return super(RegisterView, self).form_valid(form)

    def get_password(self, data):
        # try to get the password
        for fname in ['password', 'password1', 'password2', 'plain_password']:
            if fname in data:
                return data[fname]
        return None

    def get_username(self, data):
        if not 'username' in data:
            # auto generate a username
            generate_kwargs = {}
            for fname in ['first_name', 'last_name', 'email']:
                if fname in data:
                    generate_kwargs[fname] = data[fname]
            return generate_id(**generate_kwargs)

    def send_signals(self, form, user):
        user_registered.send(sender=self.__class__, user=user, request=self.request, form=form)

    def update_user_object(self, user):
        if self.password:
            user.set_password(self.password)
        return user


@class_view_decorator(login_required)
class ProfileEdit(ProfleFormMixin, UpdateView):
    def form_valid(self, form):
        response = super(ProfileEdit, self).form_valid(form)
        user_updated.send(sender=self.__class__, user=self.request.user, request=self.request, form=form)
        messages.info(self.request, _('Your profile has been updated.'))
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
