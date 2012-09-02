from committees.models import AdHocApplication, BRICSApplication, NixonApplication, WallStreetApplication

from django import forms


class AdHocAppForm(forms.ModelForm):
	class Meta:
		model = AdHocApplication


class BRICSAppForm(forms.ModelForm):
	class Meta:
		model = BRICSApplication


class NixonAppForm(forms.ModelForm):
	class Meta:
		model = NixonApplication


class WallStreetAppForm(forms.ModelForm):
	class Meta:
		model = WallStreetApplication
