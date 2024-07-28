# bookings/views.py
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
from drivers.models import Vehicle, CalendarEvent, HarvestArea
from drivers.forms import CalendarEventForm


@farmer_required
@login_required
def create_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    existing_events = CalendarEvent.objects.filter(driver=vehicle.driver).values_list('start', 'end')
    event_dates = []
    for start, end in existing_events:
        current_date = start
        while current_date <= end:
            event_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
    
    event_dates_json = json.dumps(event_dates)
    harvest_areas = HarvestArea.objects.filter(driver=vehicle.driver).values('province', 'district', 'subdistrict').distinct()
    unique_provinces = set(area['province'] for area in harvest_areas)  # ดึงจังหวัดที่ไม่ซ้ำกัน

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.farmer = request.user
            booking.vehicle = vehicle
            quantity = form.cleaned_data['quantity']
            
            if quantity < vehicle.min_acres:
                return JsonResponse({'error': f'Minimum acreage requirement not met: {vehicle.min_acres} acres needed.'}, status=400)

            if quantity <= vehicle.max_acres_per_day + 5:
                days_required = 1
            else:
                additional_acres = quantity - (vehicle.max_acres_per_day + 5)
                days_required = math.ceil(additional_acres / vehicle.max_acres_per_day) + 1

            appointment_start_date_str = request.POST.get('appointment_start_date')
            if appointment_start_date_str:
                booking.appointment_start_date = parse_date(appointment_start_date_str)
                booking.appointment_end_date = booking.appointment_start_date + timedelta(days=days_required - 1)
            else:
                return JsonResponse({'error': 'Appointment start date is required.'}, status=400)
            
            # Combine address details
            address = form.cleaned_data['address']
            province = form.cleaned_data['province']
            district = form.cleaned_data['district']
            subdistrict = form.cleaned_data['subdistrict']
            booking.address = f"{address}, จ.{province}, อ.{district}, ต.{subdistrict} "

            booking.save()
            return redirect('farmer_booking_list')
        else:
            print(form.errors)
    else:
        form = BookingForm()
    
    return render(request, 'booking/booking_form.html', {'form': form, 'vehicle': vehicle, 'event_dates': event_dates_json, 'unique_provinces': unique_provinces, 'harvest_areas': harvest_areas})



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import HarvestArea

@login_required
def get_districts(request):
    province = request.GET.get('province')
    districts = HarvestArea.objects.filter(province=province).values_list('district', flat=True).distinct()
    return JsonResponse(list(districts), safe=False)

@login_required
def get_subdistricts(request):
    district = request.GET.get('district')
    subdistricts = HarvestArea.objects.filter(district=district).values_list('subdistrict', flat=True).distinct()
    return JsonResponse(list(subdistricts), safe=False)

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

@login_required
def get_available_dates(request):
    province = request.GET.get('province')
    district = request.GET.get('district')
    subdistrict = request.GET.get('subdistrict')

    areas = HarvestArea.objects.filter(
        province=province,
        district=district
    )

    available_dates = set()
    for area in areas:
        subdistricts = [s.strip() for s in area.subdistrict.split(',')]
        if subdistrict in subdistricts:
            current_date = area.start_date
            end_date = area.end_date
            while current_date <= end_date:
                available_dates.add(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)

    # ดึงกิจกรรมที่มีอยู่ใน CalendarEvent และปิดวันที่ที่มีงานแล้ว
    driver_id = request.GET.get('driver_id')  # รับ driver_id จาก request
    if driver_id:
        existing_events = CalendarEvent.objects.filter(driver_id=driver_id).values_list('start', 'end')
        for start, end in existing_events:
            current_date = start.date()
            end_date = end.date()
            while current_date <= end_date:
                available_dates.discard(current_date.strftime("%Y-%m-%d"))  # ลบวันที่ที่มีงานออกจาก available_dates
                current_date += timedelta(days=1)

    return JsonResponse(list(available_dates), safe=False)



def count_pending_rent_request(driver):
    no_of_pending_request = 0
    bookings = Booking.objects.filter(vehicle__driver=driver)
    for booking in bookings:
        if booking.request_status == "Pending":
            no_of_pending_request += 1
    return no_of_pending_request