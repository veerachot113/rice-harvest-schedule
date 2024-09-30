#drivers/views.py
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
import os
import pickle
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from requests import Request
from google.auth.transport.requests import Request
from django.http import HttpResponseRedirect

def check_is_staff(user):
    return user.is_staff

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'google_api/credentials.json'
TOKEN_FILE = 'google_api/token.pickle'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def check_google_calendar(request):
    creds = get_credentials()
    if isinstance(creds, HttpResponseRedirect):
        return JsonResponse({'connected': False})
    return JsonResponse({'connected': True})

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # ถ้าไม่มี credentials หรือไม่ valid และมี refresh token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
            except Exception as e:
                # ลบไฟล์ token ออกหากการรีเฟรชล้มเหลว
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                # ให้ flow ใหม่เพื่อรับ token ใหม่
                return _start_google_flow()

        else:
            return _start_google_flow()
    
    return creds

def _start_google_flow():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE, 
        scopes=SCOPES, 
        redirect_uri='http://localhost:8000/oauth2callback'
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return HttpResponseRedirect(auth_url)


from django.urls import reverse
from requests import Request
@csrf_exempt
def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/oauth2callback'
    )

    if 'code' not in request.GET:
        auth_url, _ = flow.authorization_url(prompt='consent')
        return redirect(auth_url)
    else:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

        # ตรวจสอบว่ามี pending booking หรือไม่ ถ้ามีให้รีไดเรกต์กลับไปที่การยืนยันการจอง
        if 'pending_booking' in request.session:
            pending_booking = request.session['pending_booking']
            return HttpResponseRedirect(reverse('accept_booking', args=[pending_booking['booking_id']]))
        else:
            return HttpResponseRedirect(reverse('calendar_view'))

    

def create_google_calendar_event(creds, event, calendar_event):
    service = build('calendar', 'v3', credentials=creds)
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    calendar_event.google_event_id = event_result['id']
    calendar_event.save()
    return event_result

def update_google_calendar_event(creds, event_id, event):
    service = build('calendar', 'v3', credentials=creds)
    event_result = service.events().get(calendarId='primary', eventId=event_id).execute()
    
    # Update the event details
    event_result['summary'] = event['summary']
    event_result['description'] = event['description']
    event_result['start'] = event['start']
    event_result['end'] = event['end']
    
    # Update attendees
    event_result['attendees'] = event.get('attendees', [])
    
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event_result).execute()
    return updated_event 

def delete_google_calendar_event(creds, event_id):
    service = build('calendar', 'v3', credentials=creds)
    service.events().delete(calendarId='primary', eventId=event_id).execute()

def get_schedule(request, driver_id):
    driver = get_object_or_404(CustomUser, id=driver_id)
    harvest_areas = HarvestArea.objects.filter(driver=driver)
    return render(request, 'farmer/schedule.html', {'driver': driver, 'harvest_areas': harvest_areas}) 

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def calendar_view(request):
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
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


@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def add_calendar_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        start = datetime.fromisoformat(request.POST.get('start'))
        end = datetime.fromisoformat(request.POST.get('end'))
        farmer_id = request.POST.get('farmer')

        # ตรวจสอบว่ามีการเชื่อมต่อกับ Google Calendar หรือไม่
        creds = get_credentials()
        if isinstance(creds, HttpResponseRedirect):
            return JsonResponse({'status': 'redirect', 'url': creds.url})  # ส่ง URL กลับไปยัง AJAX เพื่อรีไดเรกต์

        if CalendarEvent.objects.filter(driver=request.user, start__lt=end, end__gt=start).exists():
            return JsonResponse({'status': 'error', 'message': 'ช่วงเวลานี้มีงานแล้ว'})

        event = CalendarEvent.objects.create(
            driver=request.user,
            title=title,
            details=details,
            start=start,
            end=end,
            farmer_id=farmer_id
        )

        # สร้าง Google Calendar event
        google_event = {
            'summary': title,
            'description': details,
            'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Bangkok'},
            'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Bangkok'},
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
        if farmer_id:
            farmer = CustomUser.objects.get(id=farmer_id)
            google_event['attendees'] = [{'email': request.user.email}, {'email': farmer.email}]
        else:
            google_event['attendees'] = [{'email': request.user.email}]

        create_google_calendar_event(creds, google_event, event)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

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

        # เช็คการเชื่อมต่อกับ Google Calendar
        creds = get_credentials()
        if isinstance(creds, HttpResponseRedirect):
            return JsonResponse({'status': 'redirect', 'url': creds.url})  # ส่ง URL กลับไปยัง AJAX เพื่อรีไดเรกต์

        # ตรวจสอบหากมีเหตุการณ์ที่ซ้อนทับกัน
        if CalendarEvent.objects.filter(driver=request.user, start__lt=end, end__gt=start).exclude(id=event_id).exists():
            return JsonResponse({'status': 'error', 'message': 'ช่วงเวลานี้มีงานแล้ว'})

        # อัปเดตเหตุการณ์ในฐานข้อมูล
        event.title = title
        event.details = details
        event.start = start
        event.end = end
        event.save()

        # อัปเดตเหตุการณ์ใน Google Calendar
        google_event = {
            'summary': title,
            'description': details,
            'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Bangkok'},
            'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Bangkok'},
            'attendees': [{'email': request.user.email}],
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
        update_google_calendar_event(creds, event.google_event_id, google_event)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def delete_calendar_event(request, event_id):
    if request.method == 'POST':
        # เช็คการเชื่อมต่อกับ Google Calendar
        creds = get_credentials()
        if isinstance(creds, HttpResponseRedirect):
            return JsonResponse({'status': 'redirect', 'url': creds.url})  # ส่ง URL กลับไปยัง AJAX เพื่อรีไดเรกต์

        event = get_object_or_404(CalendarEvent, id=event_id)
        
        # ลบเหตุการณ์จาก Google Calendar
        if event.google_event_id:
            try:
                delete_google_calendar_event(creds, event.google_event_id)
            except Exception as e:
                # ตรวจสอบหากเกิดข้อผิดพลาดกรณีที่เหตุการณ์ถูกลบไปแล้ว
                if "Resource has been deleted" in str(e):
                    print(f"Event {event.google_event_id} already deleted from Google Calendar.")
                else:
                    return JsonResponse({'status': 'error', 'message': 'Failed to delete the event from Google Calendar.'})

        # ลบเหตุการณ์จากฐานข้อมูล
        event.delete()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

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

@login_required
def get_harvest_areas(request):
    harvest_areas = HarvestArea.objects.filter(driver=request.user).values(
        'id', 'start_date', 'end_date', 'province', 'district', 'subdistrict', 'details'
    )
    return JsonResponse(list(harvest_areas), safe=False)


from django.http import JsonResponse

@login_required
def toggle_vehicle_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vehicle_id = data.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id, driver=request.user)

        # สลับสถานะ
        vehicle.status = not vehicle.status
        vehicle.save()

        return JsonResponse({'status': 'success', 'new_status': vehicle.status})

    return JsonResponse({'status': 'error'}, status=400)

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def add_vehicle(request):
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
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
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    driver = request.user
    pending_bookings_count = Booking.objects.filter(vehicle__driver=driver, request_status="รอดำเนินการ").count()
    now = timezone.now()
    current_month_start = now.replace(day=1)
    next_month_start = (current_month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
    current_month_end = next_month_start - timedelta(seconds=1)
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
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()

    event = get_object_or_404(CalendarEvent, id=event_id)
    booking = Booking.objects.filter(
        appointment_start_date=event.start,
        appointment_end_date=event.end,
        farmer_id=event.farmer_id,
        vehicle__driver=request.user
    ).first()
    return render(request, 'booking/booking_detail.html', {'booking': booking, 'event': event, 'no_of_pending_request': no_of_pending_request, 'no_of_pending_documents': no_of_pending_documents})

@login_required
@user_passes_test(check_is_staff, login_url='upload_document', redirect_field_name=None)
def vehicle_detail(request):
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    vehicle = Vehicle.objects.filter(driver=request.user).first()
    if not vehicle:
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
        'form': form,
        'no_of_pending_request':no_of_pending_request,
        'no_of_pending_documents':no_of_pending_documents
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

