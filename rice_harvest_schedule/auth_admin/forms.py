# auth_admin/forms.py
from django import forms
from .models import DriverDocument

class DriverDocumentForm(forms.ModelForm):
    class Meta:
        model = DriverDocument
        fields = ['id_card', 'car_registration', 'driver_with_car']
