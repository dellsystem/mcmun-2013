import os

from django.shortcuts import render
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.static import serve

from staffapps.forms import CoordinatorAppForm
from staffapps.models import cv_upload_path


def coordinator(request):
	if request.method == 'POST':
		form = CoordinatorAppForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()

			context = {
				'page': {
					'long_name': 'Application successfully submitted',
				},
				'application_type': 'coordinator',
			}

			return render(request, 'staffapps/success.html', context)
	else:
		form = CoordinatorAppForm()

	context = {
		'page': {
			'long_name': 'Staff coordinator application',
		},
		'form': form,
	}

	return render(request, 'staffapps/coordinator.html', context)

@login_required
def serve_cvs(request, file_name):
	# Could be worse
	if request.user.is_staff:
		return serve(request, file_name, os.path.join(settings.MEDIA_ROOT, cv_upload_path))
	else:
		raise HttpResponseForbidden
