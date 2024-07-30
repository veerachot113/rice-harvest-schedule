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
from django.utils import timezone
from drivers.models import CalendarEvent
from datetime import datetime, timedelta
from auth_admin.models import DriverDocument
import json

def check_is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def add_vehicle(request):
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
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
            return redirect('add_vehicle')
    else:
        if existing_vehicle:
            form = VehicleForm(instance=existing_vehicle)
        else:
            form = VehicleForm()
    
    return render(request, 'Driver/add_vehicle.html', {
        'form': form,
        'existing_vehicle': existing_vehicle,
        'no_of_pending_request': no_of_pending_request,
        'no_of_pending_documents': no_of_pending_documents
    })

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, driver=request.user)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('add_vehicle')
    return redirect('add_vehicle')

def count_pending_rent_request(driver):
    no_of_pending_request = 0
    bookings = Booking.objects.filter(vehicle__driver=driver)
    for booking in bookings:
        if booking.request_status == "รอดำเนินการ":
            no_of_pending_request += 1
    return no_of_pending_request


def get_schedule(request, driver_id):
    driver = get_object_or_404(CustomUser, id=driver_id)
    harvest_areas = HarvestArea.objects.filter(driver=driver)
    return render(request, 'farmer/schedule.html', {'driver': driver, 'harvest_areas': harvest_areas}) 



@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def calendar_view(request):
    no_of_pending_documents = DriverDocument.objects.filter(request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(request_status="รอดำเนินการ").count()
    harvest_areas = HarvestArea.objects.filter(driver=request.user)
    return render(request, 'driver/calendar.html', {'harvest_areas': harvest_areas,'no_of_pending_request': no_of_pending_request ,'no_of_pending_documents': no_of_pending_documents})

def get_calendar_events(request):
    Booking.objects.filter(request_status="รอดำเนินการ").count()

    driver_id = request.GET.get('driver_id', request.user.id)
    events = CalendarEvent.objects.filter(driver_id=driver_id).values('id', 'title', 'details', 'start', 'end', 'farmer_id', 'driver_id')
    events_list = []
    for event in events:
        events_list.append({
            'id': event['id'],
            'title': event['title'],
            'start': event['start'].isoformat(),
            'end': event['end'].isoformat(),
            'details': event['details'],
            'farmer_id': event['farmer_id'],
            'driver_id': event['driver_id'],
        })
    return JsonResponse(events_list, safe=False)


@csrf_exempt
@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
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

@csrf_exempt
@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
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

        # อัพเดทการจองที่เกี่ยวข้อง (ถ้ามี)
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

@csrf_exempt
@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def update_booking_dates(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CalendarEvent, id=event_id)
        start = parse_datetime(request.POST.get('start'))
        end = parse_datetime(request.POST.get('end'))

        # Update event dates
        event.start = start
        event.end = end
        event.save()

        # Update the related booking dates (if exists)
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
            return JsonResponse({'status': 'success'})  # Even if no matching booking, return success
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def delete_calendar_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CalendarEvent, id=event_id)
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
def get_harvest_areas(request):
    harvest_areas = HarvestArea.objects.filter(driver=request.user).values(
        'id', 'start_date', 'end_date', 'province', 'district', 'subdistrict', 'details'
    )
    return JsonResponse(list(harvest_areas), safe=False)
@csrf_exempt
@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def add_harvest_area(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        province = data.get('province')
        district = data.get('district')
        subdistrict = data.get('subdistrict')
        details = data.get('details')

        # Check for overlapping dates
        overlapping_areas = HarvestArea.objects.filter(
            driver=request.user,
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        if overlapping_areas.exists():
            return JsonResponse({'status': 'error', 'message': 'ช่วงเวลานี้มีพื้นที่ลงเก็บเกี่ยวแล้ว'})

        harvest_area = HarvestArea.objects.create(
            driver=request.user,
            start_date=start_date,
            end_date=end_date,
            province=province,
            district=district,
            subdistrict=subdistrict,
            details=details
        )

        return JsonResponse({'status': 'success', 'id': harvest_area.id})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def update_harvest_area(request, area_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        province = data.get('province')
        district = data.get('district')
        subdistrict = data.get('subdistrict')
        details = data.get('details')

        harvest_area = get_object_or_404(HarvestArea, id=area_id, driver=request.user)
        
        overlapping_areas = HarvestArea.objects.filter(
            driver=request.user,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exclude(id=area_id)
        if overlapping_areas.exists():
            return JsonResponse({'status': 'error', 'message': 'ช่วงเวลานี้มีพื้นที่ลงเก็บเกี่ยวแล้ว'})

        harvest_area.start_date = start_date
        harvest_area.end_date = end_date
        harvest_area.province = province
        harvest_area.district = district
        harvest_area.subdistrict = subdistrict
        harvest_area.details = details
        harvest_area.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
@login_required
def delete_harvest_area(request, area_id):
    if request.method == 'POST':
        harvest_area = get_object_or_404(HarvestArea, id=area_id, driver=request.user)
        harvest_area.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def driver_dashboard(request):
    no_of_pending_documents = DriverDocument.objects.filter(request_status="รอดำเนินการ").count()
    no_of_pending_request = count_pending_rent_request(request.user)
    driver = request.user

    # Count pending booking requests
    pending_bookings_count = Booking.objects.filter(vehicle__driver=driver, request_status="รอดำเนินการ").count()

    # Get current date and time
    now = timezone.now()

    # Get current month start and end dates
    current_month_start = now.replace(day=1)
    next_month_start = (current_month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
    current_month_end = next_month_start - timedelta(seconds=1)

    # Count events in the current month and that are not past
    events = CalendarEvent.objects.filter(driver=driver, start__gte=current_month_start, end__lte=current_month_end, end__gt=now)
    events_count = events.count()

    context = {
        'pending_bookings_count': pending_bookings_count,
        'events_count': events_count,
        'events': events, 
        'no_of_pending_request': no_of_pending_request ,
        'no_of_pending_documents': no_of_pending_documents}

    return render(request, 'driver/dashboard.html', context)

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def booking_detail(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id)
    try:
        booking = Booking.objects.get(
            appointment_start_date=event.start,
            appointment_end_date=event.end,
            farmer_id=event.farmer_id,
            vehicle__driver=request.user
        )
        return render(request, 'booking/booking_detail.html', {'booking': booking, 'event': event})
    except Booking.DoesNotExist:
        return render(request, 'booking/booking_detail.html', {'event': event})
    

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def vehicle_detail(request):
    vehicle = Vehicle.objects.filter(driver=request.user).first()
    if not vehicle:
        # ถ้าไม่มีรถที่เกี่ยวข้องกับผู้ใช้ ให้รีไดเรกต์ไปที่หน้าสำหรับเพิ่มรถ
        return redirect('add_vehicle')

    try:
        detail = VehicleDetail.objects.get(vehicle=vehicle)
    except VehicleDetail.DoesNotExist:
        detail = None

    try:
        harvest_area = HarvestArea.objects.filter(driver=request.user)
    except HarvestArea.DoesNotExist:
        harvest_area = None

    if request.method == 'POST':
        if detail:
            form = VehicleDetailForm(request.POST, request.FILES, instance=detail)
        else:
            form = VehicleDetailForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_detail = form.save(commit=False)
            new_detail.vehicle = vehicle
            new_detail.save()
            return redirect('vehicle_detail')
    else:
        if detail:
            form = VehicleDetailForm(instance=detail)
        else:
            form = VehicleDetailForm()

    return render(request, 'driver/add_vehicle_detail.html', {
        'vehicle': vehicle,
        'detail': detail,
        'harvest_areas': harvest_area,
        'form': form
    })


@login_required
def view_vehicle_detail(request, driver_id):
    vehicle = get_object_or_404(Vehicle, driver_id=driver_id)
    try:
        detail = VehicleDetail.objects.get(vehicle=vehicle)
    except VehicleDetail.DoesNotExist:
        detail = None

    harvest_areas = HarvestArea.objects.filter(driver_id=driver_id)

    return render(request, 'farmer/view_vehicle_detail.html', {
        'vehicle': vehicle,
        'detail': detail,
        'harvest_areas': harvest_areas
    })