import os

from django.shortcuts import render
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.static import serve

from staffapps.forms import CoordinatorAppForm, LogisticalAppForm, CommitteesAppForm
from staffapps.models import cv_upload_path

"""
TODO: Clean this file up sometime
"""


def application_success(request, app_type):
	context = {
		'page': {
			'long_name': 'Application successfully submitted',
		},
		'application_type': app_type,
	}

	return render(request, 'staffapps/success.html', context)


def committees(request):
	if request.method == 'POST':
		form = CommitteesAppForm(request.POST)

		if form.is_valid():
			form.save()

			return application_success(request, 'committees')
	else:
		form = CommitteesAppForm()

	context = {
		'page': {
			'long_name': 'Committees staff application',
		},
		'form': form,
	}

	return render(request, 'staffapps/committees.html', context)


def logistical(request):
	if request.method == 'POST':
		form = LogisticalAppForm(request.POST)

		if form.is_valid():
			form.save()

			return application_success(request, 'logistical')
	else:
		form = LogisticalAppForm()

	context = {
		'page': {
			'long_name': 'Logistical staff application',
		},
		'form': form,
	}

	return render(request, 'staffapps/logistical.html', context)


def coordinator(request):
	if request.method == 'POST':
		form = CoordinatorAppForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()

			return application_success(request, 'coordinator')
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
