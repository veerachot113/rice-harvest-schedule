#ฺ bookings/admin.py
from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'vehicle','vehicle_type', 'fullname', 'address', 'quantity',"price", 'phone', 'details', 'request_status', 'appointment_start_date', 'appointment_end_date')
    list_filter = ('request_status', 'appointment_start_date', 'appointment_end_date')
    search_fields = ('farmer__username', 'vehicle__model', 'fullname', 'address')

admin.site.register(Booking, BookingAdmin)
