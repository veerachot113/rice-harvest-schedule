# booking/models.py
from django.utils import timezone  
from django.db import models
from Driver.models import Vehicle
from Accounts.models import *

class Booking(models.Model):
    farmer = models.ForeignKey(UserFarmer, on_delete=models.CASCADE, related_name='bookings', default='')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    address = models.TextField()
    quantity = models.IntegerField()
    phone = models.CharField(max_length=15)
    details = models.TextField()
    request_responded_by = models.CharField(max_length=100, blank=True, null=True)
    request_status = models.CharField(max_length=30, default="Pending")
    appointment_start_date = models.DateTimeField(null=True, blank=True)
    appointment_end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Booking by {self.farmer.username} for {self.vehicle.model}'
