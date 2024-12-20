# bookings/views.py
from datetime import timedelta, datetime, time
import json
import math
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils.timezone import make_aware, get_current_timezone
from .models import Booking
from .forms import BookingForm
from accounts.models import CustomUser
from accounts.decorators import farmer_required, driver_required
from django.utils.dateparse import parse_date
from drivers.models import Vehicle, CalendarEvent, HarvestArea
from drivers.forms import CalendarEventForm
from auth_admin.models import DriverDocument
from drivers.views import get_credentials, create_google_calendar_event
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


def check_is_staff(user):
    return user.is_staff

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
    unique_provinces = set(area['province'] for area in harvest_areas)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.farmer = request.user
            booking.vehicle = vehicle
            booking.driver_id = vehicle.driver.id 
            booking.vehicle_type = vehicle.type
            quantity = form.cleaned_data['quantity']

            if quantity < vehicle.min_acres:
                return JsonResponse({'error': f'ไม่เป็นไปตามข้อกำหนดพื้นที่ขั้นต่ำ: {vehicle.min_acres} ต้องการพื้นที่.'}, status=400)

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
                return JsonResponse({'error': 'ต้องระบุวันที่เริ่มต้นการนัดหมาย.'}, status=400)

            address = form.cleaned_data['address']
            province = form.cleaned_data['province']
            district = form.cleaned_data['district']
            subdistrict = form.cleaned_data['subdistrict']
            booking.address = f"{address}, จ.{province}, อ.{district}, ต.{subdistrict} "

            price_per_rai = vehicle.price  
            booking.price = price_per_rai * quantity  

            booking.save()
            return redirect('farmer_booking_list')
        else:
            print(form.errors)
    else:
        form = BookingForm()
    
    return render(request, 'booking/booking_form.html', {
        'form': form,
        'vehicle': vehicle,
        'event_dates': event_dates_json,
        'unique_provinces': unique_provinces,
        'harvest_areas': harvest_areas
    })

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
def decline_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.request_status = "ปฏิเสธ"
        booking.request_responded_by = request.user.username
        booking.save()
        return redirect('driver_booking_list')
    return redirect('driver_booking_list') 


@login_required
def cancel_booking(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found.'})

    if booking.farmer == request.user and booking.request_status == "รอดำเนินการ":
        booking.delete()
        return redirect('farmer_booking_list')

    return JsonResponse({'status': 'error', 'message': 'คุณไม่ได้รับอนุญาตให้ยกเลิกการจองนี้หรือการจองไม่อยู่ในสถานะรอดำเนินการ.'})


# bookings/views.py

@login_required
def farmer_booking_list(request):
    # ดึงข้อมูลการจองทั้งหมดที่ยังคงมีหรือไม่มีค่า vehicle 
    bookings = Booking.objects.filter(farmer=request.user)
    return render(request, 'farmer/booking_farmerlist.html', {'bookings': bookings})



from django.db.models import Q

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def driver_booking_list(request):
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    
    bookings = Booking.objects.filter(Q(vehicle__driver=request.user) | Q(vehicle__isnull=True))

    return render(request, 'driver/booking_driverlist.html', {
        'bookings': bookings,
        'no_of_pending_request': no_of_pending_request,
        'no_of_pending_documents': no_of_pending_documents
    })




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

    driver_id = request.GET.get('driver_id')  
    if driver_id:
        existing_events = CalendarEvent.objects.filter(driver_id=driver_id).values_list('start', 'end')
        for start, end in existing_events:
            current_date = start.date()
            end_date = end.date()
            while current_date <= end_date:
                available_dates.discard(current_date.strftime("%Y-%m-%d")) 
                current_date += timedelta(days=1)

    pending_bookings = Booking.objects.filter(vehicle__driver_id=driver_id, request_status="รอดำเนินการ")
    for booking in pending_bookings:
        current_date = booking.appointment_start_date.date()
        end_date = booking.appointment_end_date.date()
        while current_date <= end_date:
            available_dates.discard(current_date.strftime("%Y-%m-%d"))  
            current_date += timedelta(days=1)

    return JsonResponse(list(available_dates), safe=False)


from drivers.views import update_google_calendar_event  
def create_google_calendar_event(creds, event):
    service = build('calendar', 'v3', credentials=creds)
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result


@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'GET' and 'pending_booking' in request.session:
        pending_booking = request.session.pop('pending_booking')
        title = pending_booking.get('title')
        details = pending_booking.get('details')
        start_time_str = pending_booking.get('start_time_str')
        end_time_str = pending_booking.get('end_time_str')
    elif request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        start_time_str = request.POST.get('appointment_start_time')
        end_time_str = request.POST.get('appointment_end_time')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    if not start_time_str or not end_time_str:
        return JsonResponse({'status': 'error', 'message': 'Start and end times are required.'})

    try:
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid time format.'})

    appointment_date = booking.appointment_start_date.date()

    start_datetime = datetime.combine(appointment_date, start_time)
    end_datetime = datetime.combine(appointment_date, end_time)
    booking.appointment_start_date = start_datetime

    quantity = booking.quantity
    max_acres_per_day = booking.vehicle.max_acres_per_day
    threshold = 5

    if quantity <= max_acres_per_day + threshold:
        days_required = 1
    else:
        additional_acres = quantity - (max_acres_per_day + threshold)
        days_required = math.ceil(additional_acres / max_acres_per_day) + 1

    end_date = appointment_date + timedelta(days=days_required - 1)
    end_datetime = datetime.combine(end_date, end_time)

    booking.appointment_end_date = end_datetime

    creds = get_credentials()
    if isinstance(creds, HttpResponseRedirect):
        request.session['pending_booking'] = {
            'booking_id': booking_id,
            'title': title,
            'details': details,
            'start_time_str': start_time_str,
            'end_time_str': end_time_str,
        }
        return JsonResponse({'status': 'redirect', 'url': creds.url})

    if not creds:
        return JsonResponse({'status': 'error', 'message': 'Failed to connect to Google Calendar. Please try again later.'})

    booking.request_status = "อนุมัติแล้ว"
    booking.save()

    calendar_event = CalendarEvent.objects.filter(driver=request.user, farmer=booking.farmer, start=start_datetime, end=end_datetime).first()
    if calendar_event:
        calendar_event.title = title
        calendar_event.details = details
        calendar_event.save()

        google_event = {
            'summary': title,
            'description': details,
            'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Bangkok'},
            'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Bangkok'},
            'attendees': [{'email': request.user.email}, {'email': booking.farmer.email}],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 1440},  # 1 day = 1440 minutes
                    {'method': 'email', 'minutes': 60},    # 1 hour = 60 minutes
                    {'method': 'popup', 'minutes': 60},    # Popup reminder 1 hour before
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
        update_google_calendar_event(creds, calendar_event.google_event_id, google_event)
    else:
        calendar_event = CalendarEvent.objects.create(
            driver=request.user,
            title=title,
            details=details,
            start=start_datetime,
            end=end_datetime,
            farmer=booking.farmer
        )

        google_event = {
            'summary': title,
            'description': details,
            'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Bangkok'},
            'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Bangkok'},
            'attendees': [{'email': request.user.email}, {'email': booking.farmer.email}],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 1440},  # 1 day = 1440 minutes
                    {'method': 'email', 'minutes': 60},    # 1 hour = 60 minutes
                    {'method': 'popup', 'minutes': 60},    # Popup reminder 1 hour before
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
        event_result = create_google_calendar_event(creds, google_event)
        calendar_event.google_event_id = event_result['id']
        calendar_event.save()

    return HttpResponseRedirect(reverse('calendar_view'))