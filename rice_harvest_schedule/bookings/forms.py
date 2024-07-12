# bookings/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['fullname', 'address', 'quantity', 'appointment_start_date', 'phone', 'details']
        widgets = {
            'details': forms.Textarea(attrs={'required': False}),  # Ensure the field is optional
        }
