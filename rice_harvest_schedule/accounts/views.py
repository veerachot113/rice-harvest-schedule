# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from auth_admin.models import DriverDocument
from .forms import UserFarmerRegistrationForm,CustomPasswordChangeForm, UserDriverRegistrationForm, UserFarmerUpdateForm, UserDriverUpdateForm,CustomPasswordResetForm, CustomSetPasswordForm
from .models import CustomUser
from drivers.models import Vehicle
from bookings.models import Booking
from .decorators import farmer_required, driver_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drivers.models import HarvestArea
from datetime import datetime
from collections import defaultdict

def get_backend(user):
    if user.user_type == 'farmer':
        return 'accounts.backends.UserFarmerBackend'
    elif user.user_type == 'driver':
        return 'accounts.backends.UserDriverBackend'
    else:
        return 'django.contrib.auth.backends.ModelBackend'
    
@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
@driver_required
def home_driver(request): 
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    vehicles = Vehicle.objects.filter(status=True)  
    return render(request, 'driver/home_driver.html', {'vehicles': vehicles, 'no_of_pending_request': no_of_pending_request, 'no_of_pending_documents': no_of_pending_documents})

@login_required
@farmer_required
def home_farmer(request):
    vehicles = Vehicle.objects.filter(status=True)
    return render(request, 'Farmer/home_farmer.html', {'vehicles': vehicles})

def useregister(request):
    return render(request, 'chooserole.html')

def register_farmer(request):
    if request.method == 'POST':
        form = UserFarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'farmer'
            user.save()
            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login')
        else:
            messages.error(request, 'มีข้อผิดพลาดในการสมัครสมาชิก กรุณาตรวจสอบข้อมูลที่กรอก')
    else:
        form = UserFarmerRegistrationForm()
    return render(request, 'farmer/registerfarmer.html', {'form': form})

def register_driver(request):
    if request.method == 'POST':
        form = UserDriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'driver'
            user.save()
            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login') 
        else:
            messages.error(request, 'มีข้อผิดพลาดในการสมัครสมาชิก กรุณาตรวจสอบข้อมูลที่กรอก')
    else:
        form = UserDriverRegistrationForm()
    return render(request, 'driver/registerdriver.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('document_review')
                elif user.user_type == 'farmer':
                    return redirect('home_farmer')
                elif user.user_type == 'driver':
                    return redirect('driver_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง.")
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/registration/login.html', {'form': form})

@login_required
def change_password(request):
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'รหัสผ่านของคุณถูกเปลี่ยนเรียบร้อยแล้ว!')
            return redirect('change_password') 
        else:
            messages.error(request, 'โปรดแก้ไขข้อผิดพลาดที่ปรากฏด้านล่าง.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form ,'no_of_pending_request': no_of_pending_request, 'no_of_pending_documents': no_of_pending_documents})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/forgot_password.html'
    email_template_name = 'accounts/forgot_password_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'accounts/reset_password_confirm.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'รหัสผ่านของคุณถูกเปลี่ยนเรียบร้อยแล้ว! กรุณาเข้าสู่ระบบด้วยรหัสผ่านใหม่.')
        return super().form_valid(form)

    def dispatch(self, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        self.user = self.get_user(uidb64)
        if self.user is None:
            return self.render_to_response(self.get_context_data())
        return super().dispatch(*args, **kwargs)
    
    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return CustomUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return None


@login_required
def profile_update(request):
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    if request.user.user_type == 'farmer':
        if request.method == 'POST':
            form = UserFarmerUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_update')
        else:
            form = UserFarmerUpdateForm(instance=request.user)
        return render(request, 'profile_farmer.html', {'form': form})
    elif request.user.user_type == 'driver':
        if request.method == 'POST':
            form = UserDriverUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_update')
        else:
            form = UserDriverUpdateForm(instance=request.user)
        return render(request, 'profile_driver.html', {
            'form': form, 
            'no_of_pending_request': no_of_pending_request, 
            'no_of_pending_documents': no_of_pending_documents
        })

    
@login_required
def view_driver_profile(request, driver_id):
    driver = get_object_or_404(CustomUser, id=driver_id, user_type='driver')
    is_vehicle_owner = Vehicle.objects.filter(driver=driver).exists()
    context = {
        'driver': driver,
        'is_vehicle_owner': is_vehicle_owner,
    }
    return render(request, 'driver/driver_profile.html', context)


def filter(request):
    vehicles = Vehicle.objects.filter(status=True)
    if request.method == 'POST':
        selected_province = request.POST.get('province_select', None)
        selected_vehicle_types = request.POST.getlist('vehicle_type')
        selected_start_month = request.POST.get('start_month', None)

        if selected_province:
            vehicles = vehicles.filter(province=selected_province)
        if selected_vehicle_types:
            vehicles = vehicles.filter(type__in=selected_vehicle_types)

        if selected_start_month:
            start_date = datetime.strptime(selected_start_month, "%Y-%m").date()
            available_vehicles = []
            driver_month_count = defaultdict(int)

            for vehicle in vehicles:
                harvest_areas = HarvestArea.objects.filter(driver=vehicle.driver)
                for area in harvest_areas:
                    if area.start_date <= start_date <= area.end_date:
                        driver_month_count[vehicle.driver.id] += 1

            if driver_month_count:
                min_month_count = min(driver_month_count.values())
                for vehicle in vehicles:
                    if driver_month_count[vehicle.driver.id] == min_month_count:
                        available_vehicles.append(vehicle)

            vehicles = available_vehicles

    if not vehicles:
        no_vehicles_message = "ไม่มีรถให้บริการในเดือนนี้"
    else:
        no_vehicles_message = None

    return render(request, 'home.html', {'vehicles': vehicles, 'no_vehicles_message': no_vehicles_message})