#drivers/urls.py
from django.urls import path
from .views import*

urlpatterns = [
    # Provide a unique path for the driver home
    path('add_vehicle/', add_vehicle, name='add_vehicle'),
    path('add_detailvehicle/', add_detailvehicle, name='add_detailvehicle'),
    path('delete-vehicle/<int:vehicle_id>/',delete_vehicle, name='delete_vehicle'),
    path('calendar-events/', calendar_events, name='calendar_events'),
    path('add-event/', add_event, name='add_event'),


    
]
