from django.shortcuts import render, redirect
from django.views import View
from .models import Group, Child, Parent, Teacher, PresenceList
from .forms import (LoginForm, PresenceDateForm, ChildForm, AddChildForm, ParentsForm,
	PresenceListForm, HoursAndMealsForm, AddTeacherForm) 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class LoginView(View):

	def get(self, request):
		form = LoginForm()
		return render(request, "login_view.html", {"form": form})

	def post(self, request):
		form = LoginForm(request.POST)
		if (form.is_valid()):
			u = authenticate(username=form.cleaned_data['username'],
				password=form.cleaned_data['password'])
			if u is not None:
				login(request, u)
				return HttpResponseRedirect('/hello')
		return HttpResponseRedirect('/')


class LogoutUserView(View):

	def get(self, request):
		logout(request)
		return HttpResponseRedirect('/')


class MainView(LoginRequiredMixin, View):

	def get(self, request):
		return render(request, "main.html")


class ChildrenListView(LoginRequiredMixin, View):

	def get(self, request):
		children = Child.objects.all().order_by("last_name")
		group = Group.objects.all()
		return render(request, "children_list.html", {"children": children,
														"group": group})
		

class GroupView(LoginRequiredMixin, View):

	def get(self, request):
		groups = Group.objects.all()
		return render (request, "group_view.html", {"groups": groups})


class GroupListView(LoginRequiredMixin, View):

	def get(self, request, group_id):
		group = Group.objects.get(pk=group_id)
		teachers = Teacher.objects.filter(group=group_id)
		children = Child.objects.filter(group=group_id).order_by("last_name")
		return render(request, "children_in_group.html", {"group": group,
														"teachers": teachers,
														"children": children})


class ChildView(LoginRequiredMixin, View):

	def get(self, request, group_id, child_id):
		group = Group.objects.get(pk=group_id)
		child = Child.objects.get(pk=child_id)
		form = AddChildForm(instance=child)
		return render(request, "child.html", {"child": child,
										"group": group,
										"form": form})

	def post(self, request, group_id, child_id):
		group = Group.objects.get(pk=group_id)
		child = Child.objects.get(pk=child_id)
		form = AddChildForm(request.POST)
		if form.is_valid():
			child.first_name = form.cleaned_data['first_name']
			child.last_name = form.cleaned_data['last_name']
			child.kdr = form.cleaned_data['kdr']
			child.start_hour = form.cleaned_data['start_hour']
			child.end_hour = form.cleaned_data['end_hour']
			child.breakfast = form.cleaned_data['breakfast']
			child.brunch = form.cleaned_data['brunch']
			child.dinner = form.cleaned_data['dinner']
			child.supper = form.cleaned_data['supper']
			child.group = form.cleaned_data['group']
			child.save()
			return HttpResponseRedirect('/group')


class AddChildView(LoginRequiredMixin, View):

	def get(self, request, group_id):
		group = Group.objects.get(pk=group_id)
		form = AddChildForm()
		return render (request, "add_child.html", {"form": form})

	def post(self, request, group_id):
		group = Group.objects.get(pk=group_id)
		form = AddChildForm(request.POST)
		if form.is_valid():
			child = Child.objects.create(first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            kdr=form.cleaned_data['kdr'],
            start_hour=form.cleaned_data['start_hour'],
            end_hour=form.cleaned_data['end_hour'],
            breakfast=form.cleaned_data['breakfast'],
            brunch=form.cleaned_data['brunch'],
            dinner=form.cleaned_data['dinner'],
            supper=form.cleaned_data['supper'],
            group=form.cleaned_data['group'])
			return HttpResponseRedirect('/group') 
		return HttpResponseRedirect('/add_child')


class ParentsView(LoginRequiredMixin, View):

	def get(self, request, group_id, child_id):
		group = Group.objects.get(pk=group_id)
		child = Child.objects.get(pk=child_id)
		parents = Parent.objects.filter(child=child_id)
		#parent.child.all()
		#form = ParentsForm(instance=parents)
		form = ParentsForm()
		return render(request, "parent.html", {"child": child,
											"parents": parents,
											"group": group,
											"form": form})

	def post(self, request, group_id, child_id):
		group = Group.objects.get(pk=group_id)
		child = Child.objects.get(pk=child_id)
		parents = Parent.objects.filter(child=child_id)
		form = ParentsForm(request.POST)
		if form.is_valid():
			parents.first_name = form.cleaned_data['first_name']
			parents.last_name = form.cleaned_data['last_name']
			parents.phone_number = form.cleaned_data['phone_number']
			parents.email = form.cleaned_data['email']
			parents.save()
			return HttpResponseRedirect('/group')



class PresenceDateView(LoginRequiredMixin, View): 

	def get(self, request, group_id):
		form = PresenceDateForm()
		group = Group.objects.get(pk=group_id)
		return render(request, "presence_date.html", {"form": form,
														"group": group})

	def post(self, request, group_id): 
		form = PresenceDateForm(request.POST)
		if form.is_valid():
			date_form = form.cleaned_data['day'] 
			return HttpResponseRedirect(reverse('presence_list', kwargs={"date": date_form, "group_id": group_id}))
		return HttpResponseRedirect('presence_date')


class PresenceListView(LoginRequiredMixin, View): 

	def get(self, request, group_id, date):
		group = Group.objects.get(pk=group_id)
		form = PresenceListForm(date=date, group=group) 
		children = Child.objects.filter(group=group_id).order_by("last_name")
		return render(request, "presence_list.html", {"group": group,
														"children": children,
														"form": form})

	def post(self, request, group_id, date):
		group = Group.objects.get(pk=group_id)
		form = PresenceListForm(request.POST, date=date, group=group)

		if form.is_valid():
			for child in form.get_children(group=group):

				if child.start_hour < datetime.time(7):

					if child.end_hour > datetime.time(12) and child.end_hour <= datetime.time(13):
						six = True
						twelve = True
						thirteen = False
						fourteen = False
						fifteen = False
						sixteen = False

					elif child.end_hour > datetime.time(13) and child.end_hour <= datetime.time(14):
						six = True
						twelve = True
						thirteen = True
						fourteen = False
						fifteen = False
						sixteen = False

					elif child.end_hour > datetime.time(14) and child.end_hour <= datetime.time(15):
						six = True
						fourteen = True
						thirteen = True
						twelve = True
						sixteen = False
						fifteen = False

					elif child.end_hour > datetime.time(15) and child.end_hour <= datetime.time(16):
						six = True
						twelve = True
						thirteen = True
						fourteen = True
						fifteen = True
						sixteen = False

					elif child.end_hour > datetime.time(16) and child.end_hour <= datetime.time(17):
						six = True
						twelve = True
						thirteen = True
						fourteen = True
						fifteen = True
						sixteen = True
				###
				elif child.start_hour > datetime.time(7):

					if child.end_hour > datetime.time(12) and child.end_hour <= datetime.time(13):
						six = False
						twelve = True
						thirteen = False
						fourteen = False
						fifteen = False
						sixteen = False

					elif child.end_hour > datetime.time(13) and child.end_hour <= datetime.time(14):
						six = False
						twelve = True
						thirteen = True
						fourteen = False
						fifteen = False
						sixteen = False
						
					elif child.end_hour > datetime.time(14) and child.end_hour <= datetime.time(15):
						six = False
						twelve = True
						thirteen = True
						fourteen = True
						fifteen = False
						sixteen = False
				
					elif child.end_hour > datetime.time(15) and child.end_hour <= datetime.time(16):
						six = False
						twelve = True
						thirteen = True
						fourteen = True
						fifteen = True
						sixteen = False

					elif child.end_hour > datetime.time(16) and child.end_hour <= datetime.time(17):
						six = False
						twelve = True
						thirteen = True
						fourteen = True
						fifteen = True
						sixteen = True
					
				PresenceList.objects.update_or_create(child=child, day=date, presence_breakfast=child.breakfast,
					presence_brunch=child.brunch, presence_dinner=child.dinner, presence_supper=child.supper, # przenoszę wartości pól dot. posiłków z modelu Child
					presence_six=six, presence_twelve=twelve, presence_thirteen=thirteen, 
					presence_fourteen=fourteen, presence_fifteen=fifteen, presence_sixteen=sixteen,
					defaults = {
					'present': form.cleaned_data.get('child_{}_present'.format(child.id), False),
					})
			return HttpResponseRedirect(reverse('hours_and_meals', kwargs={"date": date, "group_id": group_id}))
		return HttpResponseRedirect('hours_and_meals')
			

class HoursAndMealsView(LoginRequiredMixin, View):

	def get(self, request, group_id, date): 
		group = Group.objects.get(pk=group_id)
		form = HoursAndMealsForm(date=date, group=group)
		children = Child.objects.filter(group=group_id).order_by("last_name")
		return render(request, "hours_and_meals.html", {"group": group,
														"children": children,
														"form": form})


class TeachersView(LoginRequiredMixin, View):

	def get(self, request):
		teachers = Teacher.objects.all().order_by("last_name")
		return render(request, "teachers.html", {"teachers": teachers})


class AddTeacherView(LoginRequiredMixin, View):

	def get(self,request):
		form = AddTeacherForm()
		return render(request, "add_teachers.html", {"form": form})

	def post(self, request):
		form = AddTeacherForm(request.POST)
		if form.is_valid():
			teacher = Teacher.objects.create(first_name=form.cleaned_data['first_name'],
										last_name=form.cleaned_data['last_name'],
										group=form.cleaned_data['group'])
			return HttpResponseRedirect('/group')
		return HttpResponseRedirect('/teachers/add')

