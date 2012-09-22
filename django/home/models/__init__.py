import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from taggit.managers import TaggableManager


from home.models.location import Location
from home.models.presentation import Presentation
from home.models.headshot import Headshot
from home.models.userprofile import UserProfile
from home.models.event import Event
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])



