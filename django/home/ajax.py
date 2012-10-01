from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from django.template.loader import render_to_string
from django.conf import settings
from home.forms import ProfileLocationForm, ProfilePresentationForm
from home.forms import ProfilePersonalForm, ProfileSpeakerForm, ProfileSocialForm, ProfileNotificationsForm
from home.views import get_presentations
from home.models import Location, Presentation, UserProfile
from home.models.userprofile import RELATIONSHIP_FOLLOWING
from home.tasks import convert_to_pdf, geocode

import logging
  
logger = logging.getLogger('home.views')

@dajaxice_register
def send_form(request, form, form_id):

  dajax = Dajax()
  logger.error(form_id)

  if form_id == "id-profile-personal-form":
    form = ProfilePersonalForm(form, instance = request.user.profile)
    
    if form.is_valid():
      dajax.remove_css_class('#%s div' % form_id,'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')
      user_profile = form.save()
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-success">Personal Information Saved</div>')    
      result = "success"
      
    else:
      dajax.remove_css_class('#%s div' % form_id, 'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')      
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-error">Please fix the errors below</div>')
      for error in form.errors:
        dajax.add_css_class('#div_id_%s' % error, 'error')
      result = "failed"

    return dajax.json()

  elif form_id == "id-profile-speaker-form":
    form = ProfileSpeakerForm(form, instance = request.user.profile)
    
    if form.is_valid():
      dajax.remove_css_class('#%s div' % form_id,'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')
      user_profile = form.save()
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-success">Speaker Information Saved</div>')    
      result = "success"
      
    else:
      dajax.remove_css_class('#%s div' % form_id, 'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')      
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-error">Please fix the errors below</div>')
      for error in form.errors:
        dajax.add_css_class('#div_id_%s' % error, 'error')
      result = "failed"

    return dajax.json()
    
  elif form_id == "id-profile-social-form":
    form = ProfileSocialForm(form, instance = request.user.profile)
    
    if form.is_valid():
      dajax.remove_css_class('#%s div' % form_id,'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')
      user_profile = form.save()
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-success">Social Networking Information Saved</div>')    
      result = "success"
      
    else:
      dajax.remove_css_class('#%s div' % form_id, 'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')      
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-error">Please fix the errors below</div>')
      for error in form.errors:
        dajax.add_css_class('#div_id_%s' % error, 'error')
      result = "failed"

    return dajax.json()

  elif form_id == "id-profile-notifications-form":
    form = ProfileNotificationsForm(form, instance = request.user.profile)
    
    if form.is_valid():
      dajax.remove_css_class('#%s div' % form_id,'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')
      user_profile = form.save()
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-success">Notification Settings Saved</div>')    
      result = "success"
      
    else:
      dajax.remove_css_class('#%s div' % form_id, 'error')
      dajax.clear('#%s-alert' % form_id, 'innerHTML')      
      dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-error">Please fix the errors below</div>')
      for error in form.errors:
        dajax.add_css_class('#div_id_%s' % error, 'error')
      result = "failed"

    return dajax.json()

  else:
    pass
    
#  if form_id == "id-presentation-form":
#    logger.error("Presentation Form")

#    # Check for the presentation slides hidden value
#    if len(form['presentation_slides']) <= 0:
#        dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-error">Please upload a presenation.</div>')
#        result = "failed"
#        dajax.add_data({'result': result}, 'js_callback')
#        return dajax.json()
#    else:
#        dajax.clear('#%s-alert' % form_id, 'innerHTML')
#  
#    logger.error(form)
#    form = ProfilePresentationForm(form, request.FILES)
#    
#  elif form_id == "id-location-form":
#    form = ProfileLocationForm(form)
#    
#  elif form_id == "id-personal-form":
#    form = ProfilePersonalForm(form, instance = request.user.profile)
#    
#  else:
#    result = "failed"
#    return dajax.json()
#     
#  if form.is_valid():
#    dajax.remove_css_class('#%s div' % form_id,'error')
#    dajax.clear('#%s-alert' % form_id, 'innerHTML')
#    
#    # Save the personal information to the profile
#    if form_id == "id-personal-form":
#      user_profile = form.save(commit=False)
#      user_profile.generate_hash()
#      user_profile.new_profile = False
#      user_profile.save()
#      form.save_m2m()
#      
#    elif form_id == "id-location-form":
#      location = form.save()
#      request.user.profile.locations.add(location)
#      geocode.delay(location)

#    elif form_id == "id-presentation-form":
#      presentation = form.save(commit=False)
#      presentation.presentation_slides = form.cleaned_data['presentation_slides']
#      presentation.save()
#      form.save_m2m()
#      request.user.profile.presentations.add(presentation)
#      
#      # Kick off the Celery job to convert to PDF and generate the thumbnail
#      #convert_to_pdf.delay("%s/%s" % (settings.CURRENT_DIR, presentation_slides), request.user, presentation)
#      convert_to_pdf.delay(request.user, presentation)
#            
#    else:
#      pass
#      
#    result = "success"

#  else:
#    logger.error("%s Form not valid" % form_id)
#    dajax.remove_css_class('#%s div' % form_id,'error')
#    dajax.append('#%s-alert' % form_id, 'innerHTML', '<div class="alert alert-error">Please fix the errors below</div>')
#    logger.error(form.__dict__)
#    for error in form.errors:
#      logger.error(error)
#      dajax.add_css_class('#div_id_%s' % error, 'error')
#    result = "failed"
#      
#  dajax.add_data({'result': result, 'form_id': form_id}, 'js_callback')
#  return dajax.json()

def save_profile_personal_form(request, form, form_id, dajax):
  pass
  
def save_profile_speaker_form(request, form):
  pass
    
def save_profile_social_form(request, form):
  pass
  
def save_profile_notifications_form(request, form):
  pass  

@dajaxice_register
def presentation_pagination(request, p, speakerprofile):

  logger.error(speakerprofile)
  
  try:
    page = int(p)
  except:
    page = 1

  presentations = get_presentations(speakerprofile, page)
  logger.error(presentations.paginator.num_pages)
  
  render = render_to_string('PresentationList.html', { 'presentations': presentations })

  dajax = Dajax()
  dajax.assign('#presentations', 'innerHTML', render)
  
  return dajax.json()
  
  
@dajaxice_register
def speaker_follow(request, speaker):
  dajax = Dajax()
  
  logger.error(request.user.profile)
  speaker = UserProfile.objects.get(user_hash=speaker)
  request.user.profile.add_relationship(speaker, RELATIONSHIP_FOLLOWING)
  
  return dajax.json()  
  
@dajaxice_register
def speaker_unfollow(request, speaker):
  dajax = Dajax()
  
  logger.error(request.user.profile)
  speaker = UserProfile.objects.get(user_hash=speaker)
  request.user.profile.remove_relationship(speaker, RELATIONSHIP_FOLLOWING)
  
  return dajax.json()  
  
  

