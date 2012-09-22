import os
import decimal

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

from django.contrib.contenttypes.models import ContentType

from taggit.models import TaggedItem, Tag

from geopy import geocoders

from home.models import UserProfile, Location, Presentation, Event
from links.models import TripItUser

from home.forms import ProfilePersonalForm, ProfileLocationForm, ProfilePresentationForm, AdvancedSearchForm, EventForm

from ajaxuploader.views import AjaxFileUploader

import logging
logger = logging.getLogger('home.views')

import_uploader = AjaxFileUploader()
          
def index(request):

    if request.user.is_authenticated():
        user = User.objects.select_related().get(email = request.user.email)
        userprofile = user.profile

        if user.profile.new_profile:

          if not user.profile.first_name:
            personal_form = ProfilePersonalForm()
          
          if len(user.profile.locations.all()) == 0:
            location_form = ProfileLocationForm()
            
          if len(user.profile.presentations.all()) == 0:
            presentation_form = ProfilePresentationForm(form_skip_button = True)
            
          #if len(user.profile.upcomingtalks.all()) == 0:
          # upcomingtalks_form = ProfileUpcomingTalksForm()
          
          return render_to_response('CreateNewProfile.html', locals(), context_instance = RequestContext(request))
          
        else:
          return render_to_response('AuthenticatedIndex.html', locals(), context_instance = RequestContext(request))

          
    else:          
      return render_to_response('index.html', locals(), context_instance = RequestContext(request))

def hear(request):
  if request.user.is_authenticated():
    #return render_to_response('AuthenicatedHear.html', locals(), context_instance = RequestContext(request))
    return render_to_response('Hear.html', locals(), context_instance = RequestContext(request))    
  else:
    return render_to_response('Hear.html', locals(), context_instance = RequestContext(request))

  
def find(request):
  if request.user.is_authenticated():
    #return render_to_response('AuthenicatedFind.html', locals(), context_instance = RequestContext(request))
    return render_to_response('Find.html', locals(), context_instance = RequestContext(request))    
  else:
    return render_to_response('Find.html', locals(), context_instance = RequestContext(request))

def speak(request):
  if request.user.is_authenticated():
    return render_to_response('Speak.html', locals(), context_instance = RequestContext(request))  
    #return render_to_response('AuthenicatedSpeak.html', locals(), context_instance = RequestContext(request))
  else:
    return render_to_response('Speak.html', locals(), context_instance = RequestContext(request))
  
def explore(request):
  pass
  
def signup(request):
  page_title = "Sign Up"
  return render_to_response('signup.html', locals(), context_instance = RequestContext(request))
  
#@login_required
#def speak(request):

#    # Set everything to false
#    personal_form = location_form = presentation_form = ""
#    
#    if request.user.is_authenticated():
#        user = User.objects.get(email = request.user.email)
#        
#        # New Profile
#        if user.profile.new_profile:

#          if not user.profile.first_name:
#            personal_form = ProfilePersonalForm()
#          
#          if len(user.profile.locations.all()) == 0:
#            location_form = ProfileLocationForm()
#            
#          if len(user.profile.presentations.all()) == 0:
#            presentation_form = ProfilePresentationForm()
#            
#          #if len(user.profile.upcomingtalks.all()) == 0:
#          # upcomingtalks_form = ProfileUpcomingTalksForm()
#          
#          return render_to_response('CreateNewProfile.html', locals(), context_instance = RequestContext(request))
#        else:
#        
#          logger.error("before the call to get_presentations")
#          logger.error(user.profile.user_hash)
#          presentations = get_presentations(user.profile.user_hash)
#        
#          return render_to_response('SpeakerProfile.html', locals(), context_instance = RequestContext(request))

def signup(request):

  page_title = "Sign Up"
  return render_to_response('signup.html', locals(), context_instance = RequestContext(request))

@login_required
def logout_view(request):
    auth_logout(request)

    return HttpResponseRedirect('/')
    
def get_presentations(user_hash, page = None):

  logger.error(user_hash)
  profile = UserProfile.objects.get(user_hash = user_hash)
  presentation_list = profile.presentations.select_related().all()
  paginator = Paginator(presentation_list, 8)
  
  if page == None:
    # No page, return the first page of results.
    presentations = paginator.page(1)
  else:
    try:
      presentations = paginator.page(page)
    except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      presentations = paginator.page(1)
    except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      presentations = paginator.page(paginator.num_pages)
      
  return presentations
  
def list_presentations(request):

  user = User.objects.get(email = request.user.email)
  user_profile = user.profile
  presentation_list = user.profile.presentations.all()
  paginator = Paginator(presentation_list, 8)
  
  if page == None:
    # No page, return the first page of results.
    presentations = paginator.page(1)
  else:
    try:
      presentations = paginator.page(page)
    except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      presentations = paginator.page(1)
    except (EmptyPage, InvalidPage):
      # If page is out of range (e.g. 9999), deliver last page of results.
      presentations = paginator.page(paginator.num_pages)
      
  return HttpResponse(presentations)    
    
    
def search(request):

  logger.error(request)
  
  if request.user.is_authenticated():
      user = User.objects.get(email = request.user.email)
        
  query = request.GET.get('q', '')
  
  if query:
    # Search UserProfiles
    qset = (
        Q(first_name__istartswith=query) |
        Q(last_name__istartswith=query) |
        Q(company__istartswith=query)
    )
    speaker_results = UserProfile.objects.filter(qset).distinct().order_by('last_name', 'first_name')
    
    qset = (
        Q(presentation_title__contains=query)
    )
    presentation_results = Presentation.objects.filter(qset).distinct()
  else:
    results = []

  return render_to_response("search_results.html", {
      "speaker_results": speaker_results,
      "presentation_results": presentation_results,
      "query": query
  },context_instance = RequestContext(request))
  
def advanced_search(request):
  
  #if request.user.is_authenticated():
  #    user = User.objects.get(email = request.user.email)

  q = request.GET.get('q', '')
  
  if q:
  
    # Get all the profiles
    results = UserProfile.objects.all()
    
    # Check if a query included speaker name then filter on it
    query_speaker_name = request.GET.get('speaker_name', '')
    if query_speaker_name:
      qset = (
          Q(first_name__startswith=query_speaker_name) |
          Q(last_name__startswith=query_speaker_name)
      )
      results = results.filter(qset)

    # Check if a query included company name then filter on it
    query_company_name = request.GET.get('company_name', '')
    if query_company_name:
      qset = (
          Q(company__startswith=query_company_name)
      )
      results = results.filter(qset)
          
    query_location_choices = request.GET.get('location_choices', '')
    logger.error(query_location_choices)
    if query_location_choices:

      logger.error("searching based on profile locations")
      query_distance = request.GET.get('distance', '')
      
      # If this is km we should convert to miles      
      query_measurement = request.GET.get('measurement', '')
          
      (lat, lng) = query_location_choices.split(",")
      l = Location(latitude = decimal.Decimal(lat), longitude = decimal.Decimal(lng))
      
      # Find the location objects which match the query within the radius
      locs = l.within_radius(query_distance)
      qset = (
          Q(locations__in=locs)
      )      
      results = results.filter(qset)    
                
    query_location = request.GET.get('location', '')
    if query_location and not query_location_choices:
    
      logger.error("searching based on query")    
      query_distance = request.GET.get('distance', '')
      
      # If this is km we should convert to miles      
      query_measurement = request.GET.get('measurement', '')

      # Should find a way to cache this
      g = geocoders.Google()      
      # Get the geocode for the location entered
      place, (lat, lng) = g.geocode(query_location)

      # Create a temporary location to search with      
      l = Location(latitude = decimal.Decimal(lat), longitude = decimal.Decimal(lng))
      
      # Find the location objects which match the query within the radius
      locs = l.within_radius(query_distance)
      qset = (
          Q(locations__in=locs)
      )      
      results = results.filter(qset)

    query_topics = request.GET.get('topics', '')      
    if query_topics:
      #
      # Split query_topic into a list
      # Get presenations that match query and belong to the users we've found so far
      presentation_results = Presentation.objects.filter(userprofile__in=results, presentation_topics__name__contains=query_topics)
      
      # Update the userprofile to only include those that match the topic query
      results = UserProfile.objects.filter(presentations__in=presentation_results)
    
    results = results.distinct()
    return render_to_response("advanced_search_results.html", locals(), context_instance = RequestContext(request))

  else:

    if request.user.is_authenticated():
      userprofile = request.user.profile
      locations = userprofile.locations.all()
      form = AdvancedSearchForm(profile_locations = locations)
    else:
      form = AdvancedSearchForm()
      
    return render_to_response("advanced_search.html", locals(), context_instance = RequestContext(request))  

def event_add(request):
  if request.user.is_authenticated():
    user = User.objects.get(email = request.user.email)
      
    event_form = EventForm()
    return render_to_response('AddEvent.html', locals(), context_instance=RequestContext(request))

def location_add(request):
  if request.user.is_authenticated():
    user = User.objects.get(email = request.user.email)
      
    location_form = ProfileLocationForm()
    return render_to_response('AddLocation.html', locals(), context_instance=RequestContext(request))
    
def presentation_add(request):
  if request.user.is_authenticated():
    user = User.objects.get(email = request.user.email)
      
    presentation_form = ProfilePresentationForm(form_skip_button = False)
    return render_to_response('AddPresentation.html', locals(), context_instance=RequestContext(request))
    
def presentation_add_modal(request):
  if request.user.is_authenticated():
    user = User.objects.get(email = request.user.email)
      
    presentation_form = ProfilePresentationForm(form_skip_button = False, modal_form = True)
    return render_to_response('AddPresentationModal.html', locals(), context_instance=RequestContext(request))    
    
def presentation_thumbnail(request, presentation_hash):
    presentation = Presentation.objects.get(presentation_hash = presentation_hash)
    thumbnail_url = presentation.presentation_thumbnail
    
    return redirect(thumbnail_url)

def presentation_pdf(request, presentation_hash):
    presentation = Presentation.objects.get(presentation_hash = presentation_hash)
    filename = presentation.presentation_pdf
    pdf = FileWrapper(file(filename))
        
    response = HttpResponse(pdf, mimetype="application/pdf")
    response['Content-Length'] = os.path.getsize(presentation.presentation_pdf)
    
    return response
        
def profile_show(request, user_hash = None):

  if user_hash == None:
    if request.user.is_authenticated():
        logger.error("User authenticated")
        user = User.objects.get(email = request.user.email)
        userprofile = user.profile        
        speakerprofile = userprofile

  else:
    speakerprofile = UserProfile.objects.get(user_hash = user_hash)
    
    following = False
    if request.user.is_authenticated():
        user = User.objects.get(email = request.user.email)
        userprofile = user.profile
    
        following = userprofile.is_following(speakerprofile)      


  profile_language_tags = speakerprofile.languages.all()
  profile_presentations = speakerprofile.presentations.select_related("presentation_topics").all()
  
  tags = []
  for p in profile_presentations:
    tags = tags + list(p.presentation_topics.all())
    
  similar_speakers = []
  similar_p = Presentation.objects.select_related().filter(Q(presentation_topics__in=tags), ~Q(userprofile=speakerprofile)).distinct()
  for p in similar_p:
    s = p.userprofile_set.get()
    if s not in similar_speakers:
      similar_speakers.append(s)
      
  #for i in profile_presentations:
  #  for j in i.presentation_topics.similar_objects():
  #      for k in j.userprofile_set.all():
  #        if k != speakerprofile and k not in similar_speakers:
  #          similar_speakers.append(k)

  
  return render_to_response('SpeakerProfile.html', locals(), context_instance = RequestContext(request))
  
def profile_edit(request):
  if request.user.is_authenticated():
      user = User.objects.get(email = request.user.email)
      
      return render_to_response('EditProfile.html', locals(), context_instance = RequestContext(request))
    
  

