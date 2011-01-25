from django.contrib import admin

from models import Profile, ProfileAdmin

admin.site.register(Profile, ProfileAdmin)
