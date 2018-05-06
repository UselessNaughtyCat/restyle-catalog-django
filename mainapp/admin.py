from django.contrib import admin
from mainapp.models import Person, Site, Style

# Register your models here.

admin.site.register(Person)
admin.site.register(Site)
admin.site.register(Style)
