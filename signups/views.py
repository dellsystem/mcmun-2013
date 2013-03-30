from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.core.validators import email_re

from signups.models import Person, SIGNUP_CATEGORIES


def submit(request, category):
	categories = [x[1].lower() for x in SIGNUP_CATEGORIES]

	# Looks like a malicious request - ignore (go back to homepage)
	if category not in categories or request.method != 'POST':
		return redirect('home')
	else:
		email = request.POST.get('email', '')
		name = request.POST.get('name', '')

		title = 'Unable to process submission'
		if email == '' or not email_re.match(email):
			message = 'Please enter a valid email address and name.'
		elif name == '':
			message = 'Please enter your name.'
		else:
			try:
				Person.objects.create(email=email, name=name, category=categories.index(category))
				title = 'Successful signup'
				message = 'Thank you for signing up for our %s listserv.' % category
			except IntegrityError:
				message = 'That email address has already been used. Perhaps you signed up before and forgot about it?'

		# Why is this method so messy. Switch to using forms later?
		data = {
			'title': title,
			'message': message
		}

		return render(request, 'confirmation.html', data)
