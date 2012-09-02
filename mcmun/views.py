from mcmun.forms import RegistrationForm, ScholarshipForm
from mcmun.constants import MIN_NUM_DELEGATES, MAX_NUM_DELEGATES
from mcmun.models import RegisteredSchool, ScholarshipApp

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django_xhtml2pdf.utils import generate_pdf
from django.shortcuts import render


def home(request):
	return render(request, "home.html")


def registration(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():
			registered_school = form.save()
			registered_school.pays_convenience_fee = True
			registered_school.save()

			# Send emails to user, stysis, myself
			registered_school.send_success_email()

			data = {
				'page': {
					'long_name': 'Succcessful registration'
				}
			}

			return render(request, "registration_success.html", data)
	else:
		form = RegistrationForm()

	data = {
		'form': form,
		'page': {
			'long_name': 'Registration',
		},
		'min_num_delegates': MIN_NUM_DELEGATES,
		'max_num_delegates': MAX_NUM_DELEGATES,
	}

	return render(request, "registration.html", data)


@login_required
def dashboard(request):
	form = None
	school = None
	if request.user.registeredschool_set.count():
		# There should only be one anyway (see comment in models.py)
		school = request.user.registeredschool_set.filter(is_approved=True)[0]

		# Iff there is no scholarship application with this school, show the form
		if ScholarshipApp.objects.filter(school=school).count() == 0:
			if request.method == 'POST':
				form = ScholarshipForm(request.POST)

				if form.is_valid():
					scholarship_app = form.save(commit=False)
					scholarship_app.school = school
					scholarship_app.save()

					# Show the "thank you for your application" message
					form = None
			else:
				form = ScholarshipForm()
	elif request.user.is_staff:
		# Show a random school (the first one registered)
		# Admins can see the dashboard, but can't fill out a scholarship app
		school = RegisteredSchool.objects.get(pk=1)

	data = {
		'school': school,
		'form': form,
		# Needed to show the title (as base.html expects the CMS view)
		'page': {
			'long_name': 'Your dashboard',
		},
	}

	return render(request, "dashboard.html", data)
