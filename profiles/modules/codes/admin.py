from django.contrib import admin

from .models import Code


class CodeAdmin(admin.ModelAdmin):
    fields = ('code',)
    search_fields = ('code',)
    ordering = ['code']

admin.site.register(Code, CodeAdmin)