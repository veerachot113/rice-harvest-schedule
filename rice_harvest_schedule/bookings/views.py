# bookings/views.py
from drivers.models import Vehicle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking
from .forms import BookingForm
from accounts.models import CustomUser
from accounts.decorators import farmer_required, driver_required
@farmer_required
@login_required(login_url='login')
def create_booking(request, vehicle_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.user_type != 'farmer':
        return redirect('home')

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.farmer = request.user
            booking.vehicle = vehicle
            booking.save()
            return redirect('farmer_booking_list')
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form, 'vehicle': vehicle})

from django.utils.dateparse import parse_datetime

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        appointment_start_date = request.POST.get('appointment_start_date')
        appointment_end_date = request.POST.get('appointment_end_date')
        if appointment_start_date:
            booking.appointment_start_date = parse_datetime(appointment_start_date)
        if appointment_end_date:
            booking.appointment_end_date = parse_datetime(appointment_end_date)
        booking.request_status = "Accepted"
        booking.request_responded_by = request.user.username
        booking.save()
        return redirect('driver_booking_list')

@login_required
def decline_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.request_status = "Declined"
        booking.request_responded_by = request.user.username
        booking.save()
        return redirect('driver_booking_list')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.farmer == request.user and booking.request_status == "Pending":
        booking.delete()
    return redirect('farmer_booking_list')

@login_required
def farmer_booking_list(request):
    bookings = Booking.objects.filter(farmer=request.user)
    return render(request, 'Farmer/booking_famerlist.html', {'bookings': bookings})

@login_required
def driver_booking_list(request):
    no_of_pending_request = count_pending_rent_request(request.user)
    bookings = Booking.objects.filter(vehicle__driver=request.user)
    return render(request, 'Driver/booking_driverlist.html', {'bookings': bookings, 'no_of_pending_request': no_of_pending_request})

def count_pending_rent_request(driver):
    no_of_pending_request = 0
    bookings = Booking.objects.filter(vehicle__driver=driver)
    for booking in bookings:
        if booking.request_status == "Pending":
            no_of_pending_request += 1
    return no_of_pending_request



