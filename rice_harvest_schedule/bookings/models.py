# bookings/models.py
from django.db import models
from drivers.models import Vehicle, HarvestArea
from accounts.models import CustomUser

class Booking(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings', limit_choices_to={'user_type': 'farmer'})
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    address = models.TextField()
    quantity = models.IntegerField()
    phone = models.CharField(max_length=15)
    details = models.TextField(blank=True, null=True)
    request_status = models.CharField(max_length=30, default="รอดำเนินการ")
    appointment_start_date = models.DateTimeField(null=True, blank=True)
    appointment_end_date = models.DateTimeField(null=True, blank=True)
    province = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')
    subdistrict = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'Booking by {self.farmer.username} for {self.vehicle.model}'
