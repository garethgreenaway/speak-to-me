import creds
import logging
import tripit

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from links.models import TripItUser

logger = logging.getLogger('links.views')
tripit_api_url = 'https://api.tripit.com/'

@login_required
def addTripIt(request):

    email = request.user.email
    logger.error(email)
    user = User.objects.get(email = email)

    # get request token
    oauth_credential = tripit.OAuthConsumerCredential(oauth_consumer_key=creds.OAUTH_KEY, oauth_consumer_secret=creds.OAUTH_SECRET)
    t = tripit.TripIt(oauth_credential, api_url = tripit_api_url)
    request_token = t.get_request_token()
    logger.error(request_token['oauth_token'])

    # Added this in temporarily, then we'll replace it with the authorized token and secret
    TripItUser(user = user, oauth_token = request_token['oauth_token'], oauth_token_secret = request_token['oauth_token_secret']).save()

    # Redirect to TripIt to authorize the token
    url = "https://www.tripit.com/oauth/authorize?oauth_token=" + request_token['oauth_token'] + "&oauth_callback=http%3A%2F%2Flocalhost%3A8080%2Flink%2Fauthorized%2Ftripit"

    logger.error(url)

    return HttpResponseRedirect(url)

@login_required
def authorizedTripIt(request):

    email = request.user.email
    logger.error(email)
    user = User.objects.get(email = email)

    tripit_user = TripItUser.objects.get(user = user)

    # get authorized token
    oauth_credential = tripit.OAuthConsumerCredential(creds.OAUTH_KEY, creds.OAUTH_SECRET, tripit_user.oauth_token, tripit_user.oauth_token_secret)
    t = tripit.TripIt(oauth_credential, api_url = tripit_api_url)
    authorized_token = t.get_access_token()
    logger.error(authorized_token)

    # Replace the token and secret with the authorized ones so we can pull the trips.
    tripit_user.oauth_token = authorized_token['oauth_token']
    tripit_user.oauth_token_secret = authorized_token['oauth_token_secret']
    tripit_user.save()

    return HttpResponseRedirect("/link/added")

@login_required
def added(request):
	return render_to_response('added.html', context_instance=RequestContext(request))
