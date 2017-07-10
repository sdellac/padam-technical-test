from django.db import models

# Create your models here.

class CarAvailableManager(models.Manager):
	def get_queryset(self):
		return super(CarAvailableManager, self).get_queryset().filter(disponibility = True)

class Car(models.Model):
	disponibility = models.BooleanField()
	objects = models.Manager()
	available = CarAvailableManager()

	def __str__(self):
		return str(self.id)