# -*- coding: utf-8 -*-

from django.db import models
from car.models import Car
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

class Booking(models.Model):
	date = models.DateTimeField(auto_now_add=True, auto_now=False, 
                                verbose_name="Date de creation")
	reservation_date = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="Date de réservation")
	car = models.OneToOneField(Car, related_name='car')
	user = models.ForeignKey(User, related_name='user')
	start_address = models.CharField(max_length=250, verbose_name="Adresse de départ")
	dest_address = models.CharField(max_length=250, verbose_name="Adresse de destination")
	state = models.BooleanField()
	duration = models.CharField(max_length=10)

	def __str__(self):
		return str(self.id)

@receiver(post_save, sender=Booking)
def remove_car_disponibility(sender, instance, **kwargs):
	setattr(instance.car, 'disponibility', 0)
	instance.car.save(update_fields=['disponibility'])

@receiver(post_delete, sender=Booking)
def add_car_disponibility(sender, instance, **kwargs):
	setattr(instance.car, 'disponibility', 1)
	instance.car.save(update_fields=['disponibility'])