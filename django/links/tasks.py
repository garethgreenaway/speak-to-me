from celery.task import periodic_task
from celery.task import task
from celery.task.schedules import crontab

from datetime import timedelta

from links.models import TripItUser, TripItTrip

import json
import simplejson
import urllib

import tripit
import creds

#@periodic_task(run_every=crontab(minute="*/1"))
@task
def sync_tripit_trips():

    api_url = 'https://api.tripit.com/'

    for tripit_user in TripItUser.objects.all():

        current_trips = {}
        for item in TripItTrip.objects.filter(user = tripit_user):
            current_trips[str(item.trip_id)] = {}
            current_trips[str(item.trip_id)]['start_date'] = item.start_date
            current_trips[str(item.trip_id)]['end_date'] = item.end_date
            current_trips[str(item.trip_id)]['is_private'] = item.is_private

        oauth_credential = tripit.OAuthConsumerCredential(creds.OAUTH_KEY, creds.OAUTH_SECRET, tripit_user.oauth_token, tripit_user.oauth_token_secret)

        try:
            t = tripit.TripIt(oauth_credential, api_url = api_url)
        except URLError:
            return False

        try:
            json_data = t._do_request(verb = "/list/trip/format/json")
            data = json.loads(json_data)
        except URLError:
            return False

        for trip in data['Trip']:
            
            if not trip['id'] in current_trips:
                new_trip = TripItTrip()
                new_trip.user = tripit_user
                new_trip.trip_id = trip['id']
                new_trip.display_name = trip['display_name']
                new_trip.start_date = trip['start_date']
                new_trip.end_date = trip['end_date']
                new_trip.city = trip['PrimaryLocationAddress']['city']
                new_trip.state = trip['PrimaryLocationAddress']['state']
                new_trip.county = trip['PrimaryLocationAddress']['country']
                new_trip.longitude = trip['PrimaryLocationAddress']['longitude']
                new_trip.latitude = trip['PrimaryLocationAddress']['latitude']
                new_trip.is_private = trip['is_private']
                new_trip.save()
            else:
                current_trip = TripItTrip.objects.get(trip_id = trip['id'])

                if current_trip.start_date != trip['start_date']: current_trip.start_date = trip['start_date']

                if current_trip.end_date != trip['end_date']: current_trip.end_date = trip['end_date']

                if current_trip.is_private != trip['is_private']: current_trip.is_private = trip['is_private']

                current_trip.save()

        return True


@task
def geocode(address="New+York,+NY",sensor="false", **geo_args):

  GEOCODE_BASE_URL = 'http://maps.google.com/maps/api/geocode/json'

  geo_args = {
    'address': address,
    'sensor': sensor  
  }

  url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
  result = simplejson.load(urllib.urlopen(url))

  if result['status'] == 'OK':
    return result['results'][0]['geometry']['location']
    #print result['results'][0]['geometry']['location_type']
    #print simplejson.dumps([s['formatted_address'] for s in result['results']], indent=2)
  else:
    return None
