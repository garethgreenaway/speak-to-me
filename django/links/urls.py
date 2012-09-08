from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^add/tripit$', 'links.views.addTripIt'),
    url(r'^authorized/tripit$', 'links.views.authorizedTripIt'),
    url(r'^added$', 'links.views.added'),
)

