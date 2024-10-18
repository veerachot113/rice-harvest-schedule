# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class UserFarmerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username, user_type='farmer')
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id, user_type='farmer')
        except CustomUser.DoesNotExist:
            return None

class UserDriverBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username, user_type='driver')
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id, user_type='driver')
        except CustomUser.DoesNotExist:
            return None

