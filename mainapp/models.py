from django.db import models
from django.contrib.auth.models import User

class SiteUrls(models.Model):
    url = models.CharField(max_length=1024)

    def __str__(self):
        return self.url

class Site(models.Model):
    name = models.CharField(max_length=1024)
    urls = models.ManyToManyField(SiteUrls, blank=True)
    image = models.ImageField(upload_to='images/site_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Style(models.Model):
    name = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='images/style_logos/', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    upload_date = models.DateField(default=None)
    last_update = models.DateField(default=None)
    subscribed = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    subscriptions = models.ManyToManyField(Style, blank=True)
