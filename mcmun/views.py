import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django_xhtml2pdf.utils import generate_pdf
from django.shortcuts import render, redirect

from committees.forms import CommitteeAssignmentFormSet, DelegateAssignmentFormset
from committees.models import DelegateAssignment
from committees.utils import get_committee_from_email
from mcmun.forms import RegistrationForm, ScholarshipForm, EventForm, CommitteePrefsForm
from mcmun.constants import MIN_NUM_DELEGATES, MAX_NUM_DELEGATES
from mcmun.models import RegisteredSchool, ScholarshipApp


def home(request):
	return render(request, "home.html")


def registration(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():
			# Simple spam-prevention technique
			if not request.POST.get('address', '').startswith('http://'):
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
	# If it's a dais member, redirect to that committee's position paper listing
	if request.user.username.endswith('@mcmun@.org'):
		dais_committee = get_committee_from_email(request.user.username)
		if dais_committee:
			return redirect(dais_committee)

	form = None
	school = None
	event_form = None
	committees_form = None

	if request.user.registeredschool_set.count():
		# There should only be one anyway (see comment in models.py)
		school = request.user.registeredschool_set.filter(is_approved=True)[0]

		# Only show it if the user has not entered values yet
		if school.num_pub_crawl == 0 and school.num_non_alcohol == 0:
			event_form = EventForm(instance=school)

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

		# If we haven't passed the committee prefs deadline, show the form
		prefs_deadline = datetime.datetime(2012, 11, 19) # Nov 18 midnight
		if datetime.datetime.now() < prefs_deadline:
			committees_form = CommitteePrefsForm(instance=school)
	elif request.user.is_staff:
		# Show a random school (the first one registered)
		# Admins can see the dashboard, but can't fill out any forms
		school = RegisteredSchool.objects.get(pk=1)

	com_assignments = school.committeeassignment_set.all()
	formset = CommitteeAssignmentFormSet(queryset=com_assignments, prefix='lol')
	del_forms = []
	for com_assignment in com_assignments:
		del_forms.append(DelegateAssignmentFormset(queryset=com_assignment.delegateassignment_set.all(), prefix='%d' % com_assignment.id))

	data = {
		'management_forms': [formset.management_form] + [f.management_form for f in del_forms],
		'formset': zip(formset, del_forms),
		'unfilled_assignments': school.has_unfilled_assignments(),
		'school': school,
		'event_form': event_form,
		'committees_form': committees_form,
		'form': form,
		# Needed to show the title (as base.html expects the CMS view)
		'page': {
			'long_name': 'Your dashboard',
		},
	}

	return render(request, "dashboard.html", data)


@login_required
def assignments(request):
	"""
	For updating assignments and handling position paper uploads
	"""
	user_schools = request.user.registeredschool_set.filter(is_approved=True)

	# Why ...
	if request.method == 'POST' and user_schools.count() == 1:
		school = user_schools[0]
		com_assignments = school.committeeassignment_set.all()
		formset = CommitteeAssignmentFormSet(request.POST, request.FILES, queryset=com_assignments, prefix='lol')
		formset.save()
		for com_ass in com_assignments:
			formset = DelegateAssignmentFormset(request.POST, request.FILES, queryset=com_ass.delegateassignment_set.all(), prefix='%d' % com_ass.id)
			formset.save()

	return redirect(dashboard)

@login_required
def events(request):
	user_schools = request.user.registeredschool_set.filter(is_approved=True)

	if request.method == 'POST' and user_schools.count() == 1:
		school = user_schools[0]
		form = EventForm(request.POST, instance=school)

		if form.is_valid():
			form.save()

	return redirect(dashboard)


@login_required
def committee_prefs(request):
	# Fix this
	user_schools = request.user.registeredschool_set.filter(is_approved=True)

	if request.method == 'POST' and user_schools.count() == 1:
		school = user_schools[0]
		form = CommitteePrefsForm(request.POST, instance=school)

		if form.is_valid():
			form.save()

	return redirect(dashboard)
