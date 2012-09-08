import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Headshot(models.Model):

  class Meta:
    app_label = 'home'

  filename = models.CharField(max_length=100)

