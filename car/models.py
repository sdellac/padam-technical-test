from django.db import models

# Create your models here.

class CarManager(models.Manager):
	def get_queryset(self):
		return super(CarManager, self).get_queryset().filter(disponibility = True)

class Car(models.Model):
	disponibility = models.BooleanField()
	objects = models.Manager()
	available = CarManager()

	def __str__(self):
		return str(self.id)