from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from committees.models import Committee


def view(request, slug):
	try:
		committee = Committee.objects.get(slug=slug)
	except Committee.DoesNotExist:
		raise Http404

	data = {
		'page': {
			'long_name': committee.name,
		},
		'committee': committee,
		'dais_template': 'dais_photos/%s.html' % committee.slug,
		'DAIS_PHOTO_URL': '%simg/dais/%s/' % (settings.STATIC_URL, committee.slug),
	}

	return render(request, 'committee.html', data)
