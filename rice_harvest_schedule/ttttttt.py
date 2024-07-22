# bookings/views
from datetime import timedelta, datetime, time
import json
import math
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware, get_current_timezone
from .models import Booking
from .forms import BookingForm
from accounts.models import CustomUser
from accounts.decorators import farmer_required, driver_required
from django.utils.dateparse import parse_date
from drivers.models import Vehicle, CalendarEvent
from drivers.forms import CalendarEventForm

@farmer_required
@login_required(login_url='login')
def create_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    existing_events = CalendarEvent.objects.filter(driver=vehicle.driver).values_list('start', 'end')
    event_dates = []
    for start, end in existing_events:
        current_date = start
        while current_date <= end:
            event_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
    
    event_dates_json = json.dumps(event_dates)  # Convert to JSON
    
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.farmer = request.user
            booking.vehicle = vehicle
            quantity = form.cleaned_data['quantity']

            if quantity < vehicle.min_acres:
                return JsonResponse({'error': f'Minimum acreage requirement not met: {vehicle.min_acres} acres needed.'}, status=400)

            # Update the calculation logic as per the new requirement
            if quantity <= vehicle.max_acres_per_day + 5:
                days_required = 1
            else:
                additional_acres = quantity - (vehicle.max_acres_per_day + 5)
                days_required = math.ceil(additional_acres / vehicle.max_acres_per_day) + 1

            appointment_start_date_str = request.POST.get('appointment_start_date')
            if appointment_start_date_str:
                booking.appointment_start_date = parse_date(appointment_start_date_str)
                # Properly setting the end date considering the same start day
                booking.appointment_end_date = booking.appointment_start_date + timedelta(days=days_required - 1)
            else:
                return JsonResponse({'error': 'Appointment start date is required.'}, status=400)

            booking.save()
            return redirect('farmer_booking_list')
        else:
            print(form.errors)  # Debugging: Print form errors to the console
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form, 'vehicle': vehicle, 'event_dates': event_dates_json})


@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        start_time_str = request.POST.get('appointment_start_time')
        end_time_str = request.POST.get('appointment_end_time')

        if not start_time_str or not end_time_str:
            return JsonResponse({'status': 'error', 'message': 'Start time and end time are required.'})

        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid time format.'})

        appointment_date = booking.appointment_start_date.date()

        # Combine the date and time into a datetime object without timezone
        start_datetime = datetime.combine(appointment_date, start_time)
        end_datetime = datetime.combine(appointment_date, end_time)
        booking.appointment_start_date = start_datetime

        quantity = booking.quantity
        max_acres_per_day = booking.vehicle.max_acres_per_day
        threshold = 5
        
        # Calculate the number of days required
        if quantity <= max_acres_per_day + threshold:
            days_required = 1
        else:
            additional_acres = quantity - (max_acres_per_day + threshold)
            days_required = math.ceil(additional_acres / max_acres_per_day) + 1

        # Calculate the end date
        end_date = appointment_date + timedelta(days=days_required - 1)
        end_datetime = datetime.combine(end_date, end_time)

        booking.appointment_end_date = end_datetime
        booking.request_status = "Accepted"
        booking.save()

        # Create a calendar event
        CalendarEvent.objects.create(
            driver=request.user,
            title=title,
            details=details,
            start=start_datetime,
            end=end_datetime,
            farmer=booking.farmer
        )

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



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
    return render(request, 'Farmer/booking_farmerlist.html', {'bookings': bookings})

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

<!-- bookinf_forms.html -->
{% extends "base.html" %}
{% load static %}
{% block title %}
Create Booking - Farmer
{% endblock %}
{% block main %}
<div class="container mx-auto p-2" style="margin-top: 6rem;">

    <div class="flex flex-col max-w-7xl mx-auto  bg-white border border-gray-300 rounded-lg shadow-lg" >
        <h1 class="text-4xl text-center mb-8 mt-7">กรอกรายละเอียดการจอง</h1>
        <div class="w-full md:flex">
            <div class="md:w-1/2 p-6">
                <img class="mx-auto md:justify-center object-cover md:w-3/4 h-auto rounded-xl overflow-hidden"
                    src="{{ vehicle.image.url }}" alt="Vehicle">
                <div class="mx-auto md:justify-center object-cover md:w-3/4 h-auto mt-10 rounded-xl overflow-hidden">
                    <div class="mb-3 grid grid-cols-2 mr-24">
                        <label for="driver" class="form-label">ชื่อคนขับ:</label>
                        <span class="col span-1"> {{ vehicle.driver.first_name }} {{ vehicle.driver.last_name }}</span>
                    </div>
                    <div class="mb-3 grid grid-cols-2 mr-24">
                        <label for="type" class="form-label">ประเภทรถ: </label>
                        <span class="col span-1">{{ vehicle.type }}</span>
                    </div>
                    <div class="mb-3 grid grid-cols-2 mr-24">
                        <label for="price" class="form-label">ราคาต่อไร่: </label>
                        <span class="col span-1 ">{{ vehicle.price }} บาท</span>
                    </div>
                    <div class="mb-3 grid grid-cols-2 mr-24">
                        <label for="province" class="form-label">จังหวัด: </label>
                        <span class="col span-1 mr-3">{{ vehicle.province }}</span>
                    </div>
                    <div class="mb-3 grid grid-cols-2 mr-24">
                        <label for="min_acres" class="form-label">ขั้นต่ำที่รับเกี่ยว: </label>
                        <span class="col span-1 mr-3">{{ vehicle.min_acres }} ไร่</span>
                    </div>
                    <div class="mb-3 grid grid-cols-2 mr-24">
                        <label for="max_acres_per_day" class="form-label">จำนวนไร่ที่เกี่ยวได้ต่อวัน: </label>
                        <span class="col span-1 mr-3">{{ vehicle.max_acres_per_day }} ไร่</span>
                    </div>
                </div>
            </div>
            <div class="md:w-1/2 p-4" data-min-acres="{{ vehicle.min_acres }}" data-max-acres-per-day="{{ vehicle.max_acres_per_day }}">
                <form method="post" action="" onsubmit="return validateForm();">
                    {% csrf_token %}
                    <div class="mb-4">
                        <label for="fullname" class="block text-sm font-medium text-gray-700">ชื่อ-สกุล:</label>
                        <input type="text" id="fullname" name="fullname" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-100 focus:border-indigo-500 sm:text-xl">
                    </div>
                    <div class="mb-4">
                        <label for="address" class="block text-sm font-medium text-gray-700">ที่อยู่:</label>
                        <textarea id="address" name="address" rows="4" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
                    </div>
                    <div class="mb-4">
                        <label for="quantity" class="block text-sm font-medium text-gray-700">จำนวนไร่:</label>
                        <input type="number" id="quantity" name="quantity" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-xl">
                        <p id="quantity-warning" class="text-red-500 hidden">จำนวนไร่ที่คุณกรอกไม่ถูกต้องตามที่กำหนด</p>
                    </div>
                    <div class="mb-4">
                        <label for="appointment_start_date" class="block text-sm font-medium text-gray-700">วันเริ่มต้น:</label>
                        <input type="text" id="appointment_start_date" name="appointment_start_date" class="flatpickr mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-xl">
                    </div>
                    <div class="mb-4">
                        <label for="appointment_end_date_display" class="block text-sm font-medium text-gray-700">วันสิ้นสุด:</label>
                        <input type="text" id="appointment_end_date_display" name="appointment_end_date_display" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-xl" disabled>
                        <input type="hidden" id="appointment_end_date" name="appointment_end_date">
                    </div>
                    <div class="mb-4">
                        <label for="phone" class="block text-sm font-medium text-gray-700">เบอร์ติดต่อ:</label>
                        <input type="text" id="phone" name="phone" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-xl">
                    </div>
                    <div class="mb-4">
                        <label for="details" class="block text-sm font-medium text-gray-700">รายละเอียด (ไม่จำเป็น):</label>
                        <textarea id="details" name="details" rows="4" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
                    </div>
                    <button type="submit" id="submit-button" class="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">เพิ่ม</button>
                </form>
            </div>
        </div>
    </div>
</div>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="https://npmcdn.com/flatpickr/dist/l10n/th.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {
    // const eventDates = JSON.parse('{{ event_dates|escapejs }}');
    const eventDates = {{ event_dates|safe }};
    flatpickr(".flatpickr", {
        enableTime: false,
        dateFormat: "Y-m-d",
        locale: "th",
        disable: eventDates
    });

    const quantityInput = document.getElementById('quantity');
    const startDateInput = document.getElementById('appointment_start_date');
    const endDateDisplay = document.getElementById('appointment_end_date_display');
    const endDateInput = document.getElementById('appointment_end_date');
    const submitButton = document.getElementById('submit-button');
    const quantityWarning = document.getElementById('quantity-warning');
    const maxAcresPerDay = parseInt(document.querySelector('[data-max-acres-per-day]').getAttribute('data-max-acres-per-day'), 10);
    const minAcres = parseInt(document.querySelector('[data-min-acres]').getAttribute('data-min-acres'), 10);
    const threshold = 5;

    function formatDateToDDMMYYYY(date) {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}/${month}/${year}`;
    }

    function calculateEndDate() {
        const quantity = parseInt(quantityInput.value, 10);
        const startDate = new Date(startDateInput.value);

        if (!isNaN(quantity) && startDate instanceof Date && !isNaN(startDate.getTime())) {
            let daysRequired = 0;
            if (quantity <= maxAcresPerDay + threshold) {
                daysRequired = 1;
            } else {
                daysRequired = Math.ceil((quantity - threshold) / maxAcresPerDay);
            }

            const endDate = new Date(startDate);
            endDate.setDate(endDate.getDate() + daysRequired - 1);

            const formattedEndDate = formatDateToDDMMYYYY(endDate);
            endDateDisplay.value = formattedEndDate;
            endDateInput.value = endDate.toISOString().slice(0, 10);
        } else {
            endDateDisplay.value = '';
            endDateInput.value = '';
        }
    }

    function validateQuantity() {
        const quantity = parseInt(quantityInput.value, 10);
        if (quantity < minAcres) {
            quantityWarning.classList.remove('hidden');
            submitButton.disabled = true;
        } else {
            quantityWarning.classList.add('hidden');
            submitButton.disabled = false;
        }
    }

    quantityInput.addEventListener('input', function () {
        calculateEndDate();
        validateQuantity();
    });
    startDateInput.addEventListener('input', calculateEndDate);

    // Add form validation before submission
    window.validateForm = function() {
        const quantity = parseInt(quantityInput.value, 10);
        if (quantity < minAcres) {
            quantityWarning.classList.remove('hidden');
            return false;  // Prevent form submission
        }
        return true;  // Allow form submission
    };
});

</script>

{% endblock %}