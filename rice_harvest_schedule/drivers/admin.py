from django.contrib import admin
from .models import Vehicle, CalendarEvent, HarvestArea, VehicleDetail

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('model', 'type', 'price', 'province', 'driver')
    search_fields = ('model', 'type', 'province', 'driver__username')
    list_filter = ('type', 'province')

class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'driver', 'start', 'end')
    search_fields = ('title', 'driver__username')
    list_filter = ('start', 'end')

class HarvestAreaAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'province', 'district', 'subdistrict', 'driver')
    list_filter = ('province', 'district', 'subdistrict')
    search_fields = ('province', 'district', 'subdistrict', 'details')

class VehicleDetailAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'power', 'details')
    search_fields = ('vehicle__model', 'power', 'details')
    list_filter = ('vehicle__model', 'vehicle__type')

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CalendarEvent, CalendarEventAdmin)
admin.site.register(HarvestArea, HarvestAreaAdmin)
admin.site.register(VehicleDetail, VehicleDetailAdmin)
