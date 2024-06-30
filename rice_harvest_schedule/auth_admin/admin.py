# auth_admin/admin.py

# from django.contrib import admin
# from django.urls import path
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from .models import DriverDocument
# from accounts.models import CustomUser, Farmer, Driver
# from bookings.models import Booking
# from drivers.models import CalendarEvent, Vehicle
# from django.contrib.auth.models import Group, User

# # Custom AdminSite
# class MyAdminSite(admin.AdminSite):
#     site_header = "Welcome, ADMIN"
#     site_title = "Admin Portal"
#     index_title = "Admin Dashboard"

#     def each_context(self, request):
#         context = super().each_context(request)
#         context['site_url'] = reverse('document_review')  # Change the site URL here
#         return context

# # Instantiate the custom AdminSite
# admin_site = MyAdminSite(name='myadmin')

# # Register your models with the custom AdminSite
# admin_site.register(DriverDocument)
# admin_site.register(CustomUser)
# admin_site.register(Farmer)
# admin_site.register(Driver)
# admin_site.register(Booking)
# admin_site.register(CalendarEvent)
# admin_site.register(Vehicle)
# admin_site.register(Group)
# admin_site.register(User)


# auth_admin/admin.py
from django.contrib import admin
from .models import DriverDocument

class DriverDocumentAdmin(admin.ModelAdmin):
    list_display = ('driver', 'submission_date', 'request_status')
    search_fields = ('driver__username', 'request_status')
    list_filter = ('request_status', 'submission_date')
    readonly_fields = ('submission_date',)
    fieldsets = (
        (None, {
            'fields': ('driver', 'submission_date', 'id_card', 'car_registration', 'driver_with_car', 'note', 'request_status')
        }),
    )

admin.site.register(DriverDocument, DriverDocumentAdmin)

# You can register other models here if needed
