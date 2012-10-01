import hashlib

from django.db import models

from taggit.managers import TaggableManager

from home.models.location import Location

class Event(models.Model):

  class Meta:
    app_label = 'home'
  
  event_hash = models.CharField(max_length=36)
  event_name = models.CharField(max_length=100)
  
  start_date = models.DateField()
  end_date = models.DateField()
  
  event_description = models.CharField(max_length=700, verbose_name="Description")  
  event_website = models.URLField(max_length=100, verbose_name="Website")
  
  locations = models.ForeignKey(Location, unique=True)
  topic_tags = TaggableManager(verbose_name="Topic Tags")    
  
  def generate_hash(self):
    h = hashlib.md5()
    h.update(self.event_website)
    self.event_hash = h.hexdigest()
  
