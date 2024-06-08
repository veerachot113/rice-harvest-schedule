# Accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import UserFarmerRegistrationForm, UserDriverRegistrationForm
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group 
from django.contrib.auth.decorators import login_required
from drivers.models import Vehicle
from bookings.models import*
from django.shortcuts import render, get_object_or_404
from .models import UserDriver

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')  

@login_required
def home_driver(request):
    no_of_pending_request = count_pending_rent_request(request.user)
    vehicles = Vehicle.objects.all()
    return render(request, 'Driver/home_driver.html',{'vehicles': vehicles, 'no_of_pending_request': no_of_pending_request})

@login_required
def home_farmer(request):
    vehicles = Vehicle.objects.all()
    return render(request,'Farmer/home_farmer.html',{'vehicles': vehicles})

# def home(request):
#     if request.user.is_authenticated:
#         if request.user.groups.filter(name='farmer').exists():
#             return redirect('home_farmer')
#         elif request.user.groups.filter(name='driver').exists():
#             return redirect('home_driver')
    
#     vehicles = Vehicle.objects.all()
#     return render(request, 'home.html', {'vehicles': vehicles, 'driver_id': request.user.id if request.user.is_authenticated else None})

def home(request):
    vehicles = Vehicle.objects.all()
    if request.method == 'POST':
        selected_province = request.POST.get('province_select', None)
        selected_vehicle_types = request.POST.getlist('vehicle_type')
        if selected_province:
            vehicles = vehicles.filter(province=selected_province)
        if selected_vehicle_types:
            vehicles = vehicles.filter(type__in=selected_vehicle_types)

    return render(request, 'home.html', {'vehicles': vehicles})

def useregister(request):
     return render(request,'chooserole.html') 


def register_farmer(request):
    if request.method == 'POST':
        form = UserFarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Add the user to the 'driver' group
            farmer_group = Group.objects.get(name='farmer')
            user.groups.add(farmer_group)
            user.is_customer = True
            user.save()

            return redirect('login')
    else:
        form = UserFarmerRegistrationForm()

    return render(request, 'Farmer/registerfarmer.html', {'form': form})

def register_driver(request):
    if request.method == 'POST':
        form = UserDriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            driver_group = Group.objects.get(name='driver')
            user.groups.add(driver_group)
            user.is_customer = True
            user.save()

            return redirect('login')
    else:
        form = UserDriverRegistrationForm()

    return render(request, 'Driver/registerdriver.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Additional logging for debugging
                print(f"User {username} logged in with groups: {[group.name for group in user.groups.all()]}")

                # Check all group names
                print(f"All group names: {[group.name for group in Group.objects.all()]}")

                # Check the user's role and redirect accordingly
                if 'farmer' in [group.name for group in user.groups.all()]:
                    return redirect('home_farmer')
                elif 'driver' in [group.name for group in user.groups.all()]:
                    return redirect('home_driver')
                else:
                    return redirect('home')  # Default redirect if not in any group

            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'Accounts/registration/login.html', {'form': form})


@login_required
def profile_update(request):
    no_of_pending_request = count_pending_rent_request(request.user)
    form = None
    if 'farmer' in [group.name for group in request.user.groups.all()]:
        if request.method == 'POST':
            form = UserFarmerUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_update')
        else:
            form = UserFarmerUpdateForm(instance=request.user)
        return render(request, 'profile_farmer.html', {'form': form})  # ปรับเปลี่ยนเพื่อใช้ profile_farmer.html
    elif 'driver' in [group.name for group in request.user.groups.all()]:
        if request.method == 'POST':
            form = UserDriverUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_update')
        else:
            form = UserDriverUpdateForm(instance=request.user)
        return render(request, 'profile_driver.html', {'form': form, 'no_of_pending_request': no_of_pending_request})



def view_driver_profile(request, driver_id):
    no_of_pending_request = count_pending_rent_request(request.user)
    driver = get_object_or_404(UserDriver, id=driver_id)
    
    is_vehicle_owner = False
    if hasattr(driver, 'vehicles'):
        is_vehicle_owner = True

    context = {
        'driver': driver,
        'is_vehicle_owner': is_vehicle_owner,
        'no_of_pending_request': no_of_pending_request,
    }
    return render(request, 'Driver/driver_profile.html', context)


    
def count_pending_rent_request(user):
    no_of_pending_request = 0
    if 'driver' in [group.name for group in user.groups.all()]:
        bookings = Booking.objects.filter(vehicle__driver=user)
        for booking in bookings:
            if booking.request_status == "Pending":
                no_of_pending_request += 1
    return no_of_pending_request
 


