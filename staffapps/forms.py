from django import forms

from staffapps.models import CoordinatorApp, LogisticalApp, CommitteesApp


class CoordinatorAppForm(forms.ModelForm):
	class Meta:
		model = CoordinatorApp


class LogisticalAppForm(forms.ModelForm):
	class Meta:
		model = LogisticalApp


class CommitteesAppForm(forms.ModelForm):
	class Meta:
		model = CommitteesApp
