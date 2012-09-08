import math

from django.db import models

class Location(models.Model):

  class Meta:
    app_label = 'home'
    
  nickname = models.CharField(max_length=100, verbose_name="Nick Name")

  street_address = models.CharField(max_length=100)
  street_address_hidden = models.BooleanField(verbose_name="Hidden")
  
  city = models.CharField(max_length=100)
  city_hidden = models.BooleanField(verbose_name="Hidden")
  
  state = models.CharField(max_length=100, verbose_name="State / Province")
  country = models.CharField(max_length=100)
  postalcode = models.CharField(max_length=100)
    
  latitude = models.DecimalField(decimal_places=6, max_digits=9, blank=True, null=True)
  longitude = models.DecimalField(decimal_places=6, max_digits=9, blank=True, null=True)  

  def __unicode__(self):
      return "%s, %s, %s, %s" % (self.street_address, self.city, self.state, self.country)
      
  def distance_to_latlong(self, target):
    """ Returns the distance (in miles) of a zipcode's lat/long to
    a given target lat/long. This is basically a conversion of the
    javascript here: http://www.movable-type.co.uk/scripts/latlong.html """

    EARTH_RADIUS = 3440.07 # in n.miles
    NAUTICAL_TO_MILE_CONV = 1.15077945 # convert n.miles back to miles

    d_lat = Location.degrees_to_radians(target.latitude - self.latitude)
    d_long = Location.degrees_to_radians(target.longitude - self.longitude)
    source_lat = Location.degrees_to_radians(target.latitude)
    target_lat = Location.degrees_to_radians(self.latitude)

    hv_a = math.sin(d_lat/2)*math.sin(d_lat/2) + math.cos(source_lat) * math.cos(target_lat) * math.sin(d_long/2) * math.sin(d_long/2)
    hv_c = 2 * math.atan2(math.sqrt(hv_a), math.sqrt(1 - hv_a))
    hv_distance = EARTH_RADIUS * hv_c

    return hv_distance * NAUTICAL_TO_MILE_CONV

  @staticmethod
  def degrees_to_radians(value):
    """ Returns a Lat/Long degree value to radian equivilant """
    return float(value)*math.pi/180.0

  @staticmethod
  def radians_to_degrees(value):
    return value*180.0/math.pi
    
  @staticmethod
  def miles_to_radians(value):
    """ Returns the radian value of a mile value. We need to convert
    to nautical miles first as the formula's use those """
    NAUTICAL_MILE_CONV = 0.868976 # convert miles to nautical miles
    nmiles = float(value) * NAUTICAL_MILE_CONV
    return nmiles * math.pi / (180.0 * 60.0)

  @staticmethod
  def calculate_latitude(source_lat, distance, heading):
    """ Calculates the latitude for a source point given a certain distance and heading direction. Values are in radians """
    return math.asin(math.sin(source_lat) * math.cos(distance) + math.cos(source_lat) * math.sin(distance) * math.cos(heading))

  @staticmethod
  def calculate_longitude(prior_lat, source_long, distance, heading):
    """ Caclulated the longitude of a point. You *MUST* supply the
    (precalculted) latitude for the target point, so this call should
    always come after calculate_latitude """

    return ((source_long - math.asin(math.sin(heading) * math.sin(distance) / math.cos(prior_lat)) + math.pi) % (2 * math.pi)) - math.pi

  def within_radius(self, radius=5.0):
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

    # These are our 4 points (N/S/E/W) We use this to build a bounding box
    HEADINGS = enumerate([0, math.pi/2, math.pi, 3*math.pi/2])

    source_lat = Location.degrees_to_radians(self.latitude)
    source_long = Location.degrees_to_radians(self.longitude)
    distance = Location.miles_to_radians(radius)

    boundries = []

    for (cnt, heading) in HEADINGS:
        target_lat = Location.calculate_latitude(source_lat, distance, heading)
        target_long = Location.calculate_longitude(target_lat, source_long, distance, heading)

        boundries.append([Location.radians_to_degrees(target_lat), Location.radians_to_degrees(target_long)])

    entries = Location.objects.all().select_related().filter(latitude__lte=str(boundries[0][0]),latitude__gte=str(boundries[2][0]), longitude__gte=str(boundries[1][1]),longitude__lte=str(boundries[3][1]))

    entry_data = list()
    for entry in entries:
      # Don't want to include our starting point
      if entry != self:
        entry_data.append(dict(
          distance=entry.distance_to_latlong(self),
          object_id=entry,
          )
        )
    entry_data.sort() # return orderd by distance
    # now fix the bounding box SQL to limit within our radius
    sorted_data = [elem['object_id'] for elem in entry_data if elem['distance']<radius]
    return sorted_data
