from django.shortcuts import render, redirect
from django.views import View
from .models import Group, Child, Parent, Teacher, PresenceList
from .forms import LoginForm, PresenceDateForm, ChildForm, AddChildForm, PresenceListForm 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.


class MainView(View):

	def get(self, request):
		form = LoginForm()
		return render(request, "main_view.html", {"form": form})

	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data['login']
			return HttpResponseRedirect('/group')


class GroupView(View):

	def get(self, request):
		groups = Group.objects.all()
		return render (request, "group_view.html", {"groups": groups})


class GroupListView(View):

	def get(self, request, group_id):
		group = Group.objects.get(pk=group_id)
		teachers = Teacher.objects.filter(group=group_id)
		children = Child.objects.filter(group=group_id).order_by("last_name")
		return render(request, "children_list.html", {"group": group,
														"teachers": teachers,
														"children": children})


class ChildView(View):

	def get(self, request, group_id, child_id):
		group = Group.objects.get(pk=group_id)
		child = Child.objects.get(pk=child_id)
		form = AddChildForm(instance=child)
		return render(request, "child.html", {"form": form})

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


class AddChildView(View):

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


class PresenceDateView(View): 

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


class PresenceListView(View): 

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
				PresenceList.objects.update_or_create(child=child, day=date, 
					defaults = {
					'present': form.cleaned_data.get('child_{}_present'.format(child.id), False)
					})
			return HttpResponseRedirect('/group') 
