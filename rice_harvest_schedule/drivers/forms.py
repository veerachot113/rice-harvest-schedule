# drivers/forms.py
from django import forms
from .models import *

class VehicleForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'clearable': False, 'class': 'block w-full border border-gray-300 rounded-md px-3 py-2 mb-4 focus:outline-none focus:border-blue-500 focus:ring focus:ring-blue-300'}))

    class Meta:
        model = Vehicle
        fields = ['model', 'type', 'price', 'province', 'image', 'min_acres', 'max_acres_per_day']

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'details','start','end']



class HarvestAreaForm(forms.ModelForm):
    class Meta:
        model = HarvestArea
        fields = ['start_date', 'end_date', 'province', 'district', 'subdistrict', 'details']