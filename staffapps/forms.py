from django import forms

from staffapps.models import CoordinatorApp


class CoordinatorAppForm(forms.ModelForm):
	class Meta:
		model = CoordinatorApp
