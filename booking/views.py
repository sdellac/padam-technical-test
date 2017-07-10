from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .forms import BookingForm, JoinForm
from .models import Booking
from car.models import Car

import googlemaps
from datetime import datetime, timedelta

# Create your views here.

# Utils database functions

def get_booking(id_booking):
	try:
		return Booking.objects.get(id=id_booking)
	except ObjectDoesNotExist:
		return None

def get_bookings(user_request):
	try:
		return Booking.objects.filter(user=user_request)
	except ObjectDoesNotExist:
		return None

# gmaps direction

def get_duration(start_address, dest_address):
	gmaps = googlemaps.Client(key='AIzaSyAP5I-6vKkO3gtAL7PuxLAj7ylS_2cUyB4')
	now = datetime.now()
	try:
		directions_result = gmaps.directions(
			start_address,
			dest_address,
			mode="driving",
			departure_time=now)
		return directions_result[0]['legs'][0]['duration_in_traffic']['text']
	except googlemaps.exceptions.ApiError as inst:
		raise Http404(inst.args[0])

# Views functions

def home(request):
	data = get_bookings(request.user)
	return render(request,'booking/home.html', dict([("bookings", data)]))

def booking(request, bookingID):
	data = get_booking(bookingID)
	if data.user == request.user:
		return render(
			request,
			'booking/booking.html',
			dict([('booking', data)])
		)
	else:
		return HttpResponseForbidden()

class NewBooking(View):
	def get(self, request, *args, **kwargs):
		if not Car.available.count():
			messages.error(request, _("Error : no more car are available"))
			return redirect('/bookings/home')

		form = BookingForm()
		return render(request, 'booking/new.html', {'form' : form})
	def post(self, request, *args, **kwargs):
		form = BookingForm(request.POST)
		if form.is_valid():
			if not Car.available.count():
				messages.error(request, _("Error : no more car are available"))
				return render(request, 'booking/new.html', {'form': form})

			start_address = form.cleaned_data['start_address']
			dest_address = form.cleaned_data['dest_address']
			try:
				duration = get_duration(start_address, dest_address)
			except:
				messages.error(request, _("Error : addresses could be wrong"))
				return render(request, 'booking/new.html', {'form': form})

			booking = Booking.objects.create(user=request.user,
											 reservation_date=datetime.utcnow(),
											 start_address=start_address,
											 dest_address=dest_address,
											 duration=duration,
											 state=True,
											 car=Car.available.first())
			return redirect('/bookings/' + str(booking))
		return render(request, 'booking/new.html', {'form' : form})

def delete(request, bookingID):
	try:
		inst = Booking.objects.get(id=bookingID)
		inst.delete()
	except ObjectDoesNotExist:
		pass
	data = get_bookings(request.user)

	return render(request,'booking/home.html', dict([("bookings", data)]))

def join(request):
	form = JoinForm(request.POST or None)
	if form.is_valid():
		userDjango = User.objects.create(
			username = form.cleaned_data['email'],
			last_name = form.cleaned_data['surname'],
			first_name = form.cleaned_data['firstname'],
			email = form.cleaned_data['email'])

		userDjango.set_password(request.POST['password'])
		userDjango.save()
		return redirect('/bookings/login')

	return render(request, 'booking/join.html', locals())
