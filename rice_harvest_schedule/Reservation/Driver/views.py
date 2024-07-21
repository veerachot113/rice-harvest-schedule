#Driver/views.py
import json
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from Accounts.models import *
from Booking.models import *
from django.shortcuts import render, redirect, get_object_or_404


#เพิ่มรถ
@login_required
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

@login_required
def add_detailvehicle(request, id=None):
    if id is not None:
        try:
            vehicle = Vehicle.objects.get(pk=id)
        except Vehicle.DoesNotExist:
            return redirect('home_driver')

        if request.method == 'POST':
            form = DetailvehicleForm(request.POST)
            if form.is_valid():
                detail_vehicle = form.save(commit=False)
                detail_vehicle.vehicle = vehicle
                detail_vehicle.save()
                return redirect('home_driver')
        else:
            form = DetailvehicleForm()
        return render(request, 'Driver/add_detailvehicle.html', {'form': form, 'vehicle': vehicle})



from django.shortcuts import render
from .models import CalendarEvent
from Accounts.models import UserDriver

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CalendarEvent

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CalendarEvent
from Accounts.models import UserDriver

@login_required
@require_POST
def add_event(request):
    data = json.loads(request.body)
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')

    if title and start and end:
        event = CalendarEvent.objects.create(
            title=title,
            start=start,
            end=end,
            driver=request.user.userdriver
        )
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Missing data'})
def calendar_events(request):
    user = request.user
    driver = None
    if hasattr(user, 'userdriver'):
        driver = user.userdriver

    if driver:
        events = CalendarEvent.objects.filter(driver=driver)
        data = []
        for event in events:
            data.append({
                'id': event.id,
                'title': event.title,
                'start': event.start.isoformat(),
                'end': event.end.isoformat(),
            })
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)  # Return empty array if no driver found
    




    # Driver/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LicenseDocument
from .forms import LicenseDocumentForm

@login_required
def submit_document(request):
    if request.method == 'POST':
        form = LicenseDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            license_document = form.save(commit=False)
            license_document.driver = request.user
            license_document.save()
            return redirect('document_status')
    else:
        form = LicenseDocumentForm()
    return render(request, 'Driver/submit_document.html', {'form': form})

@login_required
def document_status(request):
    documents = LicenseDocument.objects.filter(driver=request.user)
    return render(request, 'Driver/document_status.html', {'documents': documents})

from django.shortcuts import render, redirect
from .forms import LicenseDocumentForm
def upload_document(request):
    if request.method == 'POST':
        form = LicenseDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            driver = request.user  # หากคุณมั่นใจว่า request.user จะเป็น UserDriver
            if LicenseDocument.objects.filter(driver=driver, is_approved=False).exists():
                # ถ้ามีเอกสารที่ยังไม่ได้รับการอนุมัติอยู่ ก็ไม่สามารถส่งเอกสารใหม่ได้
                form.add_error(None, "You have already submitted a document for approval.")
            else:
                form.instance.driver = driver
                form.save()
                return redirect('home_driver')
    else:
        form = LicenseDocumentForm()
    return render(request, 'Driver/upload_document.html', {'form': form})