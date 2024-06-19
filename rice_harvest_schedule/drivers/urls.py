#drivers/urls.py
from django.urls import path
from .views import*

urlpatterns = [
    path('add_vehicle/', add_vehicle, name='add_vehicle'),
    path('delete-vehicle/<int:vehicle_id>/', delete_vehicle, name='delete_vehicle'),
    path('calendar/', calendar_view, name='calendar_view'),
    path('get_calendar_events/', get_calendar_events, name='get_calendar_events'),
    path('add_calendar_event/', add_calendar_event, name='add_calendar_event'),
    path('edit_calendar_event/<int:event_id>/', edit_calendar_event, name='edit_calendar_event'),
    path('delete_calendar_event/<int:event_id>/', delete_calendar_event, name='delete_calendar_event'),
    path('schedule/<int:driver_id>/', driver_schedule, name='driver_schedule'),
 

]
