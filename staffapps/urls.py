from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'cms.views.main', name='staff-application'),
    url(r'^coordinator$', 'staffapps.views.coordinator', name='coordinator-application'),
    url(r'^committees$', 'staffapps.views.committees', name='committees-application'),
    url(r'^logistical$', 'staffapps.views.logistical', name='logistical-application'),
    url(r'^coordinator_cvs/(?P<file_name>[^/]+)', 'staffapps.views.serve_cvs'),
)
