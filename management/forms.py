from django import forms
from django.forms import Form, ModelForm
from django.forms import modelformset_factory
from .models import Group, Child, Parent, Teacher, PresenceList


class LoginForm(Form):
	login = forms.CharField(label="Twój login", max_length=100)
	password = forms.CharField(label="Hasło", max_length=100, widget=forms.PasswordInput())


class PresenceDateForm(Form):
	day = forms.DateField()


class ChildForm(Form):
	first_name = forms.CharField(label='Imię')
	last_name = forms.CharField(label='Nazwisko')
	group = forms.RadioSelect()
	start_hour = forms.TimeField(label='Godzina przyjścia')
	end_hour = forms.TimeField(label='Godzina wyjścia')
	breakfast = forms.NullBooleanField(label='Śniadanie')
	brunch = forms.NullBooleanField(label='Drugie śdniadanie')
	dinner = forms.NullBooleanField(label='Obiad')
	supper = forms.NullBooleanField(label='Kolacja')
	kdr = forms.NullBooleanField(label='Karta Dużej Rodziny')


class AddChildForm(ModelForm):
	class Meta:
		model = Child
		fields = ('first_name', 'last_name', 'kdr', 'start_hour',
			'end_hour', 'breakfast', 'brunch', 'dinner', 'supper', 'group')


class PresenceListForm(Form): 

	def get_children(self, group): 
		return Child.objects.filter(group=group) 

	def __init__(self, *args, **kwargs): 
		date = kwargs.pop('date')
		group = kwargs.pop('group') 
									
		super(PresenceListForm, self).__init__(*args, **kwargs)

		for child in self.get_children(group=group):
			try:
				presence = child.presencelist_set.get(day=date).present 
			except:
				presence = False 
			
			self.fields['child_{}_present'.format(child.id)] = forms.NullBooleanField(initial=presence, label=child.name) 

