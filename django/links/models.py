from django.contrib.auth.models import User
from django.db import models

import dateutil.parser
import hashlib
import random
import re
import sys
import time

class TripItUser(models.Model):
    user = models.OneToOneField(User)
    oauth_token = models.CharField(max_length = 40)
    oauth_token_secret = models.CharField(max_length = 40)
    #last_update = models.DateTimeField()
    #next_update = models.DateTimeField()

    def __unicode__(self):
        return self.user.email

class TripItTrip(models.Model):
    user = models.ForeignKey(TripItUser)
    trip_id = models.CharField(max_length = 40)
    display_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    county = models.CharField(max_length = 10)
    longitude = models.CharField(max_length = 20)
    latitude = models.CharField(max_length = 20)
    is_private = models.CharField(max_length = 8)

    def __unicode__(self):
        return "%s - %s" % (self.trip_id, self.display_name)

