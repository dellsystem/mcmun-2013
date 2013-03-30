from django.conf.urls import patterns, include, url

urlpatterns = patterns('signups.views',
	url(r'^(?P<category>\w+)/?$', 'submit', name='submit_signup'),
)
