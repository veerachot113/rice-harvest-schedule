#drivers/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *
from accounts.models import *
from bookings.models import Booking
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from datetime import datetime

def check_is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def add_vehicle(request):
    no_of_pending_request = count_pending_rent_request(request.user)
    existing_vehicle = Vehicle.objects.filter(driver=request.user).first()
    if request.method == 'POST':
        if existing_vehicle:
            form = VehicleForm(request.POST, request.FILES, instance=existing_vehicle)
        else:
            form = VehicleForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.instance.driver = request.user
            form.save()
            return redirect('home_driver')
    else:
        if existing_vehicle:
            form = VehicleForm(instance=existing_vehicle)
        else:
            form = VehicleForm()
    
    return render(request, 'Driver/add_vehicle.html', {
        'form': form,
        'existing_vehicle': existing_vehicle,
        'no_of_pending_request': no_of_pending_request
    })

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, driver=request.user)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('home_driver')
    return render(request, 'Driver/confirm_delete.html', {'vehicle': vehicle})


def count_pending_rent_request(driver):
    no_of_pending_request = 0
    bookings = Booking.objects.filter(vehicle__driver=driver)
    for booking in bookings:
        if booking.request_status == "Pending":
            no_of_pending_request += 1
    return no_of_pending_request

@login_required(login_url='login')
def driver_schedule(request, driver_id):
    driver = get_object_or_404(CustomUser, id=driver_id)
    return render(request, 'Driver/driver_schedule.html', {'driver': driver})

@login_required
def get_calendar_events_for_farmer(request):
    farmer_id = request.GET.get('farmer_id', request.user.id)
    events = CalendarEvent.objects.filter(farmer_id=farmer_id).values('id', 'title', 'details', 'start', 'end', 'farmer_id')
    events_list = []
    for event in events:
        events_list.append({
            'id': event['id'],
            'title': event['title'],
            'start': event['start'].isoformat(),  # ส่งค่า start ในรูปแบบ ISO string
            'end': event['end'].isoformat(),      # ส่งค่า end ในรูปแบบ ISO string
            'details': event['details'],
            'farmer_id': event['farmer_id'],      # เพิ่ม farmer_id เพื่อใช้ในการกำหนดสี
        })
    return JsonResponse(events_list, safe=False)

@login_required
def calendar_view(request):
    return render(request, 'Driver/calendar.html')

@login_required
def get_calendar_events(request):
    driver_id = request.GET.get('driver_id', request.user.id)
    events = CalendarEvent.objects.filter(driver_id=driver_id).values('id', 'title', 'details', 'start', 'end', 'farmer_id')
    events_list = []
    for event in events:
        events_list.append({
            'id': event['id'],
            'title': event['title'],
            'start': event['start'].isoformat(),  # ส่งค่า start ในรูปแบบ ISO string
            'end': event['end'].isoformat(),      # ส่งค่า end ในรูปแบบ ISO string
            'details': event['details'],
            'farmer_id': event['farmer_id'],      # เพิ่ม farmer_id เพื่อใช้ในการกำหนดสี
        })
    return JsonResponse(events_list, safe=False)


@csrf_exempt
@login_required
def add_calendar_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        start = datetime.fromisoformat(request.POST.get('start'))
        end = datetime.fromisoformat(request.POST.get('end'))
        farmer_id = request.POST.get('farmer')

        if CalendarEvent.objects.filter(driver=request.user, start__lt=end, end__gt=start).exists():
            return JsonResponse({'status': 'error', 'message': 'ช่วงเวลานี้มีงานแล้ว'})

        CalendarEvent.objects.create(
            driver=request.user,
            title=title,
            details=details,
            start=start,
            end=end,
            farmer_id=farmer_id
        )
        return JsonResponse({'status': 'success'})

from django.utils.dateparse import parse_datetime

@csrf_exempt
@login_required
def edit_calendar_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CalendarEvent, id=event_id)
        title = request.POST.get('title')
        details = request.POST.get('details')
        start = parse_datetime(request.POST.get('start'))
        end = parse_datetime(request.POST.get('end'))

        if CalendarEvent.objects.filter(driver=request.user, start__lt=end, end__gt=start).exclude(id=event_id).exists():
            return JsonResponse({'status': 'error', 'message': 'ช่วงเวลานี้มีงานแล้ว'})

        event.title = title
        event.details = details
        event.start = start
        event.end = end
        event.save()

        # อัพเดทการจองที่เกี่ยวข้อง
        booking = Booking.objects.filter(
            vehicle__driver=request.user,
            appointment_start_date__lte=event.start,
            appointment_end_date__gte=event.end,
            farmer=event.farmer
        ).first()
        if booking:
            booking.appointment_start_date = event.start
            booking.appointment_end_date = event.end
            booking.save()

        return JsonResponse({'status': 'success'})
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def update_booking_dates(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CalendarEvent, id=event_id)
        start = parse_datetime(request.POST.get('start'))
        end = parse_datetime(request.POST.get('end'))

        # Update event dates
        event.start = start
        event.end = end
        event.save()

        # Update the related booking dates
        booking = Booking.objects.filter(
            vehicle__driver=request.user,
            farmer=event.farmer
        ).first()

        if booking:
            booking.appointment_start_date = start
            booking.appointment_end_date = end
            booking.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No matching booking found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def delete_calendar_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CalendarEvent, id=event_id)
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


