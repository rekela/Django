from django.shortcuts import render
from django.views import View
from .models import Group, Child, Parent, Teacher, PresenceList, Meal
from .forms import PresenceDateForm, PresenceListForm, PresenceListFormSet
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


class MainView(View):

	def get(self, request):
		groups = Group.objects.all()
		return render (request, "main_view.html", {"groups": groups})


class GroupListView(View):

	def get(self, request, group_id):
		group = Group.objects.get(pk=group_id)
		teachers = Teacher.objects.filter(group=group_id)
		children = Child.objects.filter(group=group_id).order_by("last_name")
		return render(request, "children_list.html", {"group": group,
														"teachers": teachers,
														"children": children})


class PresenceDateView(View): 

	def get(self, request, group_id):
		form = PresenceDateForm()
		group = Group.objects.get(pk=group_id)
		return render(request, "presence_date.html", {"form": form,
														"group": group})


class PresenceListView(View): 

	def get(self, request, group_id, date):
		group = Group.objects.get(pk=group_id)
		children = Child.objects.filter(group=group_id).order_by("last_name")
		formset = PresenceListFormSet()
		return render(request, "presence_list.html", {"group": group,
														"children": children,
														"formset": formset})


