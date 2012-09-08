from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'index'),
    url(r'^signout/$', 'logout_view'),
    url(r'^address/add/$', 'address_add'),
)

