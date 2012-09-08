from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from feed.models import Feed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^add/$', 'feed.views.addFeed'),
    url(r'^added/$', 'feed.views.addedFeed'),
)

