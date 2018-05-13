from django.contrib import admin

from .models import Url, Site, Style

admin.site.register(Url)
admin.site.register(Site)
admin.site.register(Style)