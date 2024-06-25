# auth_admin/admin.py

from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import DriverDocument
from accounts.models import CustomUser, Farmer, Driver
from bookings.models import Booking
from drivers.models import CalendarEvent, Vehicle
from django.contrib.auth.models import Group, User

# Custom AdminSite
class MyAdminSite(admin.AdminSite):
    site_header = "Welcome, ADMIN"
    site_title = "Admin Portal"
    index_title = "Admin Dashboard"

    def each_context(self, request):
        context = super().each_context(request)
        context['site_url'] = reverse('document_review')  # Change the site URL here
        return context

# Instantiate the custom AdminSite
admin_site = MyAdminSite(name='myadmin')

# Register your models with the custom AdminSite
admin_site.register(DriverDocument)
admin_site.register(CustomUser)
admin_site.register(Farmer)
admin_site.register(Driver)
admin_site.register(Booking)
admin_site.register(CalendarEvent)
admin_site.register(Vehicle)
admin_site.register(Group)
admin_site.register(User)

# You can register other models here if needed
