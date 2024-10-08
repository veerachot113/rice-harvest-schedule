# bookings/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('booking/<int:vehicle_id>/', create_booking, name='create_booking'),
    path('accept/<int:booking_id>/', accept_booking, name='accept_booking'),
    path('decline/<int:booking_id>/', decline_booking, name='decline_booking'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('farmer/', farmer_booking_list, name='farmer_booking_list'),
    path('driver/', driver_booking_list, name='driver_booking_list'),
    path('get_districts/', get_districts, name='get_districts'),
    path('get_subdistricts/', get_subdistricts, name='get_subdistricts'),
    path('get_available_dates/', get_available_dates, name='get_available_dates'),
    
]
