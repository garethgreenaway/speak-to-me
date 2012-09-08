import sys
import time

import oauth2 as oauth

import creds

import tripit

if __name__ == '__main__':

    api_url = 'https://api.tripit.com/'

    # get request token
    oauth_credential = tripit.OAuthConsumerCredential(oauth_consumer_key=creds.OAUTH_KEY, oauth_consumer_secret=creds.OAUTH_SECRET)
    t = tripit.TripIt(oauth_credential, api_url = api_url)
    request_token = t.get_request_token()

    url = "https://www.tripit.com/oauth/authorize?oauth_token=%s&oauth_callback=http%3A%2F%2Fwww.tripit.com%2Fhome" % (request_token['oauth_token'])

    # get authorized token
    oauth_credential = tripit.OAuthConsumerCredential(creds.OAUTH_KEY, creds.OAUTH_SECRET, request_token['oauth_token'], request_token['oauth_token__secret'])
    t = tripit.TripIt(oauth_credential, api_url = api_url)
    print t.get_access_token()

