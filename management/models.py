from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# GROUP = (
# 		(0, "Grupa 1"),
# 		(1, "Grupa 2"),
# 		(2, "Grupa 3"), 
# 		(3, "Grupa 4")
# 		)


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
	# ilość godzin płatnych do wyliczenia w property - początek do 7, od 12 do end_hour
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


class PresenceList(models.Model):
	day = models.DateField()
	present = models.NullBooleanField(default=False)
	child = models.ForeignKey(Child)
	additional_hour = models.IntegerField(choices=PAID_HOURS, null=True)
    

MEAL_LIST = (
			(0, "śniadanie"),
			(1, "drugie śniadanie"),
			(2, "obiad"),
			(3, "podwieczorek")
		)


class Meal(models.Model):
	name = models.IntegerField(choices=MEAL_LIST)
	price = models.FloatField()
	presence = models.ForeignKey(PresenceList)

