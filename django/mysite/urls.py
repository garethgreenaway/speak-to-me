from django.conf.urls import patterns, include, url

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^link/', include('links.urls')),

    url(r'^$', 'home.views.index'),
    url(r'^logout', 'home.views.logout_view'),
    
    url(r'^find/$', 'home.views.find'),
    url(r'^hear/$', 'home.views.hear'),
    url(r'^speak/$', 'home.views.speak'),
    
    url(r'^explore/$', 'home.views.explore'),

    url(r'^search/advanced/$', 'home.views.advanced_search', name="site_advanced_search" ),
    url(r'^search/advanced', 'home.views.advanced_search', name="site_advanced_search" ),        
    url(r'^search', 'home.views.search', name="site_search" ),
        
    url(r'^signup', 'home.views.signup', name="site_signup" ),    
    
    url(r'^profile/show/$', 'home.views.profile_show'),
    url(r'^profile/show/(?P<user_hash>\w+)/$', 'home.views.profile_show'),
        
    url(r'^profile/edit/$', 'home.views.profile_edit'),
    
    url(r'^add/presentation/$', 'home.views.presentation_add'),
    url(r'^add/location/$', 'home.views.location_add'),        
    
    #url(r'^profile/new/personal', 'home.views.new_profile_personal'),
    #url(r'^profile/new/location', 'home.views.new_profile_location'),
    
    url(r'^presentations/$', 'home.views.list_presentations'),
    url(r'^presentations/(?P<page>\d+)/$', 'home.views.list_presentations'),
    
    url(r'^presentation/thumbnail/(?P<presentation_hash>\w+).png$', 'home.views.presentation_thumbnail'),
    url(r'^presentation/thumbnail/(?P<presentation_hash>\w+).pdf$', 'home.views.presentation_pdf'),
    
    url(r'ajax-upload$', 'home.views.import_uploader', name="ajax_upload" ),
    #url(r'$', upload_page, name="upload_page" ),

    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STORAGE_ROOT}),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)
