from django.contrib import admin

from .models import Code


class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('code',)
    ordering = ['code']

admin.site.register(Code, CodeAdmin)