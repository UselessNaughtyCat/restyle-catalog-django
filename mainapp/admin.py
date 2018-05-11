from django.contrib import admin
from mainapp.models import Person, Site, Style, SiteUrls

# Register your models here.

admin.site.register(Person)
admin.site.register(SiteUrls)
admin.site.register(Site)
admin.site.register(Style)
