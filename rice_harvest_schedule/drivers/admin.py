#drivers/admin.py
from django.contrib import admin
from .models import *

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('model', 'type', 'price', 'province', 'driver')
    list_filter = ('type', 'province')
    search_fields = ('model', 'driver__username')

admin.site.register(Vehicle, VehicleAdmin)


