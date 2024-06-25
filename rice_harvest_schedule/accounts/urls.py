# accounts/urls.py
from django.contrib.auth import views
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
   path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
   path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
   path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
    # 


