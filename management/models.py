from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
	name = models.CharField(max_length=32)

	def __str__(self):
		return self.name


class Child(models.Model):
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	kdr = models.NullBooleanField(default=False)
	start_hour = models.TimeField()
	end_hour = models.TimeField()
	breakfast = models.NullBooleanField(default=True)
	brunch = models.NullBooleanField(default=True)
	dinner = models.NullBooleanField(default=True)
	supper = models.NullBooleanField(default=True)
	group = models.ForeignKey(Group)


	@property
	def name(self):
		return "{} {}".format(self.first_name, self.last_name)


	def __str__(self):
		return self.name


class Parent(models.Model):
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	phone_number = models.CharField(max_length=16)
	email = models.EmailField()
	child = models.ManyToManyField(Child)

	@property
	def name(self):
		return "{} {}".format(self.first_name, self.last_name)

	def __str__(self):
		return self.name
		

class Teacher(models.Model):
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	group = models.ForeignKey(Group) 

	@property
	def name(self):
		return "{} {}".format(self.first_name, self.last_name)

	def __str__(self):
		return self.name
	

PAID_HOURS = (
		(0, "6:30"),
		(1, "12:00"),
		(2, "13:00"),
		(3, "14:00"),
		(4, "15:00"),
		(5, "16:00")
		)

MEAL_LIST = (
		(0, "śniadanie"),
		(1, "drugie śniadanie"),
		(2, "obiad"),
		(3, "podwieczorek")
		)


class PresenceList(models.Model):
	day = models.DateField()
	present = models.NullBooleanField(default=False)
	child = models.ForeignKey(Child)
	additional_hour = models.IntegerField(choices=PAID_HOURS, null=True)
	meal = models.IntegerField(choices=MEAL_LIST, null=True)
	presence_breakfast = models.NullBooleanField(null=True)
	presence_brunch = models.NullBooleanField(null=True)
	presence_dinner = models.NullBooleanField(null=True)
	presence_supper = models.NullBooleanField(null=True)
	presence_six = models.NullBooleanField(null=True)
	presence_twelve = models.NullBooleanField(null=True)
	presence_thirteen = models.NullBooleanField(null=True)
	presence_fourteen = models.NullBooleanField(null=True)
	presence_fifteen = models.NullBooleanField(null=True)
	presence_sixteen = models.NullBooleanField(null=True)
	meal_price = models.FloatField(default=0)
	hours_price = models.FloatField(default=0)

