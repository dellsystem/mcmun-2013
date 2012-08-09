from django.conf.urls import patterns, include, url
from mcmun.pages import pages

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cms.views.main', name='home'),
    url(r'^dashboard', 'mcmun.views.dashboard', name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^committees/', include('committees.urls')),
    url(r'^signups/', include('signups.urls')),
    url(r'^registration', 'mcmun.views.registration', name='registration'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^', include('cms.urls')),
)
