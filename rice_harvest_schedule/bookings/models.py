# bookings/models.py

from django.db import models
from drivers.models import Vehicle
from accounts.models import CustomUser

class Booking(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='bookings', limit_choices_to={'user_type': 'farmer'})
    driver_id = models.IntegerField(null=True, blank=True) 
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, blank=True)
    fullname = models.CharField(max_length=255)
    address = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ราคา', null=True, blank=True)
    phone = models.CharField(max_length=15)
    details = models.TextField(blank=True, null=True)
    request_status = models.CharField(max_length=30, default="รอดำเนินการ")
    appointment_start_date = models.DateTimeField(null=True, blank=True)
    appointment_end_date = models.DateTimeField(null=True, blank=True)
    province = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')
    subdistrict = models.CharField(max_length=100, default='')

    def save(self, *args, **kwargs):
        if self.vehicle and not self.vehicle_type:
            self.vehicle_type = self.vehicle.type
        super().save(*args, **kwargs)
