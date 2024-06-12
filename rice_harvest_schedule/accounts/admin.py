# accounts/admin.py
from django.contrib import admin
from .models import CustomUser, Farmer, Driver

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class FarmerAdmin(CustomUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_type='farmer')

class DriverAdmin(CustomUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_type='driver')
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Driver, DriverAdmin)
