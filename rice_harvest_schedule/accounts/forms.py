# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserFarmer, UserDriver

class UserFarmerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ')  # เพิ่มชื่อ-สกุล
    last_name = forms.CharField(max_length=100, required=True, label='สกุล')  # สกุล
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่')  # เพิ่มที่อยู่
    phone = forms.CharField(max_length=15, required=True, label='เบอร์โทรศัพท์')  # เพิ่มเบอร์โทรศัพท์

    class Meta:
        model = UserFarmer
        fields = ['username', 'email', 'password1', 'password2', 'first_name','last_name',  'address', 'phone']

class UserFarmerUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ')  # เพิ่มชื่อ-สกุล
    last_name = forms.CharField(max_length=100, required=True, label='สกุล')  # สกุล
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่')  # เพิ่มที่อยู่
    phone = forms.CharField(max_length=15, required=True, label='เบอร์โทรศัพท์')  # เพิ่มเบอร์โทรศัพท์

    class Meta:
        model = UserFarmer
        fields = ['email', 'first_name','last_name', 'address', 'phone']

class UserDriverRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ')  # เพิ่มชื่อ-สกุล
    last_name = forms.CharField(max_length=100, required=True, label='สกุล')  # สกุล
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่')  # เพิ่มที่อยู่
    phone = forms.CharField(max_length=15, required=True, label='เบอร์โทรศัพท์')  # เพิ่มเบอร์โทรศัพท์

    class Meta:
        model = UserDriver
        fields = ['username', 'email', 'password1', 'password2', 'first_name','last_name', 'address', 'phone']



class UserDriverUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ')  # เพิ่มชื่อ-สกุล
    last_name = forms.CharField(max_length=100, required=True, label='สกุล')  # สกุล
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่')  # เพิ่มที่อยู่
    phone = forms.CharField(max_length=15, required=True, label='เบอร์โทรศัพท์')  # เพิ่มเบอร์โทรศัพท์

    class Meta:
        model = UserDriver
        fields = ['email', 'first_name','last_name', 'address', 'phone']
        
