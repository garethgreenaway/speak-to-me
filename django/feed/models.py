from django.db import models

import dateutil.parser
import hashlib
import random
import re
import sys
import time

class Feed(models.Model):
    name = models.CharField(max_length=100)
    logo = models.URLField()
    url = models.URLField()
    site_uuid = models.CharField(unique=True, max_length=50)
    next_update = models.DateTimeField()
    category = models.CharField(max_length=25)
    addedDate = models.DateTimeField()
    rating = models.CharField(blank=True, max_length=25)
    subscribers = models.IntegerField(default=0)
    locked = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.url)

    def generate_uuid(self):
        m = hashlib.md5()
        m.update(self.url)
        self.site_uuid = m.hexdigest()

    def unsubscribe(self):
        self.subscribers -= 1
        self.save()

    def subscribe(self):
        self.subscribers += 1
        self.save()

    def setNextUpdate(self, nextUpdate = ""):
        if nextUpdate:
            self.save()
        else:
            now = time.time()
            self.next_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))

    def setAddedDate(self): 
        now = time.time()
        self.addedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))

    def save(self, *args, **kwargs):
        if self.addedDate:
            super(Feed, self).save(*args, **kwargs)
        else:
	        self.setAddedDate()
	        self.generate_uuid()
	        self.setNextUpdate()
	        super(Feed, self).save(*args, **kwargs)

class FeedStaging(models.Model):
    url = models.URLField()
    user = models.CharField(blank=True, max_length=30)
    category = models.CharField(blank=True, max_length=30)

    def __unicode__(self):
        return "%s" % (self.url)

