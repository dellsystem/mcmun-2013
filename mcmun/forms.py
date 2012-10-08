import re

from mcmun.models import RegisteredSchool, ScholarshipApp

from django import forms


class EventForm(forms.ModelForm):
	class Meta:
		model = RegisteredSchool
		fields = (
			'num_pub_crawl',
			'num_non_alcohol',
		)


class RegistrationForm(forms.ModelForm):
	class Meta:
		model = RegisteredSchool
		fields = (
			'school_name',
			'address',
			'country',
			'first_name',
			'last_name',
			'email',
			'phone_number',
			'num_delegates',
			'use_online_payment',
			'use_tiered',
			#'use_priority',
		)

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number']
		if re.search('[^0-9-+() ]+', phone_number) is not None:
			raise forms.ValidationError("")
		else:
			return phone_number


class ScholarshipForm(RegistrationForm):
	class Meta:
		model = ScholarshipApp
		exclude = ('school',)
