# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('farmer', 'Farmer'),
        ('driver', 'Driver'),
    )
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set', blank=True)
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES, default='farmer')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Farmer(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Farmer'
        verbose_name_plural = 'Farmers'

class Driver(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'