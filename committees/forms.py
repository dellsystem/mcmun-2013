from committees.models import AdHocApplication, BRICSApplication, NixonApplication, WallStreetApplication, \
	CommitteeAssignment, DelegateAssignment

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


CommitteeAssignmentFormSet = forms.models.modelformset_factory(CommitteeAssignment,
	fields=('position_paper',), extra=0)

DelegateAssignmentFormset = forms.models.modelformset_factory(DelegateAssignment,
	fields=('delegate_name',), extra=0)
