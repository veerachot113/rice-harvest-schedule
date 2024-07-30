# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from auth_admin.models import DriverDocument
from .forms import UserFarmerRegistrationForm, UserDriverRegistrationForm, UserFarmerUpdateForm, UserDriverUpdateForm,CustomPasswordResetForm, CustomSetPasswordForm
from .models import CustomUser
from drivers.models import Vehicle
from bookings.models import Booking
from .decorators import farmer_required, driver_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drivers.models import HarvestArea
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
def home_driver(request):
    no_of_pending_documents = DriverDocument.objects.filter(request_status="รอดำเนินการ").count()
    no_of_pending_request = count_pending_rent_request(request.user)
    vehicles = Vehicle.objects.all()  # แสดงรถทั้งหมด
    return render(request, 'driver/home_driver.html', {'vehicles': vehicles, 'no_of_pending_request': no_of_pending_request, 'no_of_pending_documents': no_of_pending_documents})


@login_required
def home_farmer(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'Farmer/home_farmer.html', {'vehicles': vehicles})

#ฟังก์การกรอกจังหวัด ประเภทรถ
from datetime import datetime
from collections import defaultdict

def filter(request):
    vehicles = Vehicle.objects.all()
    if request.method == 'POST':
        selected_province = request.POST.get('province_select', None)
        selected_vehicle_types = request.POST.getlist('vehicle_type')
        selected_start_month = request.POST.get('start_month', None)

        if selected_province:
            vehicles = vehicles.filter(province=selected_province)
        if selected_vehicle_types:
            vehicles = vehicles.filter(type__in=selected_vehicle_types)

        # Filter by driver availability
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

    return render(request, 'home.html', {'vehicles': vehicles})



def useregister(request):
    return render(request, 'chooserole.html')

def register_farmer(request):
    if request.method == 'POST':
        form = UserFarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'farmer'
            user.save()
            farmer_group = Group.objects.get(name='farmer')
            user.groups.add(farmer_group)
            user.save()
            
            # subject = 'ยืนยันการลงทะเบียน'
            # message = f'ยินดีต้อนรับ \n\n คุณ{user.first_name} {user.last_name} \n\n ชื่อผู้ใช้ของคุณ: {user.username}!'
            # from_email = 'จองง่ายได้เกี่ยว@rice.com'
            # recipient_list = [user.email]
            
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login')  # เปลี่ยนเป็นหน้าเข้าสู่ระบบหลังจากลงทะเบียนสำเร็จ
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
            driver_group = Group.objects.get(name='driver')
            user.groups.add(driver_group)
            user.save()
            
            # subject = 'ยืนยันการลงทะเบียน'
            # message = f'ยินดีต้อนรับ \n\n คุณ{user.first_name} {user.last_name} \n\n ชื่อผู้ใช้ของคุณ: {user.username}!'
            # from_email = 'จองง่ายได้เกี่ยว@rice.com'
            # recipient_list = [user.email]
            
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login')  # เปลี่ยนเป็นหน้าเข้าสู่ระบบหลังจากลงทะเบียนสำเร็จ
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
                elif 'farmer' in [group.name for group in user.groups.all()]:
                    return redirect('home_farmer')
                elif 'driver' in [group.name for group in user.groups.all()]:
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


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/forgot_password.html'
    email_template_name = 'accounts/forgot_password_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'accounts/reset_password_confirm.html'
    success_url = reverse_lazy('login')

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
    no_of_pending_request = count_pending_rent_request(request.user)
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    form = None
    if 'farmer' in [group.name for group in request.user.groups.all()]:
        if request.method == 'POST':
            form = UserFarmerUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_update')
        else:
            form = UserFarmerUpdateForm(instance=request.user)
        return render(request, 'profile_farmer.html', {'form': form})
    elif 'driver' in [group.name for group in request.user.groups.all()]:
        if request.method == 'POST':
            form = UserDriverUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_update')
        else:
            form = UserDriverUpdateForm(instance=request.user)
        return render(request, 'profile_driver.html', {'form': form, 'no_of_pending_request': no_of_pending_request, 'no_of_pending_documents': no_of_pending_documents})
    
@login_required
def view_driver_profile(request, driver_id):
    no_of_pending_request = count_pending_rent_request(request.user)
    driver = get_object_or_404(CustomUser, id=driver_id, user_type='driver')
    is_vehicle_owner = Vehicle.objects.filter(driver=driver).exists()
    context = {
        'driver': driver,
        'is_vehicle_owner': is_vehicle_owner,
        'no_of_pending_request': no_of_pending_request,
    }
    return render(request, 'driver/driver_profile.html', context)

def count_pending_rent_request(user):
    no_of_pending_request = 0
    if 'driver' in [group.name for group in user.groups.all()]:
        bookings = Booking.objects.filter(vehicle__driver=user)
        for booking in bookings:
            if booking.request_status == "รอดำเนินการ":
                no_of_pending_request += 1
    return no_of_pending_request
