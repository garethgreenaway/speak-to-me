import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from taggit.managers import TaggableManager

from home.models.headshot import Headshot
from home.models.location import Location
from home.models.presentation import Presentation

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
)

class UserProfile(models.Model):

  class Meta:
    app_label = 'home'

  user = models.ForeignKey(User, unique=True)
  
  user_hash = models.CharField(max_length=36)
  
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  languages = TaggableManager(verbose_name="Languages", help_text="", blank=True)
  company = models.CharField(max_length=100, blank=True)
  personal_bio = models.CharField(max_length=700)
  
  twitter_url = models.CharField(max_length=100, blank=True, verbose_name="Twitter", default="")
  gplus_url = models.CharField(max_length=100, blank=True, verbose_name="Google Plus", default="")
  website_url = models.CharField(max_length=100, blank=True, verbose_name="Website", default="")
  
  # Number of days before an event to alert user
  days_to_event_notify = models.IntegerField(blank=True, default=-1, max_length=3, verbose_name="Notify Me of Events")
  
  headshots = models.ManyToManyField(Headshot)    
  presentations = models.ManyToManyField(Presentation)    
  locations = models.ManyToManyField(Location)
  
  relationships = models.ManyToManyField('self', through='Relationship',
                                  symmetrical=False,
                                  related_name='related_to')
  
  new_profile = models.BooleanField(default=True)
      
  def __unicode__(self):
      return "%s %s %s" % (self.first_name, self.last_name, self.company)
            
  def generate_hash(self):
    h = hashlib.md5()
    h.update(self.user.email)
    self.user_hash = h.hexdigest()
    
  def add_relationship(self, userprofile, status):
    relationship, created = Relationship.objects.get_or_create(
      from_person=self,
      to_person=userprofile,
      status=status)
    return relationship

  def remove_relationship(self, userprofile, status):
    Relationship.objects.filter(
      from_person=self, 
      to_person=userprofile,
      status=status).delete()
    return
    
  def get_relationships(self, status):
    return self.relationships.filter(
        to_people__status=status, 
        to_people__from_person=self)

  def get_related_to(self, status):
    return self.related_to.filter(
        from_people__status=status, 
        from_people__to_person=self)

  def get_following(self):
    return self.get_relationships(RELATIONSHIP_FOLLOWING)

  def get_followers(self):
    return self.get_related_to(RELATIONSHIP_FOLLOWING)

  def is_following(self, speaker_profile):
    #speaker = UserProfile.objects.get(user_hash = user_profile)
    return self.relationships.filter(to_people__status=RELATIONSHIP_FOLLOWING,\
                              to_people__from_person=self,\
                              to_people__to_person=speaker_profile).exists()
         
  def get_friends(self):
    return self.relationships.filter(
        to_people__status=RELATIONSHIP_FOLLOWING, 
        to_people__from_person=self,
        from_people__status=RELATIONSHIP_FOLLOWING, 
        from_people__to_person=self)      
    
      
class Relationship(models.Model):
  class Meta:
    app_label = 'home'

  from_person = models.ForeignKey(UserProfile, related_name='from_people')
  to_person = models.ForeignKey(UserProfile, related_name='to_people')
  status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
