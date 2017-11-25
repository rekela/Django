from django.contrib import admin
from .models import (Group, Child, Parent, Teacher, PresenceList)

# Register your models here.


@ admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	pass


@ admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
	pass


@ admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
	pass


@ admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
	pass


@ admin.register(PresenceList)
class PresenceListAdmin(admin.ModelAdmin):
	pass
