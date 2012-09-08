import filecmp
import hashlib
import os
import re
import shutil
import simplejson
import subprocess
import urllib

from celery.task import periodic_task
from celery.task import task

from celery.task.schedules import crontab

from home.models import User,UserProfile,Location

from django.conf import settings

import logging
logger = logging.getLogger('home.views')

from DocumentConverter import DocumentConverter, DocumentConversionException

@task
def convert_to_pdf(user, presentationObject):

  inputFile = "%s/%s" % (settings.CURRENT_DIR, presentationObject.presentation_slides)
  profile = user.profile
  
  # Location to store user's files
  # based on the hash of their username  
  levelOne = profile.user_hash[0:4]
  levelTwo = profile.user_hash[4:8]
  path = "%s/%s/%s" % (settings.STORAGE_ROOT, levelOne, levelTwo)
  url_path = "%s/%s/%s" % (settings.STORAGE_URL, levelOne, levelTwo)
  
  # Check if directory exists, if not...create it
  if not os.path.exists(path):
    os.makedirs(path)
  
  # Check that the uploaded file exists
  if os.path.exists("%s" % (inputFile)):
  
    print "Uploaded file exists"
  
    # BaseName of the uploaded file
    baseName = os.path.basename(inputFile)
    
    # Name of the PDF File
    pdfFile = "%s/%s.pdf" % (path, baseName)
    pdfFile_url = "%s/%s.pdf" % (url_path, baseName)

    # New file location
    newFile = "%s/%s" % (path, baseName)
    newFile_url = "%s/%s" % (url_path, baseName)    
    
    # Check to see if the file exists in the user storage   
    if os.path.exists("%s" % (newFile)):
      if filecmp.cmp(inputFile, newFile):
        print "upload file and newFile the same, moving on"
        # Files are the same, no need to move
        pass
      else:
        # Move uploaded file into user's file location
        print "Moving uploaded file %s into location %s" % (inputFile, path)      
        shutil.move(inputFile, path)        
    else:
      # Move uploaded file into user's file location
      print "File does not exist in storage location"
      print "Moving uploaded file %s into location %s" % (inputFile, path)      
      shutil.move(inputFile, path)

    # Convert presentation to PDF
    try:
      converter = DocumentConverter()    
      converter.convert(newFile, pdfFile)
    except DocumentConversionException, exception:
      print "ERROR! " + str(exception)
      exit(1)
    except ErrorCodeIOException, exception:
      print e, exception
      print "ERROR! ErrorCodeIOException %d" % exception.ErrCode
      exit(1)
    
    # Set the new location for the slides and the PDF file
    presentationObject.presentation_slides = newFile
    presentationObject.presentation_slides_url = newFile_url
    
    presentationObject.presentation_pdf = pdfFile
    presentationObject.presentation_pdf_url = pdfFile_url
    
    # Generate the hash for the presentation
    presentationObject.generate_hash(baseName)
    
    # Save the object
    presentationObject.save()
    
    # Call the task to generate the thumbnail
    generate_thumbnail.delay(presentationObject)
  else:
    exit(1)
    
        
@task
def generate_thumbnail(presentationObject, size = "260x180"):

  pdfFile = presentationObject.presentation_pdf
  pngFile = re.sub("pdf", "png", os.path.basename(pdfFile))
  path = os.path.dirname(pdfFile)
  url_path = os.path.dirname(presentationObject.presentation_pdf_url)
      
  #
  # TODO: Replace with python code
  #
  params = ["/usr/bin/convert", "-resize", size, "%s[0]" % pdfFile, "%s/%s" % (path, pngFile)]
  subprocess.check_call(params)
  
  # Set the thumbnail and save the object
  presentationObject.presentation_thumbnail = "%s/%s" % (url_path, pngFile)
  presentationObject.save()
  
  
@task
def geocode(location,sensor="false", **geo_args):

  GEOCODE_BASE_URL = 'http://maps.google.com/maps/api/geocode/json'

  address = "%s %s %s %s" % (location.street_address, location.city, location.state, location.country)
  geo_args = {
    'address': address,
    'sensor': sensor  
  }

  url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
  result = simplejson.load(urllib.urlopen(url))

  if result['status'] == 'OK':
    location.longitude = result['results'][0]['geometry']['location']['lng']
    location.latitude = result['results'][0]['geometry']['location']['lat']
    
    location.save()
        
  else:
    return None
  
  
  
  
  
  
  

