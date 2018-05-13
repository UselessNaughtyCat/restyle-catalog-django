from django.db import models
from django.contrib.auth.models import User

from project.style.models import Style

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    subscriptions = models.ManyToManyField(Style, blank=True)

    def __str__(self):
        return self.user.username
