import re

from mcmun.models import RegisteredSchool

from django import forms


class RegistrationForm(forms.ModelForm):
	class Meta:
		model = RegisteredSchool
		exclude = ('account', 'is_approved', 'amount_paid')

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number']
		if re.search('[^0-9-+() ]+', phone_number) is not None:
			raise forms.ValidationError("")
		else:
			return phone_number
