# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('farmer', 'Farmer'),
        ('driver', 'Driver'),
    )
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES, default='')  # กำหนดบทบาท (farmer หรือ driver)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username
