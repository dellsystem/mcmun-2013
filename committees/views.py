from django.shortcuts import render, get_object_or_404
from django.conf import settings

from committees.models import Committee
from committees.forms import AdHocAppForm, BRICSAppForm, NixonAppForm, WallStreetAppForm


def view(request, slug):
	committee = get_object_or_404(Committee, slug=slug)

	data = {
		'page': {
			'long_name': committee.name,
		},
		'committee': committee,
		'dais_template': 'dais_photos/%s.html' % committee.slug,
		'DAIS_PHOTO_URL': '%simg/dais/%s/' % (settings.STATIC_URL, committee.slug),
	}

	return render(request, 'committee.html', data)


def application(request, slug):
	# Hard-coding the list of committees with applications for now
	# This should really be a field on the committee (for next year)
	committee = get_object_or_404(Committee, slug=slug)

	app_forms = {
		'ad-hoc': AdHocAppForm,
		'brics': BRICSAppForm,
		'frost-nixon': NixonAppForm,
		'wall-street': WallStreetAppForm,
	}

	if slug in app_forms:
		app_form = app_forms[slug]

	if request.method == 'POST':
		form = app_form(request.POST)

		if form.is_valid():
			form.save()

			data = {
				'committee': committee,
				'page': {
					'long_name': 'Successful application for %s' % committee.name,
				}
			}

			return render(request, 'committee_app_success.html', data)
	else:
		form = app_form

	data = {
		'deadline': 'November 18th',
		'page': {
			'long_name': 'Application for %s' % committee.name,
		},
		'intro_template': 'committee_apps/%s.md' % slug,
		'committee': committee,
		'form': form,
	}

	return render(request, 'committee_app.html', data)
