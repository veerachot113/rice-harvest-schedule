#ฺBooking/admin.py

from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','fullname','vehicle','quantity','details', 'address']  # กำหนดฟิลด์ที่ต้องการให้แสดงในรายการ
    search_fields = ['id', 'vehicle__model', 'appointment_date', 'status']  # เพิ่มช่องค้นหา






admin.site.register(Booking, BookingAdmin)
