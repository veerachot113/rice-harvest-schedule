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
    path('schedule/<int:driver_id>/', get_schedule, name='get_schedule'),
    path('update_booking_dates/<int:event_id>/', update_booking_dates, name='update_booking_dates'),
    path('add_harvest_area/', add_harvest_area, name='add_harvest_area'),
    path('get_harvest_areas/', get_harvest_areas, name='get_harvest_areas'),
    path('update_harvest_area/<int:area_id>/', update_harvest_area, name='update_harvest_area'),
    path('delete_harvest_area/<int:area_id>/', delete_harvest_area, name='delete_harvest_area'),
    path('dashboard/', driver_dashboard, name='driver_dashboard'),
    path('detail/<int:event_id>/', booking_detail, name='booking_detail'),
    path('vehicle_detail/', vehicle_detail, name='vehicle_detail'),
    path('view_vehicle/<int:driver_id>/', view_vehicle_detail, name='view_vehicle_detail'),

]



 

