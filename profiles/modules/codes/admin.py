import string
import random

from django import forms
from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from .models import Code


class AutoGenerateForm(forms.Form):
    number = forms.IntegerField(label=_('Number of codes to generate'))
    length = forms.IntegerField(
            label=_('Length of codes to generate'),
            initial=8,
            max_value=255,
            min_value=1)


class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('code',)
    ordering = ['code']

    def get_urls(self):
        from django.conf.urls import patterns, include, url

        urls = super(CodeAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^code-auto-generate/$',
                self.admin_site.admin_view(self.auto_generate),
                {},
                name='code_auto_generate'
            )
        )

        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        if request.method == 'POST':
            auto_generate_form = AutoGenerateForm(request.POST)
        else:
            auto_generate_form = AutoGenerateForm()
        extra_context['auto_generate_form'] = auto_generate_form
        return super(CodeAdmin, self).changelist_view(request, extra_context=extra_context)

    @csrf_protect_m
    def auto_generate(self, request):
        if request.method == 'POST':
            if not self.has_add_permission(request):
                raise PermissionDenied
            form = AutoGenerateForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data.get('number')
                length = form.cleaned_data.get('length')
                for i in range(number):
                    code = CodeAdmin.generate_code(length)
                    while True:
                        code = CodeAdmin.generate_code(length)
                        if not Code.objects.filter(code=code).count():
                            break

                    Code.objects.create(code=code, is_active=True)

            else:
                return self.changelist_view(request, extra_context={'auto_generate_form': form})

        return HttpResponseRedirect(reverse('admin:profiles_code_changelist'))

    @staticmethod
    def generate_code(length):
        """Generate a random string of ascii_uppercase case chars and digits."""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))


admin.site.register(Code, CodeAdmin)
