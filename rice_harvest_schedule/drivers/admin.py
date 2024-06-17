from django.contrib import admin
from .models import Vehicle, CalendarEvent

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('model', 'type', 'price', 'province', 'driver')
    search_fields = ('model', 'type', 'province', 'driver__username')
    list_filter = ('type', 'province')

class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'driver', 'start', 'end')
    search_fields = ('title', 'driver__username')
    list_filter = ('start', 'end')

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CalendarEvent, CalendarEventAdmin)
