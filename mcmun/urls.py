from django.conf.urls import patterns, include, url
from mcmun.pages import pages

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cms.views.main', name='home'),
    url(r'^dashboard', 'mcmun.views.dashboard', name='dashboard'),
    url(r'^event-registration', 'mcmun.views.events', name='events'),
    url(r'^committee-prefs', 'mcmun.views.committee_prefs', name='committee_prefs'),
    url(r'^assignments', 'mcmun.views.assignments', name='assignments'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^committees/', include('committees.urls')),
    url(r'^staff-application/', include('staffapps.urls')),
    url(r'^signups/', include('signups.urls')),
    url(r'^registration', 'mcmun.views.registration', name='registration'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^password$', 'django.contrib.auth.views.password_change', {'template_name': 'password.html'}, name='password'),
    url(r'^password_success$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_success.html'}, name="password_success"),
    url(r'^position-papers/(?P<file_name>[^/]+)', 'committees.views.serve_papers'),
    url(r'^nikhilerror$', 'mcmun.views.nikhil_error'),
    url(r'^', include('cms.urls')),
)
