from django import forms
from .models import LicenseDocument

class LicenseDocumentForm(forms.ModelForm):
    class Meta:
        model = LicenseDocument
        fields = ['id_card', 'driving_license', 'vehicle_registration', 'photo']
        widgets = {
            'id_card': forms.ClearableFileInput(attrs={'required': True}),
            'driving_license': forms.ClearableFileInput(attrs={'required': True}),
            'vehicle_registration': forms.ClearableFileInput(attrs={'required': True}),
            'photo': forms.ClearableFileInput(attrs={'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.can_resubmit:
            raise forms.ValidationError("You cannot submit a new document.")
        return cleaned_data

class ReviewDocumentForm(forms.ModelForm):
    class Meta:
        model = LicenseDocument
        fields = ['reason']
