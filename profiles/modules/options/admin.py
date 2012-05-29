from django.contrib import admin

from orderable.admin import OrderableAdmin

from .models import Option


class OptionOptions(OrderableAdmin):
    fields = ('name',)
    search_fields = ('name',)
    ordering = ['sort_order']

admin.site.register(Option, OptionOptions)
