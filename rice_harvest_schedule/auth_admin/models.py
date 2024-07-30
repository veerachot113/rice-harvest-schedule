# auth_admin/models.py
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class DriverDocument(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_card = models.ImageField(upload_to='documents/id_card/')
    car_registration = models.ImageField(upload_to='documents/car_registration/')
    driver_with_car = models.ImageField(upload_to='documents/driver_with_car/')
    submission_date = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(max_length=30, default="รอดำเนินการ")
    note = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(null=True, blank=True)  # เพิ่มฟิลด์นี้เพื่อบันทึกวันและเวลาตอบกลับ

    def __str__(self):
        return self.driver.username
