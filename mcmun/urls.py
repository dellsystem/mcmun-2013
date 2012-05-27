from django.conf.urls import patterns, include, url
from mcmun.pages import pages

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cms.views.main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)
