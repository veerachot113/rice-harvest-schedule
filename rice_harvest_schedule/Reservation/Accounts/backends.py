# Accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import UserFarmer, UserDriver


class UserFarmerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserFarmer.objects.get(username=username)
        except UserFarmer.DoesNotExist:
            return None

        if user.check_password(password):
            user.backend = 'Accounts.backends.UserFarmerBackend'  # Set the backend attribute
            return user

    def get_user(self, user_id):
        try:
            return UserFarmer.objects.get(pk=user_id)
        except UserFarmer.DoesNotExist:
            return None

class UserDriverBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserDriver.objects.get(username=username)
        except UserDriver.DoesNotExist:
            return None

        if user.check_password(password):
            user.backend = 'Accounts.backends.UserDriverBackend'  # Set the backend attribute
            return user

    def get_user(self, user_id):
        try:
            return UserDriver.objects.get(pk=user_id)
        except UserDriver.DoesNotExist:
            return None
