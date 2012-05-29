from django.contrib import admin

from orderable.admin import OrderableAdmin

from .models import Notification


class NotificationOptions(OrderableAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'field_name', )
    list_display = ('name', 'slug', 'field_name', 'sort_order_display')
    search_fields = ('name', )
    ordering = ('sort_order',) 

admin.site.register(Notification, NotificationOptions)


