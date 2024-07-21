# Accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class UserFarmer(AbstractUser):
    groups = models.ManyToManyField(Group, verbose_name="Groups", blank=True, related_name='Accounts_farmer_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name="User Permissions", blank=True, related_name='farmer_users_permissions')
    first_name = models.CharField(max_length=100, default='')  # เพิ่มชื่อ-สกุล
    last_name = models.CharField(max_length=100, default='')  # เพิ่มชื่อ-สกุล
    address = models.CharField(max_length=255, default='')  # เพิ่มที่อยู่
    phone = models.CharField(max_length=15, default='')  # เพิ่มเบอร์โทรศัพท์
    email = models.EmailField(max_length=255, unique=True)  # Keep email field only
    def __str__(self):
        return "farmer"   
 
class UserDriver(AbstractUser):
    groups = models.ManyToManyField(Group, verbose_name="Groups", blank=True, related_name='Accounts_driver_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name="User Permissions", blank=True, related_name='Accounts_driver_user_permissions')
    first_name = models.CharField(max_length=100, default='')  # เพิ่มชื่อ-สกุล
    last_name = models.CharField(max_length=100, default='')  # เพิ่มชื่อ-สกุล
    address = models.CharField(max_length=255, default='')  # เพิ่มที่อยู่
    phone = models.CharField(max_length=15, default='')  # เพิ่มเบอร์โทรศัพท์
    email = models.EmailField(max_length=255, unique=True)  # Keep email field only
    def __str__(self):
        return "driver"
    


