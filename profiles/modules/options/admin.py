from django.contrib import admin
from django.contrib.admin.options import *
from incuna.admin.order import OrderableAdmin
from models import *

class OptionOptions(OrderableAdmin):
    fields = ('name',)
    search_fields = ('name', )
    ordering = ["sort_order", ] 

admin.site.register(Option, OptionOptions)

