#drivers/urls.py
from django.urls import path
from .views import*

urlpatterns = [
    path('add_vehicle/', add_vehicle, name='add_vehicle'),
    path('delete-vehicle/<int:vehicle_id>/',delete_vehicle, name='delete_vehicle'),

]
