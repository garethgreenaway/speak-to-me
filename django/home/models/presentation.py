import hashlib

from django.db import models

from taggit.managers import TaggableManager

class Presentation(models.Model):
  PRESENTATION_LENGTH = (
    ('5','5 minutes'),
    ('30','30 minutes'),
    ('45','45 minutes'),
    ('90','90 minutes'),
  )
    
  class Meta:
    app_label = 'home'
        
  presentation_title = models.CharField(max_length=100, verbose_name="Title")
  presentation_length = models.CharField(max_length=3, verbose_name="Length", choices=PRESENTATION_LENGTH)
  presentation_hidden = models.BooleanField(verbose_name="Hidden")
  presentation_thumbnail = models.CharField(max_length=100)
  presentation_pdf = models.CharField(max_length=100)
  presentation_pdf_url = models.CharField(max_length=100)    
  presentation_slides = models.CharField(max_length=100)
  presentation_slides_url = models.CharField(max_length=100)        
  presentation_description = models.CharField(max_length=700, verbose_name="Description")
  presentation_topics = TaggableManager(verbose_name="Topics")    
  presentation_hash = models.CharField(max_length=36)    
    
  # This will get generated on conversion, in tasks.py
  def generate_hash(self, name):
    h = hashlib.md5()
    h.update(name)
    self.presentation_hash = h.hexdigest()    
