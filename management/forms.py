from django import forms
from django.forms import Form, ModelForm
from django.forms import modelformset_factory
from .models import Group, Child, Parent, Teacher, PresenceList, Meal


class PresenceDateForm(Form):
	day = forms.DateField()


class PresenceListForm(ModelForm):
	present = forms.ChoiceField()
	child = forms.ChoiceField()

PresenceListFormSet = modelformset_factory(PresenceList, fields=('present', 'child'))