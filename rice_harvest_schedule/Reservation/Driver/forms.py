# Driver/forms.py
from django import forms
from .models import Vehicle, Detailvehicle
from Accounts.models import*
class VehicleForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'clearable': False,'class': 'block w-full border border-gray-300 rounded-md px-3 py-2 mb-4 focus:outline-none focus:border-blue-500 focus:ring focus:ring-blue-300 '}))

    class Meta:
        model = Vehicle
        fields = ['model', 'type', 'price', 'province', 'image']

class DetailvehicleForm(forms.ModelForm):
    class Meta:
        model = Detailvehicle
        fields = ['power', 'details']



# Driver/forms.py

from django import forms
from .models import LicenseDocument

class LicenseDocumentForm(forms.ModelForm):
    class Meta:
        model = LicenseDocument
        fields = ['document']
        widgets = {
            'document': forms.ClearableFileInput(attrs={'required': True}),
        }
    
    def clean_document(self):
        # ตรวจสอบว่าไฟล์สามารถส่งเอกสารใหม่ได้หรือไม่
        if not self.instance.can_resubmit:
            raise forms.ValidationError("You cannot submit a new document.")
        return self.cleaned_data['document']
