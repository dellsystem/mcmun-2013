from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'cms.views.main', name='staff-application'),
    url(r'^coordinator$', 'staffapps.views.coordinator', name='coordinator-application'),
    url(r'^coordinator_cvs/(?P<file_name>[^/]+)', 'staffapps.views.serve_cvs'),
)
