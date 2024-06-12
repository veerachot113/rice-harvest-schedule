# accounts/urls.py
from django.contrib import *
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('logout/', custom_logout, name='logout'),
    path('userlogin/', user_login, name='login'),
    path('registerfarmer/', register_farmer, name='registerfarmer'),
    path('registerdriver/', register_driver, name='registerdriver'),
    path('useregister/', useregister, name='chooserole'),
    path('home_driver/', home_driver, name='home_driver'),
    path('home_farmer/', home_farmer, name='home_farmer'),
    path('profile/update/', profile_update, name='profile_update'),
    path('driver/<int:driver_id>/', view_driver_profile, name='view_driver_profile'),
]


