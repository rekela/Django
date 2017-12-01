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


	@property
	def paid_hours(self):
		paid_hours = 0 # zmienna do zliczania płatnych godzin
		start = float(self.start_hour)
		end = float(self.end_hour)
		limit = 12 # zmienna do której przypisuję koniec bezpłatnych godzin (godz.12:00)

		while (limit < end):
			paid_hours += 1
			limit += 1
		if start < 7:
			paid_hours += 0.5
		return paid_hours


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
	presence_breakfast = models.NullBooleanField(default=True)
	presence_brunch = models.NullBooleanField(default=True)
	presence_dinner = models.NullBooleanField(default=True)
	presence_supper = models.NullBooleanField(default=True)
	presence_six = models.NullBooleanField(default=True)
	presence_twelve = models.NullBooleanField(default=True)
	presence_thirteen = models.NullBooleanField(default=True)
	presence_fourteen = models.NullBooleanField(default=True)
	presence_fifteen = models.NullBooleanField(default=True)
	presence_sixteen = models.NullBooleanField(default=True)
	meal_price = models.FloatField(default=0)
	hours_price = models.FloatField(default=0)

	@property
	def breakfast(self):
		return self.presence_breakfast == Child.breakfast

	@property
	def brunch(self):
		return self.presence_brunch == Child.brunch

	@property
	def dinner(self):
		return self.presence_dinner == Child.dinner

	@property
	def supper(self):
		return self.presence_supper == Child.supper

# jeśli nieobecny -> wszytskie posiłki na null + wszytskie godziny dodatkowe na null
# jeśli obecny --> posiłki i godziny dodatkowe przenosza sie z Child + można modyfikować posiłki (wszytskie) i godziny (tylko te spoza zadeklarowanych w umowie)
