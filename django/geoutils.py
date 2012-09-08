import math

def distance_to_latlong(self, latlong):
  """ Returns the distance (in miles) of a zipcode's lat/long to
  a given target lat/long. This is basically a conversion of the
  javascript here: http://www.movable-type.co.uk/scripts/latlong.html """

  EARTH_RADIUS = 3440.07 # in n.miles
  NAUTICAL_TO_MILE_CONV = 1.15077945 # convert n.miles back to miles

  d_lat = GeoEntry.degrees_to_radians(latlong[0] - self.latitude)
  d_long = GeoEntry.degrees_to_radians(latlong[1] - self.longitude)
  source_lat = GeoEntry.degrees_to_radians(latlong[0])
  target_lat = GeoEntry.degrees_to_radians(self.latitude)

  hv_a = math.sin(d_lat/2)*math.sin(d_lat/2) + math.cos(source_lat)*math.cos(target_lat) * math.sin(d_long/2)*math.sin(d_long/2)
  hv_c = 2*math.atan2(math.sqrt(hv_a), math.sqrt(1-hv_a))
  hv_distance = EARTH_RADIUS * hv_c

  return hv_distance * NAUTICAL_TO_MILE_CONV

def degrees_to_radians(value):
  """ Returns a Lat/Long degree value to radian equivilant """
  return float(value)*math.pi/180.0

def radians_to_degrees(value):
  return value*180.0/math.pi

def miles_to_radians(value):
  """ Returns the radian value of a mile value. We need to convert
  to nautical miles first as the formula's use those """
  NAUTICAL_MILE_CONV = 0.868976 # convert miles to nautical miles
  nmiles = float(value)*NAUTICAL_MILE_CONV
  return nmiles*math.pi/(180.0*60.0)

def calculate_latitude(source_lat, distance, heading):
  """ Calculates the latitude for a source point given a certain distance and heading direction. Values are in radians """
  return math.asin(math.sin(source_lat)*math.cos(distance) + math.cos(source_lat)*math.sin(distance)*math.cos(heading))

def calculate_longitude(prior_lat, source_long, distance, heading):
  """ Caclulated the longitude of a point. You *MUST* supply the
  (precalculted) latitude for the target point, so this call should
  always come after calculate_latitude """

  return ((source_long - math.asin(math.sin(heading)*math.sin(distance)/math.cos(prior_lat)) + math.pi) % (2*math.pi)) - math.pi

def within_radius(lat, long, radius=5.0, ctype_fields=None):
  """ Takes an input latlong & desired radius, works out the square
  (not circular) boundry box for it and returns the object id's
  which fall within it. The method itself is outlined here:
  http://www.codeproject.com/KB/cs/zipcodeutil.aspx

  With lots of detail on the calculations here:
  http://mathforum.org/library/drmath/view/51816.html.

  The radius parameter is specified in *miles*. It's then
  converted into nautical miles & radians for further
  calculations.

  The actual query filters based on a box around the point, not
  a circle. So the end result is the area is around 22% larger
  than the "true" size. This can be further filtered on thesclient
  side or in the views rather than creating a complicated
  query. For most searches it's probably not a major problem
  in any case.

  Returns a list of distances increasingly far from
  our request point along with the content object's primary key
  and type for use in further lookups. By passing through a list
  of fields you can optionally get more data back. The returned
  array is ideally suited as being returned as JSON.
  """

  radius = float(radius) # may come through as str

  #if type(latlong) == GeoEntry:
  #  latlong = [latlong.latitude, latlong.longitude]

  # These are our 4 points (N/S/E/W) We use this to build a bounding box
  HEADINGS = enumerate([0, math.pi/2, math.pi, 3*math.pi/2])

  #try:
  #  geoentry = GeoEntry.objects.get(latitude=lat, longitude=long)
  #except GeoEntry.DoesNotExist:
  #  # Maybe handle more gracefully?
  #  raise Exception('No GeoEntry matching query')
  #except GeoEntry.MultipleObjectsReturned:
  #  # In this case lets use the first one instead for now
  #  geoentry = GeoEntry.objects.filter(latitude=latlong[0], longitude=latlong[1])[0]

  source_lat = degrees_to_radians(lat)
  source_long = degrees_to_radians(long)
  distance = miles_to_radians(radius)

  boundries = []

  for (cnt, heading) in HEADINGS:
      target_lat = calculate_latitude(source_lat, distance, heading)
      target_long = calculate_longitude(target_lat, source_long, distance, heading)

      boundries.append([radians_to_degrees(target_lat), \
          radians_to_degrees(target_long)])

  print boundries          
  return

  entries = GeoEntry.objects.all().select_related().filter(latitude__lte=str(boundries[0][0]),
      latitude__gte=str(boundries[2][0]), longitude__gte=str(boundries[1][1]),
      longitude__lte=str(boundries[3][1]))

  entry_data = list()
  for entry in entries:
    obj = entry.content_object
    ctype_dict = None,
    if obj and ctype_fields:
      if (len(ctype_fields)==1 and ctype_fields[0]=='all'):
        ctype_list = list()
        for field in obj._meta.fields:
          field_data = getattr(obj, field.name)
          if type(field_data) == unicode:
            ctype_list.append([field.name, field_data.encode('utf-8')])
          else:
            ctype_list.append([field.name, str(field_data)])
          ctype_dict = dict(ctype_list)
      else:
        ctype_dict = dict([[field, getattr(obj, field)] for field in ctype_fields])
    entry_data.append(dict(
      distance=entry.distance_to_latlong((latlong[0], latlong[1])),
        content_type=entry.content_type.pk,
        object_id=entry.object_id,
        object_data=ctype_dict,
        latitude=str(entry.latitude),
        longitude=str(entry.longitude),
      )
    )
  entry_data.sort() # return orderd by distance
  # now fix the bounding box SQL to limit within our radius
  sorted_data = [elem for elem in entry_data if elem['distance']<radius]
  return sorted_data
