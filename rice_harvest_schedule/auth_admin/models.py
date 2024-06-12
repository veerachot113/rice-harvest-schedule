# auth_admin/models.py
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

class DriverDocument(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    id_card = models.ImageField(upload_to='documents/id_card/')
    car_registration = models.ImageField(upload_to='documents/car_registration/')
    driver_with_car = models.ImageField(upload_to='documents/driver_with_car/')
    note = models.TextField(blank=True, null=True)
    request_status = models.CharField(max_length=30, default="Pending")
    

    def __str__(self):
        return f'{self.driver.username} - {self.request_status}'
