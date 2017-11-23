from django import forms
from django.forms import Form, ModelForm
from django.forms import modelformset_factory
from .models import Group, Child, Parent, Teacher, PresenceList, Meal


class LoginForm(Form):
	login = forms.CharField(label="Twój login", max_length=100)
	password = forms.CharField(label="Hasło", max_length=100, widget=forms.PasswordInput())


class PresenceDateForm(Form):
	day = forms.DateField()



meal_list = (
			(0, "śniadanie"),
			(1, "drugie śniadanie"),
			(2, "obiad"),
			(3, "podwieczorek")
		)

class AddChildForm(ModelForm):
	class Meta:
		model = Child
		fields = ('first_name', 'last_name', 'kdr', 'start_hour',
			'end_hour', 'breakfast', 'brunch', 'dinner', 'supper', 'group')
		
	# first_name = forms.CharField(label='Imię')
	# last_name = forms.CharField(label='Nazwisko')
	# kdr = forms.NullBooleanField(label='Karta Dużej Rodziny')
	# start_hour = forms.TimeField(label='Godzina przyjścia')
	# end_hour = forms.TimeField(label='Godzina wyjścia')
	# meal = forms.MultipleChoiceField(label='posiłki', choices='meal_list', 
	# 						widget=forms.CheckboxSelectMultiple)
	# group = forms.RadioSelect()

	# breakfast = forms.NullBooleanField(label='śniadanie')
	# brunch = forms.NullBooleanField(label='drugie śdniadanie')
	# dinner = forms.NullBooleanField(label='obiad')
	# supper = forms.NullBooleanField(label='kolacja')
	


class PresenceListForm(Form): # tworzymy ten formularz samodzielnie

	def get_children(self, group): # tworzymy metodę get_children, która zwraca nam listę dzieci z danej grupy 
		return Child.objects.filter(group=group) # metodę tą wykorzystujemy też w views

	def __init__(self, *args, **kwargs): 
		date = kwargs.pop('date') #podaję argumenty z PresenceList, których będę używać  
		group = kwargs.pop('group') #używamy pop, ponieważ musimy usunąć te argumenty z __init__, jesli tego nie zrobimy, to poniżej -
									# przy wywołaniu __init__ w super, do tych argumentów będzie się próbował odwołać __init__ i się będzie wywalał
		super(PresenceListForm, self).__init__(*args, **kwargs)

		for child in self.get_children(group=group):
			try:
				presence = child.presencelist_set.get(day=date).present # pobieram pole present z PresenceList w relacji z Child
			except:
				presence = False 
			# self.fields['child_{}_name'.format(child.id)] = forms.CharField(initial=child.name, disabled=True, label='')
			self.fields['child_{}_present'.format(child.id)] = forms.NullBooleanField(initial=presence, label=child.name) # sposób zapisu pola formularza   formularza


#PresenceListFormSet = modelformset_factory(PresenceList, fields=('present', 'child'))

